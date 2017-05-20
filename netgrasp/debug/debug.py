import logging
import sys
import pwd

ALWAYS   = 0
VERBOSE  = 1
VERBOSE2 = 2
VERBOSE3 = 3
FATAL    = True
NOTFATAL = False

DEBUG    = (logging.DEBUG, VERBOSE, NOTFATAL)
DEBUG2   = (logging.DEBUG, VERBOSE2, NOTFATAL)
DEBUG3   = (logging.DEBUG, VERBOSE3, NOTFATAL)
INFO     = (logging.INFO, VERBOSE, NOTFATAL)
INFO     = (logging.INFO, VERBOSE2, NOTFATAL)
WARNING  = (logging.WARNING, ALWAYS, NOTFATAL)
ERROR    = (logging.ERROR, ALWAYS, NOTFATAL)
CRITICAL = (logging.CRITICAL, ALWAYS, FATAL)

PRINT    = 0
FILE     = 1

# mode: PRINT or FILE
class Debugger:
    def __init__(self, mode = PRINT, logger = None, level = logging.WARNING, verbosity = False):
        self.mode = mode
        self.logger = logger
        self.level = level
        self.verbosity = False

    def log(self, message, args, severity):
        level, verbose, fatal = severity
        if self.mode == FILE:
            if not self.logger:
                self.mode = PRINT
                self.log(message, args, level, 9)
                self.fatal("fatal error, no logger provided, exiting")
            if not verbose or verbose >= self.verbosity:
                self.logger.log(level, message, *args)

        if fatal:
            # if writing to file we log and then print message, otherwise just print
            self.fatal(message, args)

        if self.mode == PRINT:
            if verbose >= self.verbosity:
                if args:
                    print message % args
                else:
                    print message

    # Determine who we are, for pretty logging.
    def whoami(self):
        whoami = pwd.getpwuid(os.getuid())
        if whoami:
            return whoami[0]

    def debug(self, message, args):
        self.log(message, args, DEBUG)

    def debug2(self, message, args):
        self.log(message, args, DEBUG2)

    def debug3(self, message, args):
        self.log(message, args, DEBUG3)

    def info(self, message, args):
        self.log(message, args, INFO)

    def info2(self, message, args):
        self.log(message, args, INFO2)

    def warning(self, message, args):
        self.log(message, args, WARNING)

    def error(self, message, args):
        self.log(message, args, ERROR)

    def critical(self, message, args):
        self.log(message, args, CRITICAL)

    def fatal(self, message, args = None):
        if args:
            sys.exit(message % args)
        else:
            sys.exit(message)
