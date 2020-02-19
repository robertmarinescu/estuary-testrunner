import datetime
import json
import os
import platform

from rest.api.definitions import test_info_init
from rest.utils.cmd_utils import CmdUtils


class TestRunnerInMemory:

    def __init__(self):
        self.__cmd_utils = CmdUtils()

    def run_commands(self, commands):
        status_finished = "finished"
        status_in_progress = "in progress"
        command_dict = test_info_init

        try:
            print("Input json is: " + json.dumps(command_dict) + "\n")
            command_dict['start_pid'] = os.getpid()
            start_total = datetime.datetime.now()
            for command in commands:
                command_dict['commands'][command.strip()] = {}
                command_dict['commands'][command.strip()]['status'] = status_in_progress
                start = datetime.datetime.now()
                command_dict['commands'][command.strip()]['startedat'] = str(start)
                if platform.system() == "Windows":
                    details = self.__cmd_utils.run_cmd_shell_true(command.split())
                else:
                    details = self.__cmd_utils.run_cmd_shell_true([command.strip()])
                command_dict['commands'][command.strip()]['status'] = status_finished
                end = datetime.datetime.now()
                command_dict['commands'][command.strip()]['finishedat'] = str(end)
                command_dict['commands'][command.strip()]['duration'] = round((end - start).total_seconds())
                command_dict['commands'][command.strip()]['details'] = details

            command_dict['finished'] = "true"
            command_dict['started'] = "false"
            end_total = datetime.datetime.now()
            command_dict['finishedat'] = str(end_total)
            command_dict['duration'] = round((end_total - start_total).total_seconds())

        except Exception as e:
            command_dict['commands'][command.strip()]['details'] = "Exception({0})".format(e.__str__())

        return command_dict
