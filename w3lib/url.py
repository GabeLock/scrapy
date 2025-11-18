from __future__ import annotations

import base64
import os
from typing import Iterable, Optional, Tuple
from urllib.parse import (
    ParseResult,
    parse_qsl,
    quote,
    unquote,
    urldefrag,
    urlencode,
    urlparse,
    urlunparse,
)

_safe_chars = frozenset(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~!$&'()*+,;=:@/")


def _unquotepath(value: str) -> str:
    return unquote(value)


__all__ = [
    "ParseResult",
    "safe_url_string",
    "canonicalize_url",
    "add_or_replace_parameter",
    "urldefrag",
    "urlparse",
    "urlunparse",
    "url_query_parameter",
    "any_to_uri",
    "file_uri_to_path",
    "path_to_file_uri",
]


def _sorted_query(params: Iterable[Tuple[str, str]]) -> str:
    return urlencode(sorted(params), doseq=True)


def canonicalize_url(url: str, keep_fragments: bool = False) -> str:
    parsed = urlparse(url)
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    if ":" in netloc:
        host, port = netloc.rsplit(":", 1)
        if (scheme == "http" and port == "80") or (scheme == "https" and port == "443"):
            netloc = host
    path = unquote(parsed.path or "/")
    path = quote(path, safe="/%:@")
    query_pairs = parse_qsl(parsed.query, keep_blank_values=True)
    query_pairs.sort()
    query = urlencode(query_pairs, doseq=True)
    fragment = parsed.fragment if keep_fragments else ""
    return urlunparse((scheme, netloc, path, parsed.params, query, fragment))


def safe_url_string(url: str, encoding: str = "utf-8") -> str:
    parsed = urlparse(url)
    safe_path = quote(parsed.path.encode(encoding, errors="ignore"), safe="/@:+")
    safe_query = quote(parsed.query.encode(encoding, errors="ignore"), safe="=&?/:+%")
    return urlunparse((parsed.scheme, parsed.netloc, safe_path, parsed.params, safe_query, parsed.fragment))


def add_or_replace_parameter(url: str, name: str, value: str) -> str:
    parsed = urlparse(url)
    params = [(k, v) for k, v in parse_qsl(parsed.query, keep_blank_values=True) if k != name]
    params.append((name, value))
    query = urlencode(params, doseq=True)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, query, parsed.fragment))


def url_query_parameter(url: str, key: str, default: Optional[str] = None) -> Optional[str]:
    for k, v in parse_qsl(urlparse(url).query, keep_blank_values=True):
        if k == key:
            return v
    return default


def any_to_uri(path: str) -> str:
    if path.startswith("file://"):
        return path
    if os.path.exists(path):
        return f"file://{path}"
    return path


def parse_data_uri(uri: str) -> Tuple[str, bytes]:
    if not uri.startswith("data:"):
        raise ValueError("Not a data URI")
    _, data = uri.split(",", 1)
    return "text/plain", base64.b64decode(data)


def path_to_file_uri(path: str) -> str:
    if path.startswith("file://"):
        return path
    return f"file://{path}"


def file_uri_to_path(uri: str) -> str:
    if not uri.startswith("file://"):
        raise ValueError("Not a file URI")
    return uri[7:]
