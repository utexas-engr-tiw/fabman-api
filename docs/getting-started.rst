.. _getting_started:

Getting Started
===============

Installing Fabman API
---------------------

You can install Fabman API using pip:

.. code::

    pip install fabman

To install the latest development version, use:

.. code::

    pip install git+https://github.com/utexas-engr-tiw/fabman-api.git

Usage
-----

To begin using the Fabman API wrappers, you must first instantiate a new Fabman object:

.. code:: python

    # Import the Fabman class
    from fabman import Fabman

    # Define your API key:
    API_KEY = "abcdef-123456"

    # Instantiate a new Fabman object:
    f = Fabman(API_KEY)

Working with Fabman objects
---------------------------

With a few notable exceptions, Fabman API objects are returned as Python Objects. For example, when requesting details of a Member given their id, the Fabman API library will return a :code:`Member` object. The exception to this rule is when returned object does not have any associated endpoints. In this case, the raw JSON response is returned as either a Python list or Dictionary. Future revisions of this library will define classes for these instances

Get a Member by ID
~~~~~~~~~~~~~~~~~~

Members of your Makerspace can be retrieved from the api:

.. code:: python

    >>> member = f.get_member(12345)
    >>> print(member.firstName, member.lastName)
    'Julian Bashear'

    # Update the member's details
    >>> member.update(firstName="Elim", lastName="Garak"
    >>> print(member.firstName, member.lastName)
    'Elim Garak'

See the documentation on :ref:`keyword arguments` for more information on how the :code:`update` method handles arguments.

Paginated Lists
~~~~~~~~~~~~~~~

When requesting an endpoint which holds many objects, the Fabman API will return a paginated list of objects. The paginated list automatically handles requesting new pages of objects from the Fabman API endpoint, and provides the familiar interface of a :code:`list` object for interacting with the objects.

.. code:: python

    >>> members = f.get_members(limit=2)
    >>> for member in members:
    >>>    print(member.firstName, member.lastName)
    'Julian Bashear'
    'Elim Garak'
    'Benjamin Sisko'
    'Kira Nerys'
    ...

Note that you don't need to explicitly request the new page will automatically be requested and filled in.



    


