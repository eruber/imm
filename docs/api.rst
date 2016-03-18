======================
Image Module Maker API
======================

.. _api-reference-label:

.. automodule:: imm.imagedata
    :members:

Logging
-------

The IMM library utilizes the Python Standard Library's logging module. 

A child logger descended from the root logger is intialized and a null logging handler is added so that if the code utilizing the IMM library does not configure logging, any logging message will be handled by the null logging handler.

For more details see `Configuring Logging for a Library <https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library>`_
from the Python Standard Library documentation.
