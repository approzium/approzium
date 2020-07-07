.. Approzium SDK documentation master file, created by
   sphinx-quickstart on Thu Jun 25 20:59:53 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Approzium Python SDK's documentation!
================================================

This is the Python SDK for Approzium_ (identity-based credential-less authentication to databases). Currently, there is support for Psycopg2 and Asyncpg (both for Postgres) as database drivers, but support for more database drivers is planned. Check out our roadmap_ for more details.

Approzium Python SDK is implemented as thin wrappers that integrate with existing Python database drivers, resulting in being extremely easy to use. It creates the same database connection objects that you are using, so you don't have to change your existing code!

Currently, it supports Python 3.5+ and AWS-based identity.

.. _Approzium: https://approzium.org/
.. _roadmap: https://approzium.org/src-pages-roadmap


API Documentation
=================

.. toctree::
   :maxdepth: 2

   approzium


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
