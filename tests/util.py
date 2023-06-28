"""Utility functions for tests. Taken from 
https://github.com/ucfopen/canvasapi/blob/develop/tests/util.py"""

import json
import os
from urllib.parse import parse_qsl

import requests
import requests_mock

from tests import settings


def register_uris(requirements, requests_mocker, base_url=None):
    """
    Given a list of required fixtures and an requests_mocker object,
    register each fixture as a uri with the mocker.

    :param base_url: str
    :param requirements: dict
    :param requests_mocker: requests_mock.mocker.Mocker
    """
    if base_url is None:
        base_url = settings.BASE_URL_WITH_VERSION
    for fixture, objects in requirements.items():
        try:
            with open(f"tests/fixtures/{fixture}.json", encoding="utf-8") as file:
                data = json.loads(file.read())
        except (IOError, ValueError) as exc:
            raise ValueError(f"Fixture {fixture}.json contains invalid JSON.") from exc

        if not isinstance(objects, list):
            raise TypeError(f"{objects} is not a list.")

        for obj_name in objects:
            obj = data.get(obj_name)

            if obj is None:
                raise ValueError(f"{repr(obj_name)} does not exist in {fixture}.json")

            method = requests_mock.ANY if obj["method"] == "ANY" else obj["method"]
            if obj["endpoint"] == "ANY":
                url = requests_mock.ANY
            else:
                url = base_url + obj["endpoint"]

            try:
                requests_mocker.register_uri(
                    method,
                    url,
                    json=obj.get("data"),
                    status_code=obj.get("status_code", 200),
                    headers=obj.get("headers", {}),
                )
            except RuntimeError as exc:
                print(exc)


def cleanup_file(filename):
    """
    Remove a test file from the system. If the file doesn't exist, ignore.

    `Not as stupid as it looks. <http://stackoverflow.com/a/10840586>_`
    """
    try:
        os.remove(filename)
    except OSError:
        pass


def validate_update(request, context):
    """Used for validating update requests have the lockVersion parameter."""
    data = dict(parse_qsl(request.body))
    if "lockVersion" in data:
        data["lockVersion"] = int(data["lockVersion"]) + 1
        context.status_code = 200
    else:
        context.status_code = 400
    return json.dumps(data)


def test_exceptions(request, context):
    """Used for testing exception handling."""
    req = str(request)
    if "400" in req:
        context.status_code = 400
        return json.dumps({"errors": "Bad Request"})
    if "401_invalid" in req:
        context.headers["WWW-Authenticate"] = "Bearer"
        context.status_code = 401
        return json.dumps({"errors": "Unauthorized"})
    if "401_unauthorized" in req:
        context.status_code = 401
        return json.dumps({"errors": "Unauthorized"})
    if "403" in req:
        context.status_code = 403
        return json.dumps({"errors": "Forbidden"})
    if "404" in req:
        context.status_code = 404
        return json.dumps({"errors": "Not found"})
    if "409" in req:
        context.status_code = 409
        return json.dumps({"errors": "Conflict"})
    if "422" in req:
        context.status_code = 422
        return json.dumps({"errors": "Unprocessable Entity"})
    if "420" in req:
        context.status_code = 420
        return json.dumps({"errors": "Enhance Your Calm"})
