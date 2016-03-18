#!/usr/bin/env python
# # -*- coding: utf-8 -*-
"""
codegenerator.py

Generate source code for a Python Module containing strings of binary image data
and optionally generate a separate Python Module containing the image meta-data.

"""

__copyright__ = 'Copyright (C) 2014-2015 by E.R. Uber'
__author__    = 'E.R. Uber (eruber@gmail.com)'
__license__   = 'ISCL'
__version__   = '2.1.0'

#-------------------------------------------------------------------------------
import sys
import os
import os.path
import platform
import logging
import getpass
import datetime as dt

from pprint import pformat

#-------------------------------------------------------------------------------
from PIL import Image, ImageTk

#-------------------------------------------------------------------------------
from imm.cli import constants as C
from imm import imagedata as GID
#-------------------------------------------------------------------------------
PYTHON_SPEC = "/usr/bin/env python"

DIVIDER_TEMPLATE = "#" + 79*"-" + "\n"

NEW_LINE = "\n"

MAIN_EMPTY_TEMPLATE = """if __name__ == "__main__":
    pass
"""

META_DATA_MODULE_FILE = "image_meta_data.py"


#-------------------------------------------------------------------------------
class CodeGen():
    """
    logger - a logging module logger object created by the caller

    This code generator supports:
        - generating a single Python module with multiple image data references
     or
        - generating multiple Python modules each containing a single image data reference.

    If module_name is None, then we are generating multiple Python modules;
    otherwise, we are generating a single Python module.

    caller_version - the version of the caller used to write a header in generated code

    empty_main - True generates an empty __main__. False is the default and
    by default a __main__ is also generated that will display a small application
    that displays each image on a button and displays some meta-data when a
    button is pressed.

    """
    def __init__(self, logger, arg_namespace, caller_version=''):
        """
        The modes are derived as follows from self._args = arg_namespace:
            args.module - if none, append defines module name
            args.code - we always have path
            args.append - module name if appending

        """
        self._logr = logger.getChild(__name__)
        self._logr.info("Initializing Code Generator...")
        self._args = arg_namespace
        self._caller_version = caller_version

        self._module_path = self._args.code
        self._encoding = self._args.encode
        self._python_spec = self._args.python
        self._main = self._args.main
        self._show = self._args.show

        self._largest_width = 0
        self._uniform_width = None  # Set this to True or False

        if self._args.append:
            # Appending to an EXISTING MODULE
            self._module_name = self._args.append
            self._write_mode = "ab"
        else:
            # Writing a NEW MODULE
            self._module_name = self._args.module
            self._write_mode = "wb"

        self._module_fp = None
        self._CurrentImageName = None
        self._CurrentImagePath = None

        self._imageMetaData = dict()


        self.genOpenModule()

    def _genRuntimeIdentStr(self):
        """
        Returns a run-time identification comment string
        """
        self._logr.info("Generate Run Identification String...")
        user = getpass.getuser()

        run_time = dt.datetime.now().strftime('%Y-%b-%d at %H:%M:%S')
        caller   = os.path.basename(sys.argv[0]) + " " + self._caller_version
        codegen  = "codegenerator.py " + __version__

        ident  = "# This module was auto-generated...\n" + \
                 "#   By user: %s\n" % user  + \
                 "#        On: %s\n" % run_time + \
                 "#     Using: %s\n" % caller  + \
                 "#            %s\n" % codegen + \
                 "#    Python: %s\n" % platform.python_version() + \
                 "#        OS: %s\n" % platform.platform()

        return ident


    def processImage(self, image_name, image_file_path, image_type):
        """
        Makes sure image name is unique and not been used before. The image name
        is used as the image data reference in the generated source file.

        Reads the image data from the image_file_path.
        """
        self._logr.info("Processing image '%s'.\n" % image_name)

        self._CurrentImageName = image_name.lower()
        self._CurrentImageType = image_type.lower()
        self._CurrentImagePath = image_file_path

        ####################### Using IMM Library ###########################
        with GID.Generator(self._module_fp, self._write_mode) as gfxModule:
            # image_file_path will be changed if the original image_file_path
            # input is not a png file
            gfxModule.write(image_file_path, image_name)
        #####################################################################

        img = Image.open(image_file_path)

        # populate image info dictionary to be returned
        (w, h) = img.size

        if w > self._largest_width:
            self._largest_width = w

        self._logr.info(" %s Size -- Width: %d  Height: %d"  % (image_type, w, h))

        self._imageMetaData[self._CurrentImageName] = {
            'FilePath' : self._CurrentImagePath,
            'ImgType'  : self._CurrentImageType,
            'Width'    : w,
            'Height'   : h,
        }

        self._logr.info("Read image data from file '%s'" % image_file_path)


    @property
    def CurrentImageName(self):
        return self._CurrentImageName


    def genOpenModule(self):
        self._module_abs_path = os.path.join(self._module_path, self._module_name+'.py')

        if os.path.exists(self._module_abs_path):
            self._logr.warning("Removing a previously generated Image Data Module File: '%s'" % self._module_abs_path)
            os.remove(self._module_abs_path)

        self._logr.info("Opening for output the Image Data Module File (Python Module) '%s' with write mode '%s'" % (self._module_abs_path, self._write_mode))

        self._module_fp = open(self._module_abs_path, self._write_mode)


    def genModuleHeader(self):
        """
        Write the Module Header to the MODULE file.

        The Header is empty be default. The following args affect Writing of the
        module header:
            --python
            --main

        """
        self._logr.info("Generating Module Header...")

        if self._args.python:
            self._logr.info("   Writing Python Spec...")
            pyspec = self._args.python + "\n"
            self._module_fp.write(bytes(pyspec.encode(self._encoding)))

        #coding=utf-8
        self._logr.info("   Writing encoding for modern editors...")
        encoding = "#" + self._args.encode + "\n"
        self._module_fp.write(bytes(encoding.encode(self._encoding)))

        self._module_fp.write(bytes(DIVIDER_TEMPLATE.encode(self._encoding)))

        ident = self._genRuntimeIdentStr()
        self._logr.info("   Writing runtime ident:\n%s" % ident)
        self._module_fp.write(bytes(ident.encode(self._encoding)))

        self._module_fp.write(bytes(DIVIDER_TEMPLATE.encode(self._encoding)))
        self._module_fp.write(bytes(NEW_LINE.encode(self._encoding)))


    def genImageData(self):
        """
        Inputs: 
                self._CurrentImageName : image name
                self._CurrentImageData : image data
                self._module_fp : image source code module file opened for writing

        Write the image data to the image module source file.
        """
        self._logr.info("Generating Image Data...")

        dataRef = "%s_data = " % self._CurrentImageName
        self._module_fp.write(bytes(dataRef.encode(self._encoding)))
        self._module_fp.write(bytes(repr(self._CurrentImageData).encode(self._encoding)))
        self._module_fp.write(bytes(NEW_LINE.encode(self._encoding)))


    def genModuleMain(self):
        """
        Generate the image source code module's "main" section.
        """
        self._logr.info("Generating Module __main__...")

        if self._args.main:
            self._logr.info("   *** Main is NOT empty. ***")
            self._module_fp.write(bytes(NEW_LINE.encode(self._encoding)))
            self._module_fp.write(bytes(DIVIDER_TEMPLATE.encode(self._encoding)))
            self._module_fp.write(bytes(MAIN_EMPTY_TEMPLATE.encode(self._encoding)))
        else:
            self._logr.info("   *** Main is empty. ***")


    def genClosure(self):
        """
        Close the image source code module file object.

        """
        self._logr.info("Closing Output File... '%s'\n" % self._module_abs_path)
        if self._module_fp:
            self._module_fp.close()
            self._module_fp = None
            

    #---------------------------------------------------------------------------
    # meta-data generation methods
    #---------------------------------------------------------------------------
    def genImageMetaData(self):
        """
        Open the meta-data file, write the meta-data dictionary, and close file
        """
        self._logr.info("Generating image metadata...")

        metadata_module_abs_path = os.path.join(self._module_path, META_DATA_MODULE_FILE)

        if os.path.exists(metadata_module_abs_path):
            self._logr.warning("Removing a previously generated Image Meta-data File: '%s'" % metadata_module_abs_path)
            os.remove(metadata_module_abs_path)

        write_mode = "wb"
        self._logr.info("Opening Image Meta-data File (Python Module) '%s' with write mode '%s'" % (metadata_module_abs_path, write_mode))

        if self._module_fp:
            self._logr.fatal("File Refernce should not be defined!!! Cannot be re-used at this time.")
            sys.exit(7)

        self._module_fp = open(metadata_module_abs_path, write_mode)

        count = 0
        uniform_count = 0
        for img in self._imageMetaData:
            count += 1
            self._imageMetaData[img]['largest_width'] = self._largest_width

            if self._imageMetaData[img]['Width'] == self._largest_width:
                uniform_count += 1

        if uniform_count == count:
            self._uniform_width = True
        else:
            self._uniform_width = False

        for img in self._imageMetaData:
            self._imageMetaData[img]['uniform_width'] = self._uniform_width

        meta_data = pformat(self._imageMetaData, indent=4, width=1)

        self.genModuleHeader()

        self._module_fp.write(bytes("IMG_META_DATA = \\\n".encode(self._encoding)))
        self._module_fp.write(bytes(meta_data.encode(self._encoding)))

        # We want an empty main in the meta-data module
        if not self._args.main:
            save_main = self._args.main
            self._args.main = True
            self.genModuleMain()
            self._args.main = save_main

        if self._module_fp:
            self._module_fp.close()


#-------------------------------------------------------------------------------
def test():
    """ Unit Tests """
    pass


#-------------------------------------------------------------------------------
if __name__ == "__main__":
    test()
