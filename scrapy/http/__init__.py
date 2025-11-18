"""Module containing all HTTP related classes."""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = [
    "Headers",
    "Request",
    "FormRequest",
    "JsonRequest",
    "XmlRpcRequest",
    "Response",
    "HtmlResponse",
    "JsonResponse",
    "TextResponse",
    "XmlResponse",
]

_lazy_modules = {
    "Headers": "scrapy.http.headers",
    "Request": "scrapy.http.request",
    "FormRequest": "scrapy.http.request.form",
    "JsonRequest": "scrapy.http.request.json_request",
    "XmlRpcRequest": "scrapy.http.request.rpc",
    "Response": "scrapy.http.response",
    "HtmlResponse": "scrapy.http.response.html",
    "JsonResponse": "scrapy.http.response.json",
    "TextResponse": "scrapy.http.response.text",
    "XmlResponse": "scrapy.http.response.xml",
}


def __getattr__(name: str) -> Any:
    if name not in _lazy_modules:
        raise AttributeError(f"module 'scrapy.http' has no attribute {name!r}")
    module = import_module(_lazy_modules[name])
    value = getattr(module, name)
    globals()[name] = value
    return value
