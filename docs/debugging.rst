.. _debugging:

Debugging
=========

There are always times where things are not going the way we think they should. Whenever you are having problems with your code, it is important to be able to debug it. You may have simply put a typo into your parameter name, or there is a deep uncaught bug in this library. Either way, you will need to be able to debug how your code is interacting with the Fabman API. 

Since all calls in this library go through the :ref:`Requester` class, debug logging has been added in at that point. You can access this logging in your own code using the standard Python :py:mod:`logging` module. Accessing these logs will make debugging much easier. 

A simple example of how to enable logging is shown below.

.. code-block:: python

    import logging
    import sys

    logger = logging.getLogger("canvasapi")
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

Once this has been configured, any logging debug or info message will be redirected to the :code:`sys.stdout`. This debugging and info can also be sent to a file for later review after being added to a process. **Note that this is a potential security issue** depending on your use of the library. While we have ensured that *your* api key will be scrubbed before it hits the logger, there are API methods which can return api keys and other sensitive information that will be included in the logging. 