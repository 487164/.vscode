#!/usr/bin/env python3
"""
App for work with XXX
"""

import argparse
import configparser
import esPublicoLogger
import json, os, sys
import traceback

from datetime import datetime, timedelta
from time import time, sleep

# getting config
config_file = "sample.conf"
config      = configparser.ConfigParser()
config.read(config_file)

# settings
# basic
NAME        = "SAMPLE"
__author__  = "name@espublico.it"
__version__ = '0.1.0'
__date__    = '2000-12-31'

## default options
CONFIG_VAR  = config.get("sample", 'CONFIG_VAR')

log_data = {
    "action": "",
    "type": "",
    "message": ""
}
syslog_logger   = config.get("syslog", "syslog_enable")
syslog_facility = config.get("syslog", "syslog_facility")
syslog_priority = config.get("syslog", "syslog_priority")

log_path = config.get("paths", "logpath")
tmp_path = config.get("paths", "tmppath")

log_file  = config.get("files", "logfile")
logfile   = log_path + log_file


#### Argparser
def cmdArguments():
    """ Main entry point of the app """
    # check if argv isn't empty
    if not argv:
        argv = sys.argv

    parse = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)

    # basic options
    parse.add_argument("-V", "--version", dest="version",
                       action="store_true", help="Show version number and exit.")
    parse.add_argument("-v", "--verbose", dest="verbose",
                       action="store_true", help="Increase output verbosity")
    parse.add_argument("-q", "--quiet", dest="quiet",
                       action="store_true", help="Don't show anything on screen.")

    # main options
    main = parse.add_argument_group("Main", "Main options.")
    # TODO: add arguments like --sample:
    # main.add_argument("-S", "--sample", dest="sample", default=config_file, help="A sample argument.")

    try:
        if hasattr(parse, "parse_known_args"):
            (args, arg) = parse.parse_known_args(argv)
        else:
            parse.parse_args(argv)
    except SystemExit:
        raise SystemExit(0)

    for i in range(len(argv)):
        if args.version:
            print("%s\nVersion: %s\nAuthor: %s" %
                  (NAME, __version__, __author__))
            raise SystemExit

    # TODO: check args here:
    # if type(args.sample) != None:
    #    parse.error("Sample error.")

    return args


#### Utils

## read file
def read_txt_file(filename):
    data = ""
    with open(filename, 'r') as f:
        data = f.read()
    return data


## create file
def check_file_exists(filename):
    if not os.path.isfile(filename):
        open(filename, "w").close()


## write to file
def write_txt_file(filename, data):
    with open(filename, "w") as f:
        f.write(data)


#### Main

def run():
    """ Main entry point of the app """

    ## get start time
    apiStart = time()

    ## start process
    logger.do_logs("info", {"message": "Starting process..."})

    # TODO: call all the main features from here,
    #       as they should be written as functions

    ## get final time
    apiEnd = time()

    ## calculate scan total time
    ctime = apiEnd - apiStart
    logger.do_logs("info", {"message": "Process complete in %s seconds" % (
        ctime), "execution_time": str(ctime)})


if __name__ == "__main__":
    try:
        ## check arguments
        args = cmdArguments()
    except Exception as e:
        print(e)

    try:
        result = 0

        ## create logger
        level = "INFO" if not args.verbose else "DEBUG"
        logger = esPublicoLogger.Logger(
            NAME, logfile, level, args.quiet, syslog_logger, syslog_facility)
        logger.create_logger()

        ## and run application
        run()
    except SystemExit as e:
        result = e
        pass
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.do_logs("critical", {"message": e})
        logger.do_logs("critical", {"message": traceback.format_exc()})
    except RuntimeError as e:
        logger.do_logs("critical", {"message": e})
        logger.do_logs("critical", {"message": traceback.format_exc()})
