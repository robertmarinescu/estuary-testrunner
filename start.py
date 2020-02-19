#!/usr/bin/env python3
import json
import os
import sys

from rest.utils.io_utils import IOUtils
from rest.utils.testrunner import TestRunner

if __name__ == '__main__':
    WORKSPACE = os.environ.get('WORKSPACE') if os.environ.get('WORKSPACE') else "tmp"
    VARIABLES_PATH = WORKSPACE + "/variables"
    COMMAND_LOGGER_PATH = WORKSPACE + "/commandlogger.txt"
    supported_modes = ("sequential", "parallel")
    supported_files = ("testinfo.json", "commandinfo.json")
    io_utils = IOUtils()

    min_args = 4
    if len(sys.argv) < min_args:
        raise Exception(
            "Error: Expecting at least {} args. Got {}, args={}".format(min_args, len(sys.argv), sys.argv))

    file = sys.argv[1].strip()
    mode = sys.argv[2].strip()
    commands_list = sys.argv[3:]

    if mode not in supported_modes:
        raise Exception(
            "Error: Unsupported mode argument: {}".format(mode) + ". Expected files: {}".format(
                json.dumps(supported_modes)))

    if file not in supported_files:
        raise Exception(
            "Error: Unsupported file argument: {}".format(file) + ". Expected files: {}".format(
                json.dumps(supported_files)))

    file_path = VARIABLES_PATH + "/{}".format(file)
    io_utils.append_to_file(COMMAND_LOGGER_PATH, json.dumps(sys.argv))

    try:
        if mode == supported_modes[0]:
            testrunner = TestRunner()
            testrunner.run_commands(file_path, sys.argv[3:])
            dictionary = io_utils.read_dict_from_file(file_path)
    except Exception as e:
        raise e

    print(json.dumps(dictionary) + "\n")
