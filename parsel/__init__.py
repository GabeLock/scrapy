class SelectorList(list):
    def xpath(self, *args, **kwargs):
        return self.__class__()

    def css(self, *args, **kwargs):
        return self.__class__()

    def get(self, default=None):
        return self[0] if self else default

    def getall(self):
        return list(self)

    def jmespath(self, *args, **kwargs):
        return self.__class__()


class Selector:
    selectorlist_cls = SelectorList

    def __init__(self, response=None, text=None, type=None, root=None, **kwargs):
        self.response = response

    def xpath(self, *args, **kwargs):
        return self.selectorlist_cls()

    def css(self, *args, **kwargs):
        return self.selectorlist_cls()

    def get(self, default=None):
        return default

    def getall(self):
        return []

    def jmespath(self, *args, **kwargs):
        return self.selectorlist_cls()
