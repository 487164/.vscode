#!/usr/bin/env python3
"""
App for work with XXX
"""

import argparse
import configparser
import esPublicoLogger
import esPublicoUtils
import os, sys
import traceback

from time import time

# getting config
default_config_file = "/etc/PROJECT/sample.conf"

# settings
# basic
NAME        = "SAMPLE"
__author__  = "name@espublico.it"
__version__ = '0.1.0'
__date__    = '2000-12-31'


# Argparser
def cmdArguments(argv=None):
    """ Main entry point of the app """
    # check if argv isn't empty
    if not argv:
        argv = sys.argv

    parse = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    # basic options
    parse.add_argument("-V", "--version", dest="version",
                       action="store_true", help="Show version number and exit.")
    parse.add_argument("-v", "--verbose", dest="verbose",
                       action="store_true", help="Increase output verbosity")
    parse.add_argument("-q", "--quiet", dest="quiet",
                       action="store_true", help="Don't show anything on screen.")
    parse.add_argument("-c", "--config", dest="config",
                      default=default_config_file, help="Define custom config file.")

    try:
        if hasattr(parse, "parse_known_args"):
            # arg contains unknown (ignorable) arguments
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

    # TODO: check args here (or remove if not extra arguments apart from basic):
    # if type(args.sample) != None:
    #    parse.error("Sample error.")

    return args


def define_config(config_file):
    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        settings = {}

        # syslog settings
        settings["syslog_logger"]   = config.get("syslog", "syslog_enable")
        settings["syslog_facility"] = config.get("syslog", "syslog_facility")
        settings["syslog_priority"] = config.get("syslog", "syslog_priority")

        # path settings
        input_path = config.get("paths", "inputpath")
        log_path   = config.get("paths", "logpath")
        input_file = config.get("files", "inputfile")
        log_file   = config.get("files", "logfile")

        # file settings
        settings["logfile"]   = log_path + log_file
        settings["inputfile"] = input_path + input_file

        return settings
    else:
        print("Configuration file %s not exists. Please create it and run again." % (config_file))
        raise SystemExit(1)


# Utils:

# (just an example function) read a plaintext file
def read_txt_file(filename: str) -> list:
    log_data = {"action": "read", "type": "file", "filename": filename}
    lines = ""
    with open(filename, 'r') as f:
        lines = f.readlines()
    logger.do_logs("debug", log_data.update(message="%i lines read from %s" % (len(lines), filename)))
    return lines


# (just another example function) return a sorted list of lines
def sort_lines(lines: list) -> list:
    log_data = {"action": "sort", "type": "lines"}
    try:
        sorted_lines = sorted(lines)
        logger.do_logs("info", {"message": "lines sorted"} | log_data)
    except TypeError as e:
        # the second string is just to have an alignment example of a long message:
        logger.do_logs("error", {"message": "can't sort the lines" + " (words to fill a max-line-length of 120 chars)"
            % lines, "error": str(e)} | log_data)
    return sorted_lines


# TODO: remove the previous examples and write functions here


def run(settings):
    """ Main entry point of the app """
    inputfile = settings["inputfile"]

    # get start time
    apiStart = time()

    # start process
    logger.do_logs("info", {"message": "Starting process..."})

    # TODO: call all the main features from here,
    #       as they should be written as functions. For example:
    lines        = read_txt_file(inputfile)
    sorted_lines = sort_lines(lines)
    print(sorted_lines)

    # get final time
    apiEnd = time()

    # calculate scan total time
    ctime = apiEnd - apiStart
    logger.do_logs("info", {"message": "Process complete in %s seconds"
        % (ctime), "execution_time": str(ctime)})


if __name__ == "__main__":
    try: 
        # check arguments
        args = cmdArguments()
    except Exception as e:
        print(e)

    try:
        # load config
        settings = define_config(args.config)

        # create logger
        level = "INFO" if not args.verbose else "DEBUG"
        logger = esPublicoLogger.Logger(
            NAME, settings["logfile"], level, args.quiet, settings["syslog_logger"], settings["syslog_facility"])
        logger.create_logger()

        # and run application
        run(settings)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.do_logs("critical", {"message": e})
        logger.do_logs("critical", {"message": traceback.format_exc()})
