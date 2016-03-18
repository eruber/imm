#!/usr/bin/env python
#coding=utf-8
"""
Command line processing
"""

__copyright__ = 'Copyright (C) 2014-2015 by E.R. Uber'
__author__    = 'E.R. Uber (eruber@gmail.com)'
__license__   = 'ISCL'
__version__   = '2.2.0'

#-------------------------------------------------------------------------------
import sys
import os.path
import argparse
import re
import logging

#-------------------------------------------------------------------------------
from imm.cli import constants as C
from imm.cli import codegenerator as CG
from imm.cli.loggingsetup import LOG_LEVELS

#-------------------------------------------------------------------------------
def usage(msg, parser, version):
    """
    Emit usage from docstring at top of file.

    msg   - message string
    parser - command line parser object returned by argparse.ArgumentParser()
    """
    
    import immcli

    lines = list()
    lines.append(msg)
    lines.append('')
    lines.append("Version: %s" % version)
    lines.append('')
    lines.append("Author: %s" % __author__)

    # adds the documentation at the top of the file
    for line in immcli.__doc__.split('\n'):
        try:
            if (line[0] != '#'):
                if line.startswith('<<AUTO-INSERT-CLI-USAGE-HERE>>'):
                    clihelp = parser.format_help().split('\n')
                    for cli_lines in clihelp:
                        lines.append(cli_lines)
                else:
                    lines.append(line)
        except:
            lines.append(line)

    return lines

#-------------------------------------------------------------------------------
def help_topic(topic):
    """
    Return a list of lines for a particular help section in the user manual
    whose heading matches topic.
    """
    lines = list()
    # If not using choices in the add_argument(), need to validate the topic
    # ourselves, the advantage is that we can honor partial matches
    valid = False
    for a_topic in C.HELP_TOPIC_CHOICES:
        # This gives us the partial matching
        if re.match(topic, a_topic):
            valid = True

    if not valid:
        lines.append("\n")
        lines.append("Unknown HELP_TOPIC '%s' - expecting one of:" % topic)
        _topics_list = help_topics()
        for t in _topics_list:
            lines.append("  " + t)
        return lines

    # Supports the topics listing
    if re.match(topic, 'topics'):
        return help_topics()

    # So we can get to the doc string
    import imm as app

    from enum import Enum
    class State(Enum):
        looking = 1
        found = 2
        ended = 3

    lines.append("\n")
    state = State.looking
    underlines_found = 0
    first_line_after_found = False
    for line in app.__doc__.split('\n'):
        #print("LINE: '%s'  STATE: %s" % (line, state))
        if state is State.looking:
            if line.lower().startswith(topic.lower()):
                state = State.found
                lines.append(line)
                first_line_after_found = True
        elif state is State.found:
            if line.startswith('--'):
                first_line_after_found = False
                underlines_found += 1
                if underlines_found == 2:
                    state = State.ended
                    # remove the last line since it is
                    # the next header
                    lines.pop()
                else:
                    # buffer the first underline for output
                    lines.append(line)
            else:
                # In found state, but next line is not a heading underline,
                # so we pop the found state line and reset state
                if first_line_after_found:
                    lines.pop()
                    state = State.looking
                    first_line_after_found = False
                else:
                    lines.append(line)


    if state == State.found:
        # case of running out of doc string while appending the last section
        state = State.ended
        # there may be a blank line or a line of x number of spaces we could
        # elminate if we wanted to

    return lines

#-------------------------------------------------------------------------------
def help_topics():
    """
    Return a list of help topic explanation lines
    """
    pad = 0
    for topic in C.HELP_TOPICS:
        if len(topic) > pad:
            pad = len(topic)

    lines = list()
    title = 'Help Topics for --help HELP_TOPIC'
    #lines.append('\n')
    lines.append(title)
    lines.append(len(title)*'-')
    for topic in C.HELP_TOPICS:
        padstr = (pad - len(topic))*' '
        lines.append("   %s%s - %s" % (padstr, topic, C.HELP_TOPICS[topic]))
    lines.append('\n')
    return lines

#-------------------------------------------------------------------------------
# A simplified version of SmartFormatter at
# https://bitbucket.org/ruamel/std.argparse
class LocalFormatter(argparse.HelpFormatter):

    def __init__(self, *args, **kw):
        self._add_defaults = None
        super(LocalFormatter, self).__init__(*args, **kw)

    def _fill_text(self, text, width, indent):
        return ''.join([indent + line for line in text.splitlines(True)])

    def _split_lines(self, text, width):
        if text.startswith('R|'):
            # Help Text prefaced with 'R|' uses the help text's own raw formatting
            return text[2:].splitlines()

        return argparse.HelpFormatter._split_lines(self, text, width)

    def _format_action(self, action):
        # Separate each action's help with a new line
        s = argparse.HelpFormatter._format_action(self, action)
        return s + '\n'

#-------------------------------------------------------------------------------
def parseCmdLine(version):
    """
    """

    DESCRIPTION = "Reads image files and embeds them in a Python module."

    EPILOG = "For debug output see the log file at: '%s'\nOn Windows invoke as just 'imm' or 'python imm.py'." % C.LOG_PATH \

    cliparser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0])[0:-3],
                                        add_help=False,  # False, we do our own and must supply --help, -h
                                        #formatter_class=argparse.RawTextHelpFormatter,
                                        formatter_class=LocalFormatter,
                                        description=DESCRIPTION,
                                        epilog=EPILOG)

    cliparser.add_argument('--input', '-i', metavar ='INPUT', default='.',
                             help='Specifies an INPUT directory of image files or specifies a single image file. \n' \
                                  'Defaults to current directory.')

    group = cliparser.add_mutually_exclusive_group(required=False)
    group.add_argument('--module', '-m', metavar ='MODULE', default='gfxmodule',
                             help='Specifies the Python MODULE name to generate. MODULE can be specified by --module or --append.\n' \
                                  "If MODULE is not specified, the default MODULE name is 'gfxmodule'.\n" \
                                  'Note that a Python module name does NOT include the .py file extension\n' \
                                  'and must be a legal Python identifier.')
    group.add_argument('--append', '-a', metavar ='MODULE', default=None,
                             help='Specifies the Python MODULE name to append the generated data. MODULE can be specified by --append or --module.\n' \
                                  "If MODULE not specified, the default MODULE name is 'gfxmodule'.\n" \
                                  'Note that a Python module name does NOT include the .py file extension\n' \
                                  'and must be a legal Python identifier.')

    cliparser.add_argument('--code', '-c', metavar ='CODE_PATH', default='.',
                             help="Specifies path where the code to the Python module named MODULE will be generated.\n" \
                                   "If the --show option is specified, then a meta-data module and a GUI module will also be generated.\n" \
                                   "Defaults to current directory.")

    # # MISC flag options
    cliparser.add_argument('--fixident', metavar ='PREFIX', default=None, nargs='?', const=C.FIXIDENT_NO_ARG,
                           help='Fix image names that are illegal Python identifiers by prefixing this PREFIX string. No quotes required.\n' \
                                'PREFIX can be omitted in order to just have spaces and dashes converted to underscores.')

    specline = "#!" + CG.PYTHON_SPEC
    cliparser.add_argument('--python', metavar ='SPEC', default=None, nargs='?', const=CG.PYTHON_SPEC,
                           help='SPEC specifies the first line of the generated Python MODULE. By default no first line beginning with #! is generated.\n' \
                                'If SPEC is omitted, then --python generates "%s" as the first line in MODULE.\n' \
                                'If SPEC is specified, then the first line generated in MODULE will be "#!SPEC"' % specline)

    cliparser.add_argument('--encode', metavar ='ENCODING', default=C.DEFAULT_ENCODE, nargs='?', const=C.DEFAULT_ENCODE,
                           help='ENCODING specifies the character encoding of the generated Python MODULE.\n' \
                                'By default the character encoding used is "utf-8".\n' \
                                'If ENCODING is omitted, then "utf-8" will be used to encode the generated MODULE.\n' \
                                'If ENCODING is specified, then ENCODING will be used. Note that no validation is done on ENCODING.')

    cliparser.add_argument('--show', action='store_true', default=False,
                           help='Generates an addtional image meta-data module and a show module that will\n' \
                                'be executed to display a visual interface to interact with the image data.')

    cliparser.add_argument('--main', action='store_true', default=False,
                           help='If --main not specified, no __main__ statement is generated.\n' \
                                "If --main is specified, then this line is generated:   if __name__ == '__main__':pass")

    cliparser.add_argument('--quiet', action='store_true', help='Suppress all console output (and we do really really mean ALL)')

    LOG_LEVEL_DEFAULT = 'warning'
    cliparser.add_argument('--loglevel', '-l', metavar ='NAME', default=LOG_LEVEL_DEFAULT, choices=LOG_LEVELS,
                             help="Specifies a log level NAME to be used by the logging sub-system. Legal NAME values are:\n %s.\nDefaults to '%s'." % (LOG_LEVELS, LOG_LEVEL_DEFAULT))

    # comment this out if add_help=True
    # cliparser.add_argument('--help', '-h', dest='help', choices=[C.SYNTAX, C.BASIC, C.ALL], metavar='HELP_ITEM', nargs='?',
    #                         default=None, const=C.SYNTAX,
    #                         help="Show help & exit. HELP_ITEM can be omitted for simple command line syntax help\n" \
    #                              "or use HELP_ITEM 'basic' (no single quotes needed) for option defintions\n" \
    #                              "or use HELP_ITEM 'all' (no single quotes needed) for the full help manual.\n")
    cliparser.add_argument('--help', '-h', dest='help', metavar='HELP_TOPIC', nargs='?',
                            default=None, const=C.EMPTY,
                            help="Show help & exit. HELP_TOPIC can be omitted for simple command line syntax help\n" \
                                 "or specify HELP_TOPIC as one of %s" % C.HELP_TOPIC_CHOICES)

    cliparser.add_argument('--version', '-v', action='version', version=version,
                           help='Specifies the version and exits.')

    args = cliparser.parse_args()

    return args, cliparser

#-------------------------------------------------------------------------------
if __name__ == "__main__":
    pass

