"""
Scrapy - a web crawling and web scraping framework written for Python
"""

import pkgutil
import sys
import warnings
from importlib import import_module

from twisted import version as _txv

__all__ = [
    "__version__",
    "version_info",
    "twisted_version",
    "Spider",
    "Request",
    "FormRequest",
    "Selector",
    "Item",
    "Field",
]

_lazy_imports = {
    "Spider": "scrapy.spiders",
    "Request": "scrapy.http",
    "FormRequest": "scrapy.http",
    "Selector": "scrapy.selector",
    "Item": "scrapy.item",
    "Field": "scrapy.item",
}


# Scrapy and Twisted versions
__version__ = (pkgutil.get_data(__package__, "VERSION") or b"").decode("ascii").strip()
version_info = tuple(int(v) if v.isdigit() else v for v in __version__.split("."))
twisted_version = (_txv.major, _txv.minor, _txv.micro)


# Check minimum required Python version
if sys.version_info < (3, 8):
    print(f"Scrapy {__version__} requires Python 3.8+")
    sys.exit(1)


# Ignore noisy twisted deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="twisted")


def __getattr__(name: str):
    if name not in _lazy_imports:
        raise AttributeError(f"module 'scrapy' has no attribute {name!r}")
    module = import_module(_lazy_imports[name])
    value = getattr(module, name)
    globals()[name] = value
    return value


del pkgutil
del sys
del warnings
