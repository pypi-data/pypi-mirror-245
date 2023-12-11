# Error Design

# 1000 - 资源和配置类错误
# 2000 - QA对话类错误
# 3000 - 大模型类错误


class DataSourceExists(Exception):
    code = 1001
    message = "数据源已存在"


class DataSourceNotFound(Exception):
    code = 1002
    message = "数据源不存在"


class ChatNotFound(Exception):
    code = 1003
    message = "对话不存在"


class ParameterError(Exception):
    code = 1004
    message = "参数错误"


class DataSourceConfigError(Exception):
    code = 1005
    message = "数据源配置错误"


class BIQAError(Exception):
    code = 2001


class BINoMatchDataSource(BIQAError):
    code = 2002


class BIInsufficientData(BIQAError):
    code = 2003


class BIIncompleteQuestion(BIQAError):
    code = 2004


class PromptTooLong(Exception):
    code = 3001
