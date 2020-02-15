import datetime
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
            dictionary = self.__io_utils.read_dict_from_file(json_file)
            dictionary['start_pid'] = os.getpid()
            start_total = datetime.datetime.now()
            for command in commands:
                dictionary['commands'][command.strip()]['status'] = status_in_progress
                start = datetime.datetime.now()
                dictionary['commands'][command.strip()]['startedat'] = str(start)
                self.__io_utils.write_to_file_dict(json_file, dictionary)
                details = self.__cmd_utils.run_cmd(command.split())
                dictionary['commands'][command.strip()]['status'] = status_finished
                end = datetime.datetime.now()
                dictionary['commands'][command.strip()]['finishedat'] = str(end)
                dictionary['commands'][command.strip()]['duration'] = round((end - start).total_seconds())
                dictionary['commands'][command.strip()]['details'] = details

            dictionary['finished'] = "true"
            dictionary['started'] = "false"
            end_total = datetime.datetime.now()
            dictionary['finishedat'] = str(end_total)
            dictionary['duration'] = round((end_total - start_total).total_seconds())
            self.__io_utils.write_to_file_dict(json_file, dictionary)

        except Exception as e:
            raise e
