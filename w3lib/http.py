from __future__ import annotations

import base64
from typing import Iterable, List, Tuple


def basic_auth_header(username: str, password: str) -> bytes:
    token = f"{username}:{password}".encode("utf-8")
    return b"Basic " + base64.b64encode(token)


def headers_dict_to_raw(headers: Iterable[Tuple[str, List[bytes]]]) -> bytes:
    lines: List[bytes] = []
    iterable = headers.items() if hasattr(headers, "items") else headers
    for name, values in iterable:
        header_name = name.decode("latin-1") if isinstance(name, bytes) else str(name)
        for value in values:
            header_value = value.decode("latin-1") if isinstance(value, bytes) else str(value)
            lines.append(f"{header_name}: {header_value}".encode("latin-1"))
    if not lines:
        return b""
    return b"\r\n".join(lines)


def headers_raw_to_dict(raw_headers: bytes) -> List[Tuple[bytes, bytes]]:
    headers: List[Tuple[bytes, bytes]] = []
    for line in raw_headers.splitlines():
        if not line:
            continue
        if b":" in line:
            name, value = line.split(b":", 1)
            headers.append((name.strip(), value.strip()))
    return headers
