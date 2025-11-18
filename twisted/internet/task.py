class LoopingCall:
    def __init__(self, func=None, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def start(self, interval, now=True):
        if self.func:
            self.func(*self.args, **self.kwargs)
        return None


class Cooperator:
    def coiterate(self, iterable):
        return iterable
