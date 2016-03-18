#!/usr/bin/env python
# # -*- coding: utf-8 -*-
"""
Utilities

"""

__copyright__ = 'Copyright (C) 2014-2015 by E.R. Uber'
__author__    = 'E.R. Uber (eruber@gmail.com)'
__license__   = 'ISCL'
__version__   = '0.0.0'

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def FormatArgsNamespace(args, namespace_name='args'):
    """
    Returns a formatted string of argparse's args namespace for easy reading
    """
    # Find longest arg name in the namespase for format alignment padding
    pad = 0
    for attribute in dir(args):
        if len(attribute) > pad:
            pad = len(attribute)

    out = '\n'
    for attribute in dir(args):
        if not attribute.startswith('_'):
            padstr = (pad - len(attribute))*' '
            if isinstance(getattr(args, attribute), str):
                formatstr = "  %s%s%s : '%s'\n"
            else:
                formatstr = "  %s%s%s : %s\n"

            out += formatstr % (padstr, namespace_name+'.', attribute, getattr(args, attribute))

    return out

#-------------------------------------------------------------------------------
if __name__ == "__main__":
    pass
