#!/usr/bin/env python
#coding=utf-8
"""
Setup up logging

1. To console at INFO level with a simplified less noisy log record
2. To a log file at DEBUG Level with a more detailed log record
3. To a file that keeps certain number of backed up log file sessions
   before rolling them over
"""

#-------------------------------------------------------------------------------
import os
import os.path
import logging
import logging.handlers
import time
#-------------------------------------------------------------------------------
from imm.cli import constants as C

#-------------------------------------------------------------------------------
LOG_LEVELS = ['notset', 'debug', 'info', 'warning', 'error', 'critical']

#-------------------------------------------------------------------------------
def logLevelIsValid(levelname):
    """
    Returns True if levelname is a valid logging level name, else returns False.
    """
    numeric_level = getattr(logging, loglevel.upper(), None)
    
    if not isinstance(numeric_level, int):
        return(False)

    return(True)


#-------------------------------------------------------------------------------
# Setup logging to console at level INFO and logging to a log file at
# level DEBUG.
#-------------------------------------------------------------------------------
class Setup():
    def __init__(self, apploggername):
        # Check if previous log file exits and set in motion roll-over if it does
        rollOverLogFile = False
        if os.path.isfile(C.LOG_PATH):
            rollOverLogFile = True

        self._logger = logging.getLogger()

        self._logger.setLevel(logging.DEBUG)

        # create console handler and set log level
        self._ch = logging.StreamHandler()
        self._ch.setLevel(logging.INFO)

        # create a rotating file handler that keeps backupCount number of backups
        # this call actually creates the Log file, so we can roll it over once logging is completely setup
        self._fh = logging.handlers.RotatingFileHandler(C.LOG_PATH, mode=C.LOG_FILE_MODE, encoding=C.LOG_ENCODING, backupCount=C.LOG_FILE_BACKUP_COUNT)
        self._fh.setLevel(logging.DEBUG)
        # create formatters
        self._formatter_fh = logging.Formatter(C.LOG_FILE_FORMAT)
        self._formatter_ch = logging.Formatter(C.LOG_CONSOLE_FORMAT)
        # add formatters to handlers
        self._ch.setFormatter(self._formatter_ch)
        self._fh.setFormatter(self._formatter_fh)

        # add handlers to root logger
        self._logger.addHandler(self._ch)
        self._logger.addHandler(self._fh)

        # use a child of the root logger with app's logger name
        self._logger = logging.getLogger().getChild(apploggername)
        self._logger.setLevel(logging.DEBUG)

        if rollOverLogFile:
            self._logger.debug('\n---------\nPrevious Log file closed & rolled-over on: %s.\n---------\n' % time.asctime())
            self._fh.doRollover()


    def Logger(self):
        return self._logger


    def RootLogger(self):
        return logging.getLogger()


    def SetConsoleHandlerLoggingLevel(self, level):
        """
        Changes the logging level for the console handler
        """
        self._ch.setLevel(level)


    def SetFileHandlerLoggingLevel(self, level):
        """
        Changes the logging level for the file handler
        """
        self._fh.setLevel(level)


    def QuietConsoleLogger(self):
        """
        This will suppress logging to the console. For quiet mode.
        """
        # Remove the console handler from the root logger where it was originally attached
        logging.getLogger().removeHandler(self._ch)



#-------------------------------------------------------------------------------
if __name__ == "__main__":
    pass
