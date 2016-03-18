==================
Image Module Maker
==================

Image Module Maker (IMM) is both a Python library and a command line utility.

The IMM library facilitates converting image files into strings and embedding them in Python source code files
that can be utilized by graphical applications.

The IMM command line utility uses the IMM library to manage processing a directory of images and creating a Python 
module containing the directory's embedded images.

The Image Module Maker is licenced as free software under the ISC_ license.

Full documentation is available as part of the project as well as online at ReadTheDocs_.


Dependencies
------------

1. Pillow_ the friendly fork of the Python Imaging Library (PIL) is used to process image files

2. Python_ 3.3 or better 



Features
--------

* Converts image files into strings suitable for embedding in Python source code files
* Generates Python source code module containing embedded image data
* Ships with a command line utility for processing a directory of image files
* Optionally will generate code for a small Tk app, execute the app, and graphically show what the embedded images look like and allows image selection to emit image meta-data



.. _ISC: https://en.wikipedia.org/wiki/ISC_license
.. _ReadTheDocs: http://image-module-maker.readthedocs.org/en/latest/
.. _Python: https://www.python.org
.. _Pillow: http://python-pillow.org/

