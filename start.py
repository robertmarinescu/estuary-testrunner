#!/usr/bin/env python3
import json
import os
import sys

from rest.utils.io_utils import IOUtils
from rest.utils.testrunner import TestRunner

if __name__ == '__main__':
    io_utils = IOUtils()
    WORKSPACE = os.environ.get('WORKSPACE') if os.environ.get('WORKSPACE') else "tmp"
    VARIABLES_PATH = WORKSPACE + "/variables"
    COMMAND_LOGGER_PATH = WORKSPACE + "/commandlogger.txt"
    file_path = VARIABLES_PATH + "/testinfo.json"

    io_utils.append_to_file(COMMAND_LOGGER_PATH, " ".join(sys.argv))

    min_args = 3
    if len(sys.argv) < min_args:
        raise Exception(
            "Error: Expecting at least {} args. Got {}, args={}".format(min_args, len(sys.argv), sys.argv))

    test_id = sys.argv[1]
    commands_list = sys.argv[2:]

    test_runner = TestRunner()
    dictionary = test_runner.run_commands(file_path, test_id, commands_list)
    dictionary = io_utils.read_dict_from_file(file_path)

    print(json.dumps(dictionary) + "\n")
