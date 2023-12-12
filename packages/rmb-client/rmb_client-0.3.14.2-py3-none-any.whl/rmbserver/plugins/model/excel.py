from rmbcommon.models.bi import StrucQuery, QueryResult


class ExcelQuery(StrucQuery):
    pass


class ExcelQueryResult(QueryResult):
    __source_type__ = "Excel"

    @property
    def rows(self):
        return self.content.values

    @property
    def columns(self):
        return self.content.columns

    def __str__(self):
        return self.content.to_string()[0:2000]  # 截取前2000个字符
