from __future__ import annotations

from typing import Any, Callable


class DelayedCall:
    def __init__(self, delay: float, func: Callable | None, *args: Any, **kwargs: Any) -> None:
        self.delay = delay
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self._cancelled = False

    def cancel(self) -> None:
        self._cancelled = True

    def __call__(self) -> None:
        if not self._cancelled and self._func:
            self._func(*self._args, **self._kwargs)


class ThreadedResolver:
    pass
