#!/usr/bin/env python3

import json
import os
import sys

from rest.utils.testrunner import TestRunner

if __name__ == '__main__':
    WORKSPACE = os.environ.get('WORKSPACE') if os.environ.get('WORKSPACE') else "tmp"
    VARIABLES_PATH = WORKSPACE + "/variables"
    json_file = VARIABLES_PATH + "/testinfo.json"

    status_finished = "finished"
    status_in_progress = "in progress"
    min_args = 2
    if len(sys.argv) < min_args:
        raise Exception("Error: Expecting at least {} args. Got {}, args={}".format(min_args, len(sys.argv), sys.argv))
    try:
        testrunner = TestRunner()
        testrunner.run_commands(json_file, sys.argv[1:])
        dictionary = testrunner.read_dict_from_file(json_file)
    except Exception as e:
        raise e

    print(json.dumps(dictionary))
