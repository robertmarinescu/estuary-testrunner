import datetime
import json
import os
import platform

from rest.utils.cmd_utils import CmdUtils
from rest.utils.io_utils import IOUtils


class TestRunner:

    def __init__(self):
        self.__cmd_utils = CmdUtils()
        self.__io_utils = IOUtils()

    def run_commands(self, json_file, commands):
        status_finished = "finished"
        status_in_progress = "in progress"
        try:
            command_dict = self.__io_utils.read_dict_from_file(json_file)
            print("Input json is: " + json.dumps(command_dict) + "\n")
            command_dict['start_pid'] = os.getpid()
            start_total = datetime.datetime.now()
            for command in commands:
                command_dict['commands'][command.strip()]['status'] = status_in_progress
                start = datetime.datetime.now()
                command_dict['commands'][command.strip()]['startedat'] = str(start)
                self.__io_utils.write_to_file_dict(json_file, command_dict)
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
            self.__io_utils.write_to_file_dict(json_file, command_dict)

        except Exception as e:
            raise e
