from rmbserver.ai.openai_client import openai_llm
import json
from jinja2 import Template


def ai_generate(prompt_template: str,
                template_format: str = "jinja2",  # jinja2 or string
                output_format: str = "json",  # json or str
                **input_variables
                ) -> str or dict:
    """
    根据模板生成文本
    """
    if input_variables is None:
        input_variables = {}

        # 处理Jinja2模板
    if template_format == "jinja2":
        template = Template(prompt_template)
        prompt = template.render(**input_variables)
    else:
        prompt = prompt_template.format(**input_variables)

        # 调用OpenAI API
    if output_format == "json":
        return json.loads(openai_llm.predict(prompt, json_format=True))
    elif output_format == "str":
        return openai_llm.predict(prompt)
    else:
        raise ValueError(f"output_format must be json or str, but got {output_format}")
