#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The imagedata module handles reading images, perhaps converting images, and writing image data to a text file.
Typically a text file that is a Python module.

"""

__author__  = 'E.R. Uber'
__email__   = 'eruber@gmail.com'
__license__ = 'ISCL'
__version__ = '2.1.0'

#----------------------------------------------------------------------------------------
import os
import sys
import logging
from io import BytesIO
import re
import random
import string

#----------------------------------------------------------------------------------------
from logging import NullHandler
from datetime import datetime as dt

#----------------------------------------------------------------------------------------
from PIL import Image, ImageTk

#----------------------------------------------------------------------------------------
APPEND_MODE = 'APPEND'
WRITE_MODE  = 'WRITE'

WRITE_MODE_NAMES = ( WRITE_MODE, APPEND_MODE)

WRITE_MODES = ('wb', 'ab')

WRITE_MODE_MAP = { 
                    WRITE_MODE_NAMES[0] : WRITE_MODES[0],
                    WRITE_MODE_NAMES[1] : WRITE_MODES[1]
                  }

NEW_LINE = '\n'

#----------------------------------------------------------------------------------------
def make_string_valid_python_identifier(s):
    """
    Modify the input string, s, until we can return a valid Python identifier.

    The process is as follows:

        1. Replace all spaces and dashes with underscores
        2. Remove any invalid Python identifier characters 
           (any char that is not 0-9, a-z, A-Z, or underscore)
        3. If an empty identifier remains, generate a random identifier
        4. If the identifier begins with a digit, prefix an underscore
        5. If the identifier begins with an underscore, prefix the string 'image'
    
    """

    # Replace all spaces and dashes with underscores
    variableName = s.replace(' ', '_')
    variableName = s.replace('-', '_')

    # Remove non-python identifier characters
    # See: http://stackoverflow.com/questions/3303312/how-do-i-convert-a-string-to-a-valid-variable-name-in-python
    
    # Remove invalid characters -- any character that is not a number, letter, or underscore
    variableName = re.sub('[^0-9a-zA-Z_]', '', variableName)

    if len(variableName) == 0:
        # create a random name
        variableName = '_' + id_generator()

    if variableName[0].isdigit():
        variableName = '_' + variableName
        
    if variableName.startswith('_'):
        variableName = 'image' + variableName

    return(variableName)


#----------------------------------------------------------------------------------------
def id_generator(size=7, chars=string.ascii_lowercase + string.digits):
    """
    Returns a random python identifier that is size characters in length and composed of
    characters from the set of chars.
    """
    # See: http://pythontips.com/2013/07/28/generating-a-random-string/
    # See: http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
    id = ''.join(random.choice(chars) for x in range(size))
    return(id)


#----------------------------------------------------------------------------------------
class IllegalFileIOWriteModeError(Exception):
    pass


#---------------------------------------------------------------------------------------- 
class Generator(object):
    """
    This class implements a context manager for opening, or using a previouisly opened,
    Python module text file and writing image data to it.

    :param output: Can be a string naming the output text file to be created or it can be an already opened output
                   file object. If not specificed, a string is assumed and the default value is "gfxmodule.py".
    :param writemode: A string defining the write mode. Legal values are 'WRITE' and 'APPEND', the default is 'WRITE'.
    :param encoding: A string defining the write encoding of the output. Defaults to 'utf-8',

    Note that if the output parameter represents an already opened output file object, then this
    context manager does not own the output file object resource and will therefore not close it
    upon exiting the context manager's with statement code block.
    
    """
    def __init__(self, output='gfxmodule.py', writemode=WRITE_MODE_NAMES[0], encoding='utf-8'):
        # Get a logger descended from the root logger, which is found by logger.getLogger()
        self._logr = logging.getLogger().getChild(__name__)

        # This library is using a null handler so that if the user does not have logging configured,
        # the default behavior of WARNING or above being printed to sys.stderr does not happen.
        # See: https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
        self._logr.addHandler(logging.NullHandler())

        if hasattr(output, "read"):
            self._logr.info("Output already opened by user, not owned by this context")
            # output is an already opened file object
            self._output_file_stream = output
            self._output_file = "<ALREADY OPENED BY USER>"
            # This context does NOT own the output file stream so
            # it should not close it
            self._close_on_context_exit = False
        else:
            self._logr.info("Output will be owned by this context")
            # output is a string naming a file to be opened
            self._output_file_stream = None
            self._output_file = output
            self._close_on_context_exit = True

        if writemode in WRITE_MODES:
            self._write_mode = writemode
        elif writemode in WRITE_MODE_NAMES:
            self._write_mode = WRITE_MODE_MAP[writemode]
        else:
            raise IllegalFileIOWriteModeError("Input parameter 'writemode' should be one of %s, but is %s" % (WRITE_MODE_NAMES, writemode))

        self._image_file = None
        self._image_var_name = None

        self._encoding = encoding

    
    def __enter__(self):
        """
        The enter method to make this class a context manager.
        """
        return(self)


    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        The exit method to make this class a context manager.
        """
        if self._close_on_context_exit:
            # This context manager owns this context's resource, so we can close it
            self._logr.debug("Attempting to close the output stream")
            self.close()


    def write(self, imagefile, imagevarname=None):
        """
        This method writes the image data read from imagefile to the output Python module text file.

        :param imagefile: A string specifying the image file name to read.
        :param imagevarname: A string specifying the image data's variable name.

        If imagefile is NOT a .png file, then it will be converted in memory to a PNG image
        before being written to the output Python module text file.

        If imagevarname is NOT specified, then a legal Python variable name will be derived
        from the imagefile name. If no legal Python identifier can be derived from the image
        file name, the a random identifer will be generated.
        """
        self._image_file = os.path.abspath(imagefile)
        self._image_var_name = imagevarname

        if self._image_var_name is None:
            # If no image variable name is specified, we do our best to derive one from the
            # image file name
            path, filename_with_ext = os.path.split(self._image_file)
            filename_with_no_ext, ext = os.path.splitext(filename_with_ext)

            self._image_var_name = make_string_valid_python_identifier(filename_with_no_ext)

        if self._output_file_stream is None:
            try:
                self._logr.debug("Opening output file '%s' write stream in mode '%s'" % (self._output_file, self._write_mode))
                self._output_file_stream = open(self._output_file, self._write_mode)
            except (OSError, IOError) as e:
                self._logr.exception(e)
                raise 

        imageBuf = BytesIO()

        try:
            self._logr.debug("Reading image file '%s' with PIL.Image.open()" % self._image_file)
            img = Image.open(self._image_file)

            # Save the opened image to an in memory bytes buffer as a PNG image
            self._logr.debug("Saving image object in PNG format to a bytes buffer in memory.")
            img.save(imageBuf, 'PNG')
           
            # image data to write to module text file
            self._image_data = imageBuf.getvalue()

            self._image_var_name = "%s_data" % self._image_var_name.lower()
            self._logr.info("Writing image data as variable '%s' to output file '%s'" % (self._image_var_name, self._output_file))
            dataRef = "%s = " % self._image_var_name

            self._output_file_stream.write(bytes(dataRef.encode(self._encoding)))
            self._output_file_stream.write(bytes(repr(self._image_data).encode(self._encoding)))
            self._output_file_stream.write(bytes(NEW_LINE.encode(self._encoding)))

        except Exception as e:
            self._logr.exception(e)
            raise

        finally:
            imageBuf.close()


    def close(self):
        """
        Close the output write stream.

        If imm.imagedata.Generator() is used has a context manager, this close() method will be called
        automatically if necessary upon exit of the context's with block.

        """
        if self._output_file_stream:
            self._output_file_stream.close()
            self._output_file_stream = None
            self._logr.debug("Closed output file '%s' write stream" % self._output_file)
        else:
            self._logr.debug("The output file '%s' write stream is ALREADY CLOSED" % self._output_file)


if __name__ == "__main__":
    pass    
