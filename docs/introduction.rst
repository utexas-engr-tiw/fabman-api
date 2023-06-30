.. _introduction:

Introduction
============

This python package provides a simple wrapper interface around the Fabman API endpoints and response objects. It is intended to be used by Fabman customers to integrate their own software with their Fabman accounts. While this library provides an interface, familiarity of the Fabman API is assumed. You can read more about the Fabman API at https://github.com/FabmanHQ/fabman-api and interact with the live documentation at https://fabman.io/api/v1/documentation.

.. _Canvas Python API: https://fabman.io/api/v1/documentation#/members/getMembers

This library was originally designed for a sync process with Canvas LMS. As a result, the design choices are heavily influenced by the choices made by the `Canvas Python API`_. Most of the :ref:`internal_classes` were either copied or adapted from the Canvas Python API.