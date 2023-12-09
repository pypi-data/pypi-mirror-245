
class BIQuestion:

    def __init__(self, content):
        self.content = content

    def __str__(self):
        return self.content

class BIQueryPlan:
    pass


class NaturalQuery:

    def __init__(self, content: str):
        self.content = content

    def __str__(self):
        return self.content


class StrucQuery:
    pass

    def __init__(self, content: str):
        self.content = content

    def __str__(self):
        return self.content

    def __repr__(self):
        return self.__str__()


class QueryResult:

    def __init__(self, content: any):
        self.content = content

    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        return self.__str__()

class BIAnswer:
    def __init__(self, content: str):
        self.content = content

    def __str__(self):
        return self.content
