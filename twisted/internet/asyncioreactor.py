from __future__ import annotations

from typing import Any, Callable


class AsyncioSelectorReactor:
    def __init__(self, eventloop: Any = None) -> None:
        self._asyncioEventloop = eventloop

    def callLater(self, delay: float, func: Callable, *args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    def callFromThread(self, func: Callable, *args: Any, **kwargs: Any) -> None:
        func(*args, **kwargs)

    def stop(self) -> None:  # pragma: no cover - not exercised
        return None


def install(eventloop: Any = None) -> AsyncioSelectorReactor:
    import twisted.internet as internet

    internet.reactor = AsyncioSelectorReactor(eventloop)
    return internet.reactor
