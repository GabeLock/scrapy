class ItemAdapter:
    def __init__(self, item):
        self.item = item

    def asdict(self):
        return dict(self.item)


def is_item(value):
    return isinstance(value, (dict, ItemAdapter))
