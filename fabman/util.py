"""General Utility Functions to be used throughout the package"""

from typing import Any


def is_multivalued(value: Any):
    """
    Determines if the given value is a list or tuple when used as a request 
    parameter. In general, anything that is multivalued will be considered here.
    The one special case would be strings and byte strings, which are iterable
    but not multi-valued.
    """

    if isinstance(value, (str, bytes)):
        return False

    try:
        iter(value)
        return True
    except TypeError:
        return False


def clean_headers(headers: dict):
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


def combine_kwargs(**kwargs):
    """Flatten a series of keywwords.
    """
    combined_kwargs = []

    for kw, arg in kwargs.items():  # pylint: disable=invalid-name
        if isinstance(arg, dict):
            for k, v in arg.items():  # pylint: disable=invalid-name
                for tup in flatten_kwarg(k, v):
                    combined_kwargs.append((f"{kw}{tup[0]}", tup[1]))
        elif is_multivalued(arg):
            for i in arg:
                for tup in flatten_kwarg("", i):
                    combined_kwargs.append((f"{kw}{tup[0]}", tup[1]))
        else:
            combined_kwargs.append((str(kw), arg))

    return combined_kwargs


def flatten_kwarg(key: Any, obj: Any):
    """Recursive call to flatten sections of a kwarg to be combined.

    Args:
        key (Any): The partial keyword to add to the full keyword
        obj (Any): The object to translate into a kwarg. If the type
        is `dict`, the key parameter will be added to the keyword between
        square brackets and recursively call this function. If the type is 
        `list` or `tuple`, a set of empty brackets will be appended to the 
        keyword and recursively call this function. Otherwise, the function
        returns with the final keyword and value

    Returns:
        _type_: _description_
    """
    if isinstance(obj, dict):
        new_list = []
        for k, v in obj.items():  # pylint: disable=invalid-name
            for tup in flatten_kwarg(k, v):
                new_list.append((f"{tup[0]}", tup[1]))
        return new_list

    if is_multivalued(obj):
        new_list = []
        for i in obj:
            for tup in flatten_kwarg(key, i):
                new_list.append((tup[0], tup[1]))
        return new_list

    # base case
    return [(f"{str(key)}", obj)]
