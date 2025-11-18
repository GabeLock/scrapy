from __future__ import annotations

import codecs
import re
from typing import Callable, Optional, Tuple

_charset_re = re.compile(r"charset=\s*['\"]?([^;\s'\"]+)", re.I)
_meta_re = re.compile(r"<meta[^>]+charset=['\"]?([^\s'\"/>]+)", re.I)


def resolve_encoding(encoding: Optional[str]) -> Optional[str]:
    if encoding is None:
        return None
    try:
        return codecs.lookup(encoding).name
    except LookupError:
        return None


def http_content_type_encoding(header: str) -> Optional[str]:
    match = _charset_re.search(header)
    if match:
        return resolve_encoding(match.group(1))
    return None


def html_body_declared_encoding(body: bytes) -> Optional[str]:
    match = _meta_re.search(body.decode("latin-1", errors="ignore"))
    if match:
        return resolve_encoding(match.group(1))
    return None


def read_bom(body: bytes) -> Tuple[Optional[str], bytes]:
    for bom, encoding in (
        (codecs.BOM_UTF8, "utf-8"),
        (codecs.BOM_UTF16_LE, "utf-16-le"),
        (codecs.BOM_UTF16_BE, "utf-16-be"),
    ):
        if body.startswith(bom):
            return encoding, body[len(bom) :]
    return None, body


def html_to_unicode(
    declared_encoding: str,
    body: bytes,
    auto_detect_fun: Optional[Callable[[bytes], Optional[str]]] = None,
    default_encoding: str = "ascii",
):
    encoding = resolve_encoding(http_content_type_encoding(declared_encoding))
    if encoding is None and auto_detect_fun is not None:
        encoding = auto_detect_fun(body)
    if encoding is None:
        encoding = default_encoding
    try:
        return encoding, body.decode(encoding)
    except (LookupError, UnicodeDecodeError):
        return encoding, body.decode(encoding, errors="replace")
