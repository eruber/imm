#!/usr/bin/env python
#coding=utf-8
"""
Constants
"""

__copyright__ = 'Copyright (C) 2014-2015 by E.R. Uber'
__author__    = 'E.R. Uber (eruber@gmail.com)'
__license__   = 'ISCL'
__version__   = '1.0.0'

#-------------------------------------------------------------------------------
import os
import os.path
import platform
import collections
import logging

#-------------------------------------------------------------------------------
APP_DIR = '.imm'
LOG_FILE = 'imm.log'

if platform.system().lower() == 'windows':
   path = os.environ['USERPROFILE']
elif platform.system().lower() == 'linux':
   path = os.environ['HOME']
elif platform.system().lower() == 'darwin':
   path = os.environ['HOME']
else:
   path = '.'

USER_HOME_PATH = path

APP_PATH = os.path.join(USER_HOME_PATH, APP_DIR)

LOG_PATH = os.path.join(os.path.join(USER_HOME_PATH, APP_DIR), LOG_FILE)

LOGGER = 'Image-Module-Maker(IMM)'
LOG_LVL_FILE = 'DEBUG'
LOG_LVL_CONSOLE = 'INFO'
LOG_ENCODING = 'utf8'
LOG_FILE_MODE = 'w'
LOG_FILE_FORMAT = '%(asctime)s:%(name)s:%(funcName)s-%(lineno)d:%(levelname)s - %(message)s'
LOG_CONSOLE_FORMAT = '%(name)s:%(levelname)s-%(lineno)d: %(message)s'
LOG_FILE_BACKUP_COUNT = 5

# https://pillow.readthedocs.org/handbook/image-file-formats.html#fully-supported-formats
# The Image (file) Extensions below are the most common supported by PILLOW
# The only formats tested so far are: png, gif, jpg, ico, tif/tiff, tga, xbm, ppm
IMG_EXTS = ['.png', '.pcx', '.ppm', '.gif', '.ico', '.jpg', '.jpeg', '.jfif', '.j2p', '.jpx', '.bmp', '.tif', '.tiff', '.tga', '.xbm']

LEGAL_PYTHON_IDENT = """
A legal Python identifier must adhere to the following syntax:

    1. Begin with a letter or an underscore
    2. Followed by a sequence of zero or more letters, digits, or underscores

Officially, the above two rules are specified as follows:

        identifier ::=  (letter|"_") (letter | digit | "_")*
"""

PYTHON_SPEC = "/usr/bin/env python"

#-------------------------------------------------------------------------------
FIXIDENT_NO_ARG = '<<NO-PREFIX>>'
DEFAULT_ENCODE = "utf-8"
DEFAULT_INDENT = 4 * ' '

#-------------------------------------------------------------------------------
# Help System -- see commandline module (I know, it should be in its own module)
# Special Help Topics
HT_TOPICS   = 'topics'
HT_ALL      = 'all'
HT_REDIRECT = 'redirect'
HT_USAGE    = 'usage'
HT_HELP     = 'help'  # This is an alias for HT_TOPICS

# Section Name Help Topics
HT_INTRO    = 'intro'
HT_CLI      = 'cli'
HT_EXAMPLES = 'examples'
HT_IMAGE    = 'image'
HT_CODE     = 'code'
HT_DEPEND   = 'depend'
HT_RETURN   = 'return'
HT_CREDIT   = 'credits'

HELP_TOPICS = collections.OrderedDict()

HELP_TOPICS[HT_INTRO]    = 'Introduction'

HELP_TOPICS[HT_USAGE]    = 'Command Line Usage (BRIEF)'
HELP_TOPICS[HT_CLI]      = 'Command Line Interface (FULL)'
HELP_TOPICS[HT_EXAMPLES] = 'Example Command Lines'
HELP_TOPICS[HT_IMAGE]    = 'Image File Names'
HELP_TOPICS[HT_CODE]     = 'Code Generation'
HELP_TOPICS[HT_DEPEND]   = 'Dependencies'
HELP_TOPICS[HT_CREDIT]   = 'Credits'
HELP_TOPICS[HT_RETURN]   = 'Return Codes'
HELP_TOPICS[HT_TOPICS]   = 'Emit this list of Help Topics'
HELP_TOPICS[HT_HELP]     = 'Emit this list of Help Topics'
HELP_TOPICS[HT_ALL]      = 'Paged User Manual'
HELP_TOPICS[HT_REDIRECT] = 'Unpaged User Manual (for file redirection)'

HELP_TOPIC_CHOICES = list()
for k in HELP_TOPICS.keys():
    HELP_TOPIC_CHOICES.append(k)

DEFAULTS_MSG = """Defaults:
          INPUT .
          PATH .
          MODULE images
          PREFIX None
          SPEC '#!/usr/bin/env python'
          ENCODING utf-8
"""

EMPTY = '<<empty>>'

#-------------------------------------------------------------------------------
if __name__ == "__main__":
    # visually inspect defined constants
    import constants as C

    print("Constants Defined:")
    attributes = dir(C)
    for attribute in attributes:
        if not attribute.startswith('__') and attribute.isupper():
            print("   %s = %s" % (attribute, getattr(C, attribute)))
