.. _troubleshooting:

Troubleshooting
===============

If you have any problems with or questions about this library, please contact us on our issues board and we will be happy to help! Note that our use case does not require all endpoints in this library so you may run into issues with some endpoints that we have not explored. There are, however, some easy things to check before making an issue.

Parameters
~~~~~~~~~~

All parameters for endpoints are passed as keyword arguments. If you are trying to send a dictionary as an argument to any of the functions you will need to unpack it first. Please refer to the :ref:`keyword arguments` section for more information. 

Valid parameters for the Fabman API are case sensitive and use the camelCase naming convention. A good rule of thumb is that any camelCase paramter or attribute are from the API, where as anything with the underscore naming convention is from this library.

Permissions
~~~~~~~~~~~

Depending on your account, you may not have access to all endpoints. Note that many of the endpoints in this library require admin permissions of an account. There are other endpoints which require superuser permissions, which is highly unlikely you have. Most of the superuser endpoints are not covered by this library since they are for internal Fabman use.