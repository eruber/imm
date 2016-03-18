#!/usr/bin/env python
#coding=utf-8
#-------------------------------------------------------------------------------
# immcli.py
#
# Image Module Maker Command Line Interface
#
# Create a Python module of embedded images from a directory of image files.
#_______________________________________________________________________________

"""
INTRODUCITON
------------
Image Module Maker (IMM) is a utility that will parse a directory of image files
and create a Python source code module that embeds each image file's binary data
into a string that is suitable to be imported by Python application code.

There is a use case that allows a single image file to be named rather than a
directory of images.

An option exists to append to an existing module rather than create a new module.

See the section below titled EXAMPLES OF COMMAND LINES for further details
regarding the most commonly used command line interface options.

By default Image Module Maker just writes the bare image data to the module file;
however, their are several command line options to further dress-up the generated
module code and even generate ancillary modules that support visual confirmation
of the embedded image data. For further details, see the section below titled
CODE GENERATION.

Not all image file names can be translated to Python identifier names without
some further command line options. See the section below titled IMAGE FILE NAMES
for more details.

Options also exist for appending image data to an existing Python module file.
See the section titled COMMAND LINE INTERFACE for more detail.

The full user manual can be emitted to stdout by invoking Image Module Maker as:

    python immcli.py --help all

The less verbose command line usage is available via:

    python immcli.py --help

or just simply:

    python immcli.py


COMMAND LINE INTERFACE
----------------------
<<AUTO-INSERT-CLI-USAGE-HERE>> (Command Line Usage inserted here at runtime)

Regarding execution on Windows, the batch file imm.bat allows immcli.py to be
invoked simply as:

    imm [OPTIONS]

rather than

    python immcli.py [OPTIONS]

or even as

   immcli.py

assuming PATHEXT is configured properly.

See the comments in the imm.bat file for all the gory details.


EXAMPLES OF COMMAND LINES
-------------------------
Use Case #1 - A Directory of Images to be Processed

    imm --input gfx --module icons

    This command line will scan the directory 'gfx' and creates a Python module
    file named 'icons.py' in the current directory containing referenced strings
    of the image data from the image files found in the 'gfx' directory.

Use Case #2 - A Single Image File to be Processed

    imm --input file.png --module image

    This command encodes the binary image data from the image file 'file.png'
    into the Python module file named 'image.py' that will be created in the
    current directory.

If the --module option is not specified, the default MODULE name used is 'gfxmodule'.

If the Python module needs to be created in another location other than the
current directory, then specify:

    --code CODE_PATH

where CODE_PATH is the directory in which the Python module should be created. 
If CODE_PATH does not exist, it will be created.

If the MODULE already exists, it can be appended to by using the

    --append MODULE

option rather than the

    --module MODULE

option.


IMAGE FILE NAMES
----------------
This utility attempts to use image file names as Python identifiers. 

However, a legal file name can specify an ILLEGAL Python identifier. So it is 
important to insure that all image files processed by this utility have file 
names that reduce to legal Python identifiers when the file name extension 
is removed.

A legal Python identifier must adhere to the following syntax:

    1. Begin with a letter or an underscore
    2. Followed by a sequence of zero or more letters, digits, or underscores

Officially, the above two rules are specified as follows:

        identifier ::=  (letter|"_") (letter | digit | "_")*

So if an image file name begins with a character that is not a letter or an
underscore, it represents a illegal Python identifier.

If this utility finds an image file name that represents an illegal Python
identifier, it will terminate with a fatal error... unless...

... the option --fixident PREFIX is used to append the PREFIX string to the
image file name. Of course PREFIX itself should be a legal Python identifier.

If --fixident PREFIX is specified, then the following other problematic fix-ups
will be done automatically:

    1. All spaces will be translated to underscores
    2. All dashes will be translated to underscores

Note that --fixident may be specified WITHOUT a PREFIX. In this case only the
default prefix 'gfx' will be used.


CODE GENERATION
---------------
By default IMM just writes the image data. Options can be used to dress-up the
file generated and/or allow visual inspection of the image data embedded in
the Python MODULE generated:

  --python [SPEC]      Default is to not generate a "#!" line as the first line of
                       MODULE. If no SPEC is specifed, default is:

                                "#!/usr/bin/env python"

                       If SPEC is specified, first line of MODULE will be:

                                #!SPEC

                       No validation is done on SPEC.

  --encode [ENCODING]  Default ENCODING is "utf-8". If ENCODING is specified,
                       it will be used with no validation.

  --main               Default is to not generate a __main__ if statment.
                       If this option is specified, the following __main__
                       if statement will be generated:

                            if __name__ == "__main__":
                                pass

  --show               Default is to just generate MODULE. If this option is
                       specified two more Python Module files will be generated
                       in CODE_PATH:

                            show.py
                            image_meta_data.py

                       Once generated, the show module will also be executed to
                       display a Graphical User Interface that allows:

                          a) visual confirmation of the image data in MODULE
                          b) user interaction with buttons of the image data
                             which displays image meta-data

DEPENDENCIES
------------
The Image Module Maker has been tested with Python 3.4 and 3.5.

No effort has yet been expended to test it under any other versions of Python.

The Python Imaging Library Pillow is required to convert non-PNG image formats
to PNG. The versions of Pillow used for testing were:

    https://pypi.python.org/pypi/Pillow/2.6.1
    https://pypi.python.org/pypi/Pillow/3.1.1


RETURN CODES
------------
This utility exits with the following return codes:

    0 - Successfully executed with no known errors
    1 - The option --input specifies an argument that does not exist
    2 - The option --input specifies an argument that is not a directory nor a file
    3 - NOT CURRENTLY USED
    4 - The option --module or --append does not specify a legal Python module name.
    5 - One or more image files have file names that cannot be legal Python identifiers
        and the --fixident option was not specified
    6 - The option --input specifies nothing that leads to recognizeable image file(s)
    7 - Mis-use file object in codegenerator.py (left open; should be closed for re-use)
    8 - Unable to create --code CODE_PATH


CREDITS
-------
A forked version of python-pager by techtonik on BitBucket is included in this
release to provide console terminal paging control that displays the number of
pages yet to view. The orginal project is at:

    https://bitbucket.org/techtonik/python-pager

The forked project is at:

    https://bitbucket.org/eruber/python-pager

To the developers of Pillow (https://github.com/python-pillow/Pillow) -- thanks for 
making such great a package.

And, of course, to all the knowledgeable individuals who frequent StackOverflow and
answer Python questions are a continual source of guidance.
"""

__version__="2.1.00"
__author__="eruber@gmail.com"

#-------------------------------------------------------------------------------
# From the Python Standard Library
#-------------------------------------------------------------------------------
import os
import os.path
import sys
import platform
import pprint
import re


#-------------------------------------------------------------------------------
# Local imports -- see the immlib & immcli directories
#-------------------------------------------------------------------------------
from imm.cli import constants as C
from imm.cli import loggingsetup
from imm.cli import commandline as Cli
from imm.cli import utils
from imm.cli import pager
from imm.cli import showgenerator as Sg
from imm.cli import codegenerator as Cg

from imm import imagedata

#-------------------------------------------------------------------------------
# identifier ::=  (letter|"_") (letter | digit | "_")*
# [^\d\W] matches a character that is not a digit and
# not "not alphanumeric" which translates to
# "a character that is a letter or underscore"
# \Z matches only the end of a string.
# \w matches unicode word characters
# See: http://stackoverflow.com/questions/5474008/regular-expression-to-confirm-whether-a-string-is-a-valid-identifier-in-python
pythonIdentifier = re.compile(r"^[^\d\W]\w*\Z", re.UNICODE)

#-------------------------------------------------------------------------------
def main():
    if not os.path.exists(C.APP_PATH):
        os.makedirs(C.APP_PATH, exist_ok=True)

    logSubSystem = loggingsetup.Setup(C.LOGGER)
    logger = logSubSystem.Logger()

    platformdata = platform.platform() + " using Python " + platform.python_version()
    IDENT = os.path.basename(sys.argv[0]) + " " + __version__ + " running on " + platformdata
    
    #---------------------------------------------------------------------------
    # See imm.cli/commandline.py
    (args, cliparser) = Cli.parseCmdLine(__version__)

    if len(sys.argv) < 2:
        print(IDENT, '\n')
        cliparser.print_usage()
        print("\nwhere HELP_TOPIC can be one of the following:")
        for ht in C.HELP_TOPICS.keys():
            print("   {0:9s} : {1}".format(ht, C.HELP_TOPICS[ht]))
        sys.exit(0)

    #------------------------ HELP OPTIONS -------------------------------------
    if args.help:
        # Let cliparser know about the terminal width for help output
        os.environ['COLUMNS'] = str(pager.getwidth())
        os.system('cls' if os.name == 'nt' else 'clear')

        # --help
        if args.help == C.EMPTY:
            hlines = cliparser.format_usage().split('\n')
            hlines.insert(0, IDENT)
            for l in C.DEFAULTS_MSG.split('\n'):
                hlines.append(l)
            for l in Cli.help_topics():
                hlines.append('  ' + l)
            hlines.append('\n')
            pager.page(hlines)

        # --help usage
        elif re.match(args.help, C.HT_USAGE):
            hlines = cliparser.format_usage().split('\n')
            hlines.insert(0, IDENT)
            pager.page(hlines)

        # --help help  or  --help topics
        elif re.match(args.help, C.HT_HELP) or re.match(args.help, C.HT_TOPICS):
            hlines = Cli.help_topics()
            hlines.insert(0, IDENT)
            hlines.insert(1, ' ')
            pager.page(hlines)

        # --help cli
        elif re.match(args.help, C.HT_CLI):
            hlines = cliparser.format_help().split('\n')
            hlines.insert(0, IDENT)
            pager.page(hlines)

        # --help all
        elif re.match(args.help, C.HT_ALL):
            pager.page(Cli.usage("Full User Manual", cliparser, __version__))

        # --help redirect
        elif re.match(args.help, C.HT_REDIRECT):
            manual = '\n'.join(Cli.usage("Full User Manual", cliparser, __version__))
            print(manual)

        # --help <HELP_TOPIC>
        elif args.help != None:
            pager.page(Cli.help_topic(args.help))

        sys.exit(0)

    #---------------------------------------------------------------------------
    # Fource upper case on loglevel because logging sub-system requires it
    args.loglevel = args.loglevel.upper()

    if args.quiet:
        log.QuietConsoleLogger()
    else:
        # Only change the logging level for the Console Handler, this will
        # leave the logging level for the File Handler unchanged -- which
        # is typically DEBUG
        logSubSystem.SetConsoleHandlerLoggingLevel(args.loglevel)

    #---------------------------------------------------------------------------
    # The default is for args.module == 'images', but if args.append is specified
    # then args.module must be set to None so we can distinguish between them.
    if args.append:
        args.module = None

    #---------------------------------------------------------------------------
    if args.python:
        args.python = "#!" + args.python
        logger.info("Python SPEC string: '%s'" % args.python)

    #---------------------------------------------------------------------------

    logger.debug("Cmd Line: %s" % sys.argv)
    logger.debug(args)
    logger.info(utils.FormatArgsNamespace(args))

    #---------------------------------------------------------------------------
    input_img_files = list()
    if not os.path.exists(args.input):
        logger.fatal("The option --input specifies an argument '%s' that does not exist!" % args.input)
        sys.exit(1)
    elif os.path.isdir(args.input):
        logger.info("The option --input specifies a directory '%s'" % args.input)
        input_img_files = [ f for f in os.listdir(args.input) if os.path.isfile(os.path.join(args.input,f)) ]
    elif os.path.isfile(args.input):
        logger.info("The option --input specifies a file '%s'" % args.input)
        (dirname, imgfilename) = os.path.split(args.input)
        args.input = dirname
        input_img_files.append(imgfilename)
    else:
        logger.fatal("The option --input specifies an argument that is not a directory and is not a file!")
        sys.exit(2)

    if args.module:
        if not pythonIdentifier.match(args.module):
            logger.fatal("The module name specified by '--module %s' is not a legal Python module name!%s" % (args.module, C.LEGAL_PYTHON_IDENT))
            sys.exit(4)
        else:
            logger.info("All images processed will be written to the Python module named '%s'" % args.module)

    if args.append:
        if not pythonIdentifier.match(args.append):
            logger.fatal("The module name specified by '--append %s' is not a legal Python module name!%s" % (args.append, C.LEGAL_PYTHON_IDENT))
            sys.exit(4)
        else:
            logger.info("All images processed will be appended to the Python module named '%s'" % args.append)

    #---------------------------------------------------------------------------
    if args.fixident:
        if args.fixident == C.FIXIDENT_NO_ARG:
            # --fixident specified with NO ARGUMENT -- attempt auto fixup of Python identifier names
            args.fixident = 'gfx'
            logger.info("The option --fixident specified without a PREFIX, using 'gfx'.")
        else:
            # validate the option --fixident has an argument that is a valid python identifier
            if not pythonIdentifier.match(args.fixident):
                logger.warning("The option '--fixident %s' specifies an illegal Python identifier prefix. The option will be ignored." % args.fixident)
                args.fixident = None

    #---------------------------------------------------------------------------
    # The file system prevents image files in the same directory from having
    # the same name; however, a legal file system name can be an illegal Python
    # identifier; so we check the list of images that will be processed to make
    # sure each one is a legal Python identifier (sans file exstension).
    # We check them all and give a report at the end.
    logger.info("Checking if image file(s) can be legal Python identifiers...")
    count = 0
    illegalIdentifiers = list()
    for imgFile in input_img_files:
        (imageName, ext) = os.path.splitext(imgFile)
        if ext in C.IMG_EXTS:
            count += 1
            if not pythonIdentifier.match(imageName):
                illegalIdentifiers.append(imageName)

    if count == 0:
        logger.error("No image files were found.")
        # A directory was specified that contains on recognizeable image files
        # or a file was specified that is not a recognizeable image file.
        # This is a user error...
        logger.fatal("The --input option names a directory with no recognizable image files or names a single image file that is not recognizable.")
        sys.exit(6)

    identmappings = dict()
    if len(illegalIdentifiers) > 0:
        if args.fixident:
            # a valid fix ident prefix, setup a mapping

            for badIdent in illegalIdentifiers:
                badIdent2 = badIdent.replace(' ', '_')
                badIdent2 = badIdent2.replace('-', '_')
                identmappings[badIdent] = args.fixident + badIdent2

            dict_txt = pprint.pformat(identmappings, indent=4, width=1)
            logger.info("Bad Identifier Mapping:\n\n%s" % dict_txt)
        else:
            # not valid fix ident prefix, error out
            msg  = '\n\n' + 80*'-' + '\n'
            msg += '   The following image file(s) do not represent a legal Python Identfier:\n\n'
            for badIdent in illegalIdentifiers:
                msg += "      '%s'\n" % badIdent
            msg += '\n   Please change their file name(s) and re-run,\n'
            msg += '   or use the --fixident [PREFIX] option to potentially fix this issue.\n'
            msg += '   A legal Python identifer must meet the following definition:\n\n      identifier ::=  (letter|"_") (letter | digit | "_")*\n'
            msg += 80*'-' + '\n'
            logger.critical(msg)
            sys.exit(5)

    #---------------------------------------------------------------------------

    logger.info("%d image file(s) will be processed..." % count)

    # If args.code (--code CODE_PATH) does NOT exist create it
    if not os.path.exists(args.code):
        logger.info("Code path '%s' does NOT exist, creating it..." % args.code)
        try:
            os.makedirs(args.code)
        except Exception as e:
            logger.exception("Unable to create path '%s': %s" % (args.code, e))
            sys.exit(8)

        logger.info("Created path '%s'" % args.code)

    # ---------------------------- CODE GENERATION ----------------------------
    CGen = Cg.CodeGen(logger=logger, arg_namespace=args, caller_version=__version__)

    # If appending, this will be None
    if args.module:
        # New Python Module, write mode "wb"
        CGen.genModuleHeader()

    ignoredFiles = list()
    logger.debug("Input Image File List: %s" % input_img_files)
    for imgFile in input_img_files:
        (imageName, ext) = os.path.splitext(imgFile)
        if ext in C.IMG_EXTS:
            imgFilePath = os.path.join(args.input, imgFile)

            if imageName in identmappings:
                new_ident_name = imagedata.make_string_valid_python_identifier(identmappings[imageName])
                logger.warning("Renaming imageName '%s' (illegal Python identifier) to '%s'" % (imageName, new_ident_name))
                imageName = new_ident_name

            logger.info("Processing Image Name '%s' from file: '%s'" % (imageName, imgFile))

            CGen.processImage(image_name=imageName, image_file_path=imgFilePath, image_type=ext)

        else:
            ignoredFiles.append(imgFile)

    if args.module:
        # Single Python Module File
        CGen.genModuleMain()

        CGen.genClosure()

    # Emit the list of ignored files
    if len(ignoredFiles) > 0:
        msg = "The following %d file(s) were ignored:\n" % len(ignoredFiles)
        for f in ignoredFiles:
            msg += "   '%s'\n" % f

        logger.info(msg)

    if args.show:
        # We generated the meta-data module which is used by the generated
        # show module
        CGen.genImageMetaData()

        ShowGen = Sg.ShowGen(logger=logger, arg_namespace=args, caller_version=__version__).Generator()

    sys.exit(0)

if __name__ == "__main__":
    main()
