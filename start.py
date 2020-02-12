#!/usr/bin/env python3

import datetime
import json
import os
import platform
import subprocess
import sys


class TestRunner:

    @staticmethod
    def load_dict_from_file(file):
        try:
            with open(file, 'r') as f:
                return json.loads(f.read())
        except Exception as e:
            raise e

    @staticmethod
    def save_dict_to_file(dictionary, file):
        with open(file, 'w') as f:
            json.dump(dictionary, f)

    @staticmethod
    def run_test(command):
        lines_to_slice = 500
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        [out, err] = p.communicate()

        return {
            "out": "\n".join(out.decode('utf-8').split("\n")[-lines_to_slice:]).rstrip(),
            "err": "\n".join(err.decode('utf-8').split("\n")[-lines_to_slice:]).rstrip(),
            "code": p.returncode,
            "pid": p.pid,
            "args": p.args
        }


if __name__ == '__main__':
    WORKSPACE = os.environ.get('WORKSPACE') if os.environ.get('WORKSPACE') else "tmp"
    VARIABLES_PATH = WORKSPACE + "/variables"
    testinfo_file = VARIABLES_PATH + "/{}".format(sys.argv[1])  # (testinfo.json or commandinfo.json)

    status_finished = "finished"
    status_in_progress = "in progress"
    if len(sys.argv) < 3:
        print("Error: Expecting at least 3 args. Got {}, args={}".format(len(sys.argv), sys.argv))
        sys.exit(1)
    try:
        dictionary = TestRunner.load_dict_from_file(testinfo_file)
        dictionary['start_pid'] = os.getpid()
        start_total = datetime.datetime.now()

        print("Success: Got {}, args={}".format(len(sys.argv), sys.argv))
        arguments = sys.argv
        for i in range(2, len(arguments)):
            dictionary['commands'][arguments[i].strip()]['status'] = status_in_progress
            start = datetime.datetime.now()
            dictionary['commands'][arguments[i].strip()]['startedat'] = str(start)
            TestRunner.save_dict_to_file(dictionary, testinfo_file)
            if platform.system() == "Windows":
                details = TestRunner.run_test(" ".join(arguments[i].split()).split())
            else:
                details = TestRunner.run_test([arguments[i].strip()])
            dictionary['commands'][arguments[i].strip()]['status'] = status_finished
            end = datetime.datetime.now()
            dictionary['commands'][arguments[i].strip()]['finishedat'] = str(end)
            dictionary['commands'][arguments[i].strip()]['duration'] = round((end - start).total_seconds())
            dictionary['commands'][arguments[i].strip()]['details'] = details

        dictionary['finished'] = "true"
        dictionary['started'] = "false"
        end_total = datetime.datetime.now()
        dictionary['finishedat'] = str(end_total)
        dictionary['duration'] = round((end_total - start_total).total_seconds())
        TestRunner.save_dict_to_file(dictionary, testinfo_file)
    except Exception as e:
        raise e

    sys.exit(0)
