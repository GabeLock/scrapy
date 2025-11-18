from . import defer


def deferToThread(func, *args, **kwargs):
    return defer.Deferred(func(*args, **kwargs))
