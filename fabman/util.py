"""General Utility Functions to be used throughout the package"""

from typing import Union

from requests.structures import CaseInsensitiveDict


def clean_headers(headers: Union[dict, CaseInsensitiveDict]):
    """Cleans the headers to hide sensitive information in logs.
    Originally defined in canvasapi/util.py:
    https://github.com/ucfopen/canvasapi/blob/develop/canvasapi/util.py#L228

    Args:
        headers (dict): The headers to sanitize

    Returns:
        _type_: _description_
    """
    cleaned_headers = headers.copy()

    authorization_header = headers.get("Authorization")
    if authorization_header:
        sanitized = "****" + authorization_header[-4:]
        cleaned_headers["Authorization"] = sanitized

    return cleaned_headers
