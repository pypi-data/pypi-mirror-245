from rmbcommon.models import MetaData
from rmbserver.ai.generations.base import ai_generate
from rmbserver.log import log

PROMPT_GEN_META = """
处理并更新给定的 MetaData，包括：

1. 为每个对象（schema/table/field）推测并更新其含义到 curr_desc 字段，若已有内容则保留。
2. 对于field可以直接根据name来推测，对于table则不止根据table name，更要结合其下的field来推测，对于schema则不止根据schema name，更要结合其下的table来推测。
3. 推测字段间的关联关系，更新相关字段的 related_field 和准确率 related_field_precision_rate（范围 0-1）。若无关联，则不用设置这2个字段。
（比如，如果 db01 数据库下的 book 表的 auth_id 字段与 author 表的 id 字段相关联，则应更新 book.auth_id 的 related_field 为 db01.author.id。）
4. 保持 MetaData 格式不变。

请注意，对于不确定的含义，使用“未知”更新 curr_desc 字段。

输入 MetaData={{ meta_data }}
更新后的 MetaData=
"""


def gen_meta_desc_and_relations(meta_data: MetaData) -> MetaData:
    """
    生成描述和关联关系
    ## TODO 测试上面prompt的第二点。
    """
    # 使用to_string_for_llm()方法，只返回存在字段描述 curr_desc 为空的表
    inferred_meta = ai_generate(PROMPT_GEN_META,
                                meta_data=meta_data.to_string_for_llm())
    log.info(f"原始 Meta：{meta_data.to_string_for_llm()}")
    log.info(f"更新后的 Meta： {inferred_meta}")

    if inferred_meta.get("MetaData"):
        inferred_meta = inferred_meta["MetaData"]
    log.info(f"推理结果：{inferred_meta}")
    return MetaData.load_from_dict(inferred_meta)

