from __future__ import annotations

from typing import Any


class Port:
    def __init__(self, port: int, factory: Any, interface: str | None = None) -> None:
        self.port = port
        self.factory = factory
        self.interface = interface

    def stopListening(self) -> None:  # pragma: no cover - not exercised
        return None
