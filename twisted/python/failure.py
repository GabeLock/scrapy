class Failure(Exception):
    def __init__(self, value=None):
        super().__init__(value)
        self.value = value
