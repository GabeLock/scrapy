import platform
import sys
from typing import List, Tuple

try:
    import cryptography
except ImportError:  # pragma: no cover - optional dependency
    cryptography = None

try:
    import cssselect
except ImportError:  # pragma: no cover - optional dependency
    cssselect = None

try:
    import lxml.etree  # nosec
except ImportError:  # pragma: no cover - optional dependency
    lxml = None
else:
    lxml = lxml

try:
    import parsel
except ImportError:  # pragma: no cover - optional dependency
    parsel = None

try:
    import twisted
except ImportError:  # pragma: no cover - optional dependency
    twisted = None

try:
    import w3lib
except ImportError:  # pragma: no cover - optional dependency
    w3lib = None

import scrapy
from scrapy.utils.ssl import get_openssl_version


def scrapy_components_versions() -> List[Tuple[str, str]]:
    if lxml is not None:
        lxml_version = ".".join(map(str, lxml.etree.LXML_VERSION))
        libxml2_version = ".".join(map(str, lxml.etree.LIBXML_VERSION))
    else:
        lxml_version = libxml2_version = "unavailable"

    cssselect_version = getattr(cssselect, "__version__", "unavailable")
    parsel_version = getattr(parsel, "__version__", "unavailable")
    w3lib_version = getattr(w3lib, "__version__", "unavailable")
    twisted_version = (
        twisted.version.short() if getattr(twisted, "version", None) else "unavailable"
    )
    cryptography_version = getattr(cryptography, "__version__", "unavailable")

    return [
        ("Scrapy", scrapy.__version__),
        ("lxml", lxml_version),
        ("libxml2", libxml2_version),
        ("cssselect", cssselect_version),
        ("parsel", parsel_version),
        ("w3lib", w3lib_version),
        ("Twisted", twisted_version),
        ("Python", sys.version.replace("\n", "- ")),
        ("pyOpenSSL", get_openssl_version()),
        ("cryptography", cryptography_version),
        ("Platform", platform.platform()),
    ]
