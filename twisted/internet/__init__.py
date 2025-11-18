"""Tiny subset of ``twisted.internet`` needed for the unit tests."""
from __future__ import annotations

from typing import Any, Callable

from .base import DelayedCall
from .tcp import Port


class _FakeReactor:
    """Extremely small reactor stub.

    It is only meant to satisfy tests that import Scrapy components while
    Twisted is unavailable in this execution environment.
    """

    def __init__(self) -> None:
        self._asyncioEventloop: Any = None

    def callLater(self, delay: float, func: Callable, *args: Any, **kwargs: Any) -> DelayedCall:
        call = DelayedCall(delay, func, *args, **kwargs)
        call()
        return call

    def callFromThread(self, func: Callable, *args: Any, **kwargs: Any) -> None:
        func(*args, **kwargs)

    def listenTCP(self, port: int, factory: Any, interface: str | None = None) -> Port:
        return Port(port, factory, interface=interface)

    def stop(self) -> None:  # pragma: no cover - nothing to clean up
        return None


reactor = _FakeReactor()
