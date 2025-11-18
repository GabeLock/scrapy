HTML5_WHITESPACE = "\t\n\x0c\r "


def strip_html5_whitespace(value: str) -> str:
    return value.strip(HTML5_WHITESPACE)
