#!/usr/bin/env python
# # -*- coding: utf-8 -*-
"""
Generate source code for a Python Module that will import a generated image
data module and visually display it and allow user interaction to view the
image meta-data.

"""

__copyright__ = 'Copyright (C) 2014-2015 by E.R. Uber'
__author__    = 'E.R. Uber (eruber@gmail.com)'
__license__   = 'ISCL'
__version__   = '1.1.7'

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


#-------------------------------------------------------------------------------
SHOW_MODULE_NAME = "show"
SHOW_MODULE_FILE = SHOW_MODULE_NAME + ".py"


DIVIDER_TEMPLATE = "#" + 79*"-" + "\n"

NEW_LINE = "\n"

IMPORTS = """
import tkinter as tk
from tkinter import scrolledtext as st
from tkinter import StringVar

from PIL import Image, ImageTk

from pprint import pformat

#-------------------------------------------------------------------------------
import image_meta_data as META_DATA
"""

BODY_TOP = """
# See:
# http://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-grid-of-widgets-in-tkinter
# For the genesis of this module.

TEXT_WIDGET_LINES = 10
GEO_X = GEO_Y = 10

class Show():
    def __init__(self):
        self.root=tk.Tk()

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.wLimit = self.screen_width - 175
        self.hLimit = self.screen_height - 300

        # Right here we need to figure out the geometry based on the
        # number and size of the embedded icons
        self.root.geometry("+%d+%d" % (GEO_X, GEO_Y))

        self.widthCumulation = 20
        self.row = 0
        self.column = -1

        self.ImageLabelText = StringVar()
        self.ImageLabelText.set("Images...")

        self.TopFrame = tk.Frame(self.root)
        TLabel = tk.Label(self.TopFrame, textvariable=self.ImageLabelText).pack()

        self.canvas = tk.Canvas(self.TopFrame, borderwidth=0, width=self.wLimit, height=self.hLimit)
        self.vsframe = tk.Frame(self.canvas, width=self.wLimit, height=self.hLimit)
        self.vsb = tk.Scrollbar(self.TopFrame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.vsframe, anchor="nw",
                                  tags="self.vsframe")

        self.vsframe.bind("<Configure>", self.OnFrameConfigure)

        self.BottomFrame = tk.Frame(self.root, background="pink")
        BLabel = tk.Label(self.BottomFrame, text="Image Meta Data").pack()

        self.text = st.ScrolledText(self.root, wrap=tk.WORD, height=TEXT_WIDGET_LINES)
        self.text.pack(side=tk.BOTTOM, fill=tk.X, anchor=tk.W)

        self.TopFrame.pack(side=tk.TOP)
        self.BottomFrame.pack(side=tk.BOTTOM)

        self.buttons = list()


    def mainloop(self):
        self.root.mainloop()

"""

POPULATE_TOP = """
    def populate(self):
        '''Populate the vertically scrollable frame inside the canvas'''
        # self.<<IMAGEDATA>> = ImageTk.PhotoImage(data=IMG_DATA.<<IMAGEDATA>>)
        # <<IMAGEDATA>>Btn = tk.Button(self.vsframe, image=self.<<IMAGEDATA>>, command=lambda: self.callback(whatever))
        # self.calculateCoordinates(self.<<IMAGEDATA>>)
        # self.buttons.append(<<IMAGEDATA>>Btn, row=self.row, column=self.column)

"""

POPULATE_BOTTOM = """
        for button in self.buttons:
            button[0].grid(row=button[1], column=button[2])
"""

BODY_BOTTOM = """
    def calculateCoordinates(self, img, image_name):
        #print('IMG:', img)

        if META_DATA.IMG_META_DATA[image_name]['uniform_width']:
            if self.widthCumulation + img.width() > self.wLimit - 55:
                self.widthCumulation = img.width() + 5
                self.row += 1
                self.column = 0
            else:
                self.widthCumulation += img.width() + 5
                self.column += 1
        else:
            if self.widthCumulation + META_DATA.IMG_META_DATA[image_name]['largest_width'] > self.wLimit:
                self.widthCumulation = META_DATA.IMG_META_DATA[image_name]['largest_width']
                self.row += 1
                self.column = 0
            else:
                self.widthCumulation += META_DATA.IMG_META_DATA[image_name]['largest_width']
                self.column += 1

        #print('Width Cumulation: ', self.widthCumulation)
        #print('Row: ', self.row)
        #print('Col: ', self.column)

    def OnFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def callback(self, metadata_dict):
        text = pformat(metadata_dict, indent=4, width=1)
        index = '1.0'
        self.text.delete(index, tk.END)
        self.text.insert(index, text)

"""

MAIN_CODE = """if __name__ == "__main__":
    s = Show()
    s.populate()
    s.mainloop()
"""

#-------------------------------------------------------------------------------
class ShowGen():
    """
    """
    def __init__(self, logger, arg_namespace, caller_version=''):
        """
        """
        self._logr = logger.getChild('ShowGen')
        self._logr.info("Initializing Show Generator...")
        self._args = arg_namespace
        self._caller_version = caller_version

        self._module_path = self._args.code
        self._module_name = self._args.module
        self._encoding = self._args.encode
        self._python_spec = self._args.python
        self._main = self._args.main

        self._show_module_file = SHOW_MODULE_FILE
        self._show_module_abs_file = os.path.join(self._module_path, self._show_module_file)

        self._write_mode = "wb"


    def _genRuntimeIdentStr(self):
        """
        Returns a run-time identification comment string
        """
        self._logr.info("Generate Run Identification String...")
        user = getpass.getuser()

        run_time = dt.datetime.now().strftime('%Y-%b-%d at %H:%M:%S')
        caller   = os.path.basename(sys.argv[0]) + " " + self._caller_version
        codegen  = "showgenerator.py " + __version__

        ident  = "# This module was auto-generated...\n" + \
                 "#   By user: %s\n" % user  + \
                 "#        On: %s\n" % run_time + \
                 "#     Using: %s\n" % caller  + \
                 "#            %s\n" % codegen + \
                 "#    Python: %s\n" % platform.python_version() + \
                 "#        OS: %s\n" % platform.platform()

        return ident

    def Generator(self):
        """
        """
        self._logr.info("Generating the Show Module at '%s'..." % self._show_module_abs_file)

        # open show module for writing
        if os.path.exists(self._show_module_abs_file):
            self._logr.warning("Removing a previously generated Show Module File: '%s'" % self._show_module_abs_file)
            os.remove(self._show_module_abs_file)

        self._logr.info("Opening Show Module File (Python Module) '%s' with write mode '%s'" % (self._show_module_abs_file, self._write_mode))

        self._module_fp = open(self._show_module_abs_file, self._write_mode)


        self.genHeader()

        self.genBody()

        self.genMain()


        # close Show Module
        self._logr.info("Closing Output File... '%s'\n" % self._show_module_abs_file)
        if self._module_fp:
            self._module_fp.close()
            self._module_fp = None

        # now we call the module we just generated.
        self.executeShow()


    def genHeader(self):
        """
        """
        self._logr.info("Generating Show Module header...")

        self._logr.info("   Writing Python Spec...")
        pyspec=""
        if self._args.python:
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

        self._module_fp.write(bytes(IMPORTS.encode(self._encoding)))

        #import <<MODULE_NAME>> as IMG_DATA
        import_module = "import %s as IMG_DATA\n" % self._module_name
        self._module_fp.write(bytes(import_module.encode(self._encoding)))

        self._module_fp.write(bytes(NEW_LINE.encode(self._encoding)))
        self._module_fp.write(bytes(DIVIDER_TEMPLATE.encode(self._encoding)))

    def genBody(self):
        self._logr.info("Generating Show Module body...")

        # Need to add self._args.code to import search path so we can import it
        sys.path.insert(1, self._args.code)

        import image_meta_data as META_DATA

        self._module_fp.write(bytes(BODY_TOP.encode(self._encoding)))

        # Generate the code for the populate method
        self._module_fp.write(bytes(POPULATE_TOP.encode(self._encoding)))

        # self.<<IMAGEDATA>> = ImageTk.PhotoImage(data=IMG_DATA.<<IMAGEDATA>>)
        # <<IMAGEDATA>>Btn = tk.Button(self.vsframe, image=self.<<IMAGEDATA>>, command=lambda: self.callback('bi048', r'testdir\big_icons\basic_001_Img.png', '.png', 32, 32))
        # self.calculateCoordinates(self.<<IMAGEDATA>>)
        # self.buttons.append(<<IMAGEDATA>>Btn, row=self.row, column=self.column)

        lineC = "        image_count = 0\n"
        self._module_fp.write(bytes(lineC.encode(self._encoding)))

        for image_name in META_DATA.IMG_META_DATA:
            lines = list()

            line0 = "        image_count += 1"
            lines.append(line0)

            line1 = "        self.%s_Img = ImageTk.PhotoImage(data=IMG_DATA.%s_data)" % (image_name, image_name)
            lines.append(line1)

            line2 = "        self.calculateCoordinates(self.%s_Img, '%s')" % (image_name, image_name)
            lines.append(line2)

            line3 = "        META_DATA.IMG_META_DATA['%s']['row'] = self.row" % image_name
            lines.append(line3)
            line4 = "        META_DATA.IMG_META_DATA['%s']['col'] = self.column" % image_name
            lines.append(line4)
            line5 = "        META_DATA.IMG_META_DATA['%s']['imagecount'] = image_count" % image_name
            lines.append(line5)

            line6 = "        %sBtn = tk.Button(self.vsframe, image=self.%s_Img, command=lambda: self.callback(META_DATA.IMG_META_DATA['%s']))" % (image_name, image_name, image_name)
            lines.append(line6)

            line7 = "        self.buttons.append((%sBtn, self.row, self.column))\n" % image_name
            lines.append(line7)

            for line in lines:
                line += '\n'
                self._module_fp.write(bytes(line.encode(self._encoding)))

        # self.ImageLabelText.set("Images... [%d]" % image_count)
        ImgCountLabel = "'Images... [%d]' % image_count"
        labelCode = "        self.ImageLabelText.set(%s)\n" % ImgCountLabel
        self._module_fp.write(bytes(labelCode.encode(self._encoding)))

        self._module_fp.write(bytes(POPULATE_BOTTOM.encode(self._encoding)))

        self._module_fp.write(bytes(BODY_BOTTOM.encode(self._encoding)))


    def genMain(self):
        self._logr.info("Generating Show Module main...")

        self._module_fp.write(bytes(NEW_LINE.encode(self._encoding)))
        self._module_fp.write(bytes(DIVIDER_TEMPLATE.encode(self._encoding)))
        self._module_fp.write(bytes(MAIN_CODE.encode(self._encoding)))

    def executeShow(self):
        """
        """
        self._logr.info("Attempting to execute the generated Show Module...")

        # For now we are taking the easy way out on this which will
        # block until we return. Using the subprocess module would be
        # more elegant, but this is just a utility after all...
        cmd = 'python %s' % self._show_module_abs_file
        self._logr.info("Blocking Run of: '%s'" % cmd)
        # Assumes python is in the execution path
        os.system(cmd)


if __name__ == "__main__":
    pass
