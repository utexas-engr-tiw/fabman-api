.. _keyword arguments:

Keyword Arguments
=================

With few exceptions, all functions in the Fabman API library make use of keyword arguments to populate the request body. This is done to make the API more flexible and to allow for future extensions without breaking backwards compatibility. Moreover, the library does nothing to enforce the presence of required arguments, so it is up to the user to make sure that all required arguments are present.

Basic Parameters
----------------

We will use the members object to highlight how to use basic parameters. Assuming an authenticated :ref:`fabman` object, :code:`f`, we can fetch a list of members with filters:

.. code:: python

    f.get_members(q='Garak', limit=10, privileges='member')

.. _API documentation: https://fabman.io/api/v1/documentation#/members/getMembers

These parameters are passed as keyword arguments to the :code:`get_members` function. The :code:`q` parameter is a search query, :code:`limit` is the maximum number of results to return, and :code:`privileges` is a filter for the member's privileges, as defined in the `API documentation`_.

For many options, it is also possible to construct the request and pass it as a dictionary:

.. code:: python

    new_member = {
        'firstName': 'Kira',
        'lastName': 'Nerys',
        'emailAddress': 'first.officer@ds9.starfleet',
        'company': 'Bajoran Militia',
        'requiredUpFrontPayment': False,
        'billingFirstName': 'Benjamin',
        'billingLastName': 'Sisko',
        'billingCompany': 'Starfleet',
        'billingEmailAddress': 'financial@ds9.starfleet'
    }

    member = f.create_member(**new_member)

List Parameters
---------------

Certain Fabman API objects also take multi-valued parameters. Most notably, the embed parameter, which embeds additional information in the response. These can be passed to the calling function as a list, which is then processed by the :code:`requests` library:

.. code:: python

    f.get_members(q='Garak', limit=10, privileges='member', embed=['memberPackages', 'privileges'])

Note that if there is only one value, it can be passed as either a list or a string:

.. code:: python

        # These two calls are equivalent
        f.get_members(q='Garak', limit=10, privileges='member', embed='memberPackages')
        f.get_members(q='Garak', limit=10, privileges='member', embed=['memberPackages'])

