"""Base Fabman Object for all other returned objects"""

from typing import Any
import fabman.requester


class FabmanObject(object):
    """Base class for all classes representing objects returned by the API

    This makes a call to `fabman.fabman_object.FabmanObject.set_attributes`
    to dynamically construct this object's attributes with a JSON object

    Based off of canvasapi.canvas_object.CanvasObject found at
    https://github.com/ucfopen/canvasapi/blob/develop/canvasapi/canvas_object.py
    """

    def __getattribute__(self, __name: str) -> Any:
        return super(FabmanObject, self).__getattribute__(__name)

    def __init__(self, requester: fabman.requester.Requester, attributes: dict) -> None:
        """Initialize the Object. Stores the requester method to interact
        with the API for further calls

        Args:
            requester (_type_): _description_
            attributes (_type_): _description_
        """

        self._requester = requester
        self.set_attributes(attributes)

    def __repr__(self) -> str:
        classname = self.__class__.__name__
        attrs = ", ".join(
            [
                f"{k}={v}"
                for k, v in self.__dict__.items()
                if not k.startswith("_") and k != "attributes"
            ]
        )

        return f"<{classname} {attrs}>"

    def set_attributes(self, attributes: dict):
        """Loads this object with attributes."""
        for attr, val in attributes.items():
            setattr(self, attr, val)
