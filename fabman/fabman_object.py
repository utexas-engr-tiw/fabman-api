"""Base Fabman Object for all other returned objects"""

from typing import Any

import fabman.requester


class FabmanStaticObject(object):
    """
    Base class for all objects returned from the API which do not have any
    associated methods to call. For example, Payment Info objects returned from
    an Account are immutable
    """

    def __getattribute__(self, __name: str) -> Any:
        return super(FabmanStaticObject, self).__getattribute__(__name)

    def __init__(self, attributes: dict) -> None:
        """Initializes the object and calls :code:`set_attributes` to dynamically
        populate the attributes of the class

        :param attributes: dictionary of attributes to set
        :type attributes: dict
        :return: Nothing
        :rtype: None
        """

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
        """Helper method to set attributes on the object

        :param attributes: dictionary of attributes
        :type attributes: dict
        """
        for attr, val in attributes.items():
            setattr(self, attr, val)


class FabmanObject(object):
    """
    Base class for all classes representing objects returned by the API

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

        :param requester: The :code:`Requester` object to make requests with
        :type requester: :code:`Requester`
        :param attributes: The attributes to initialize this object with
        :type attributes: dict
        """

        self._requester = requester
        self.set_attributes(attributes)
        if "_embedded" not in self.__dict__:
            self._embedded = {}

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
        """
        Loads the Object with the specified attributes. Typically, these attributes
        will be returned by the API when the object is created. Can also be used when
        update 'PUT' requests are made to the API.

        :param attributes: The attributes to initialize this object with
        :type attributes: dict
        """
        for attr, val in attributes.items():
            setattr(self, attr, val)
