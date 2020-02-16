#!/usr/bin/env python3

import json
import os
import sys

from rest.utils.io_utils import IOUtils
from rest.utils.testrunner import TestRunner
from rest.utils.testrunner_parallel import TestRunnerParallel

if __name__ == '__main__':
    WORKSPACE = os.environ.get('WORKSPACE') if os.environ.get('WORKSPACE') else "tmp"
    VARIABLES_PATH = WORKSPACE + "/variables"
    COMMAND_LOGGER_PATH = WORKSPACE + "/commandlogger.txt"
    io_utils = IOUtils()

    json_file = VARIABLES_PATH + "/commandinfo.json"
    if sys.argv[1] is not None:
        json_file = VARIABLES_PATH + "/{}".format(sys.argv[1].strip())
    mode = "parallel"
    if sys.argv[2] is not None:
        mode = sys.argv[2].strip()

    io_utils.append_to_file(COMMAND_LOGGER_PATH, " ".join(sys.argv))

    status_finished = "finished"
    status_in_progress = "in progress"
    min_args = 4
    if len(sys.argv) < min_args:
        raise Exception("Error: Expecting at least {} args. Got {}, args={}".format(min_args, len(sys.argv), sys.argv))
    try:
        if mode == "sequential":
            testrunner = TestRunner()
            testrunner.run_commands(json_file, sys.argv[3:])
            dictionary = io_utils.read_dict_from_file(json_file)
        elif mode == "parallel":
            testrunner = TestRunnerParallel()
            testrunner.run_commands(json_file, sys.argv[3:])
            dictionary = io_utils.read_dict_from_file(json_file)
        else:
            raise Exception("Unsupported mode: " + mode)
    except Exception as e:
        raise e

    print(json.dumps(dictionary) + "\n")
