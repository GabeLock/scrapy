from __future__ import annotations

from typing import Any, Callable, Generator


class Deferred:
    def __init__(self, result: Any = None) -> None:
        self.result = result

    def addBoth(self, callback: Callable[[Any], Any]) -> "Deferred":
        if callback:
            self.result = callback(self.result)
        return self

    def addCallback(self, callback: Callable[[Any], Any]) -> "Deferred":
        if callback:
            self.result = callback(self.result)
        return self

    def callback(self, result: Any) -> None:
        self.result = result


class DeferredList(Deferred):
    def __init__(self, deferred_list: list[Deferred]) -> None:
        super().__init__(deferred_list)


def inlineCallbacks(func: Callable[..., Generator[Any, Any, Any]]) -> Callable:
    return func


def maybeDeferred(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    return func(*args, **kwargs)


def succeed(result: Any = None) -> Deferred:
    d = Deferred(result)
    return d


def ensureDeferred(result: Any) -> Any:
    return result
