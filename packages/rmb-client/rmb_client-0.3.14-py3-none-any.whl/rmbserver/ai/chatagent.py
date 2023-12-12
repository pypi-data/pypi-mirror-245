from functools import wraps

import httpx
from langchain.agents import (
    # AgentType,
    Tool,
    # initialize_agent,
)
from langchain.agents import AgentExecutor, ConversationalAgent
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

from rmbserver import config
from rmbserver.log import log
from rmbserver.ai.prompts import (
    PROMPT_AGENT_PREFIX,
    PROMPT_AGENT_SUFFIX,
    PROMPT_AGENT_FORMAT_INSTRUCTIONS,
    PROMPT_CHOOSE_DATASOURCE,
    PROMPT_GEN_STRUC_QUERY,
    PROMPT_GEN_BI_ANSWER,
    PROMPT_CHECK_QUESTION_INTEGRITY,
)

from rmbserver.exceptions import (
    BIQAError,
    BINoMatchDataSource,
    BIInsufficientData,
    BIIncompleteQuestion,
)
from rmbserver.analysis.chat import Chat
from rmbserver.brain.datasource import DataSource
from rmbcommon.models import StrucQuery
from rmbserver.ai.generations import ai_generate


def handle_biqa_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BIQAError as e:
            error_type = e.__class__.__name__
            return f"BIQAError查询失败，原因是 {error_type}: {e}"
    return wrapper


class ChatAgentManager:

    def __init__(self, chat: Chat):
        self.chat = chat
        self.agent = self.create_agent()

    def _choose_a_data_source(self, question: str) -> DataSource:
        ds_summary = ""
        for ds in self.chat.datasources:
            ds_summary += f"{ds.type}数据源[{ds.name}][{ds.id}]包含以下数据表：\n"
            ds_summary += ds.brain_meta.to_table(level='table')

        choice_datasource = ai_generate(
            PROMPT_CHOOSE_DATASOURCE,
            template_format="jinja2",
            question=question,
            datasources_summary=ds_summary
        )["choice_datasource_id"]
        if choice_datasource:
            return DataSource.get(choice_datasource)
        else:
            raise BINoMatchDataSource(
                f"从你选择的数据源（{','.join([ds.name for ds in self.chat.datasources])}）"
                f"中无法回答问题【{question}】。"
            )

    def _query_to_a_data_source(
            self,
            data_source: DataSource,
            question: str
    ) -> list[dict]:
        output = ai_generate(
            PROMPT_GEN_STRUC_QUERY,
            datasource_prompt=data_source.accessor.PROMPT_GEN_STRUC_QUERY,
            bi_question=question,
            meta_data=data_source.brain_meta.to_dict(),
        )
        if output.get("PossibleMissingTable", None):
            log.warning(f"在{data_source.name}[{data_source.id}]中从查询{question}，")
            raise BIInsufficientData(
                f"在{data_source.name}[{data_source.id}]中从查询{question}，"
                f"缺失这些信息: {output['PossibleMissingTable']}")
        else:
            struc_queries = [StrucQuery(query) for query in output["StructureQueries"]]
            log.info(f"数据源：[{data_source}]"
                     f"\n问题：[{question}]\n查询语句：{struc_queries}")

        query_and_results = [
            {
                'StrucQuery': query,
                'QueryResult': data_source.accessor.query(query)
            } for query in struc_queries
        ]
        return query_and_results

    def _generate_answer(
            self,
            data_source: DataSource,
            question: str,
            query_and_results: list
    ) -> str:
        output = ai_generate(
            PROMPT_GEN_BI_ANSWER,
            datasource_type=data_source.type,
            bi_question=question,
            meta_data=data_source.brain_meta.to_dict(),
            query_and_results=query_and_results
        )
        log.info(f"根据问题、数据源类型、元数据、查询语句和结果，生成答案: {output}")
        return output

    @handle_biqa_error
    def tool_answer_bi_question(self, question: str) -> str:
        # choose a data source
        if len(self.chat.datasources) == 1:
            data_source = self.chat.datasources[0]
        else:
            data_source = self._choose_a_data_source(question)

        # query to a data source
        query_and_results = self._query_to_a_data_source(data_source, question)

        # generate answer using query result
        answer = self._generate_answer(
            data_source,
            question,
            query_and_results
        )
        return answer

    @handle_biqa_error
    def tool_check_question_integrity(self, question: str) -> str:
        output = ai_generate(
            PROMPT_CHECK_QUESTION_INTEGRITY,
            meta_data=[data_source.brain_meta.to_dict()
                       for data_source in self.chat.datasources],
            question=question,
            chat_history='\n'.join(
                [f"{msg.role}:{msg.content}" for msg in self.chat.messages(10)]
            )
        )
        log.info(f"问题: {question} \n检查完整性： {output}")
        if output.get("more_info_feedback", None):
            log.warning(f"需要补充信息：{output['more_info_feedback']}")
            raise BIIncompleteQuestion(output['more_info_feedback'])
        return output["summarized_question"]

    @property
    def tools(self):
        return [
            Tool(
                name="answer question from a private database",
                description="useful for when you need to answer questions from a private database",
                func=self.tool_answer_bi_question,
            ),
            Tool(
                name="question integrity check",
                description="check if the bi question is complete before answering",
                func=self.tool_check_question_integrity,
            )
        ]

    @property
    def agent_prompt(self):
        prompt = ConversationalAgent.create_prompt(
            self.tools,
            prefix=PROMPT_AGENT_PREFIX,
            suffix=PROMPT_AGENT_SUFFIX,
            format_instructions=PROMPT_AGENT_FORMAT_INSTRUCTIONS,
        )
        return prompt

    def create_agent(self, ):

        kwargs = {
            "model": config.openai_model_name,
            "openai_api_key": config.openai_api_key,
            "verbose": True,
            # Agent 里面不能用JSON输出，ReAct output parser 要跟着改
            # "model_kwargs": {
            #     "response_format": {"type": "json_object"},
            # },
        }
        if config.openai_proxy:
            kwargs["http_client"] = httpx.Client(
                proxies=config.openai_proxy,
            )

        llm = ChatOpenAI(**kwargs)

        # memory
        memory = ConversationBufferMemory(memory_key="chat_history")

        for msg in self.chat.messages(limit=30):
            if msg.role == 'human':
                memory.chat_memory.add_user_message(str(msg.content))
            elif msg.role == 'ai':
                memory.chat_memory.add_ai_message(str(msg.content))
            else:
                log.warning(f"Unknown message role: {msg}")

        # Re-define Agent Prompt
        llm_chain = LLMChain(llm=llm, prompt=self.agent_prompt)

        agent = ConversationalAgent(
            llm_chain=llm_chain,
            tools=self.tools,
        )

        chat_agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=self.tools,
            memory=memory,
            verbose=True
        )

        # # Direct create agent executor
        # chat_agent_executor = initialize_agent(
        #     self.tools,
        #     llm,
        #     agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        #     verbose=True,
        #     memory=memory,
        #     # output_parser=ReActSingleInputOutputParser(),
        #     # output_parser=ConvoOutputParser(),
        # )

        return chat_agent_executor

    def query(self, question: str) -> str:
        response = self.agent.invoke({"input": question})["output"]
        # log.debug(f"\nHuman: {question} \nAI: {response}")
        return response
