"""General Utility Functions to be used throughout the package"""


def clean_headers(headers):
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
