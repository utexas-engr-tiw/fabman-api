"""Exceptions for use throughout the package"""


class FabmanException(Exception):
    """Base class for all Fabman exceptions"""

    def __init__(self, message):
        if isinstance(message, dict):

            errors = message.get("errors", None)

            if errors:
                self.message = errors
            else:
                self.message("Something went wrong ", message)
        else:
            self.message = message

    def __str__(self):
        return str(self.message)


class BadRequest(FabmanException):
    """Fabman was unable to understand the request. More information may be needed"""


class InvalidAccessToken(FabmanException):
    """The access token provided was invalid"""


class Unauthorized(FabmanException):
    """The access token provided was not authorized to access the resource"""


class ResourceDoesNotExist(FabmanException):
    """The resource requested does not exist"""


class ForbiddenError(FabmanException):
    """The access token provided does not have permission to access the resource"""


class Conflict(FabmanException):
    """The request could not be completed due to a conflict with the current 
    state of the resource"""


class UnprocessableEntity(FabmanException):
    """The request was well-formed but was unable to be followed due to semantic errors"""


class RateLimitExceeded(FabmanException):
    """The request was valid, but too may requests have been issued from this access token. 
    Please try again later"""
