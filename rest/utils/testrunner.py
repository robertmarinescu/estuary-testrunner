import datetime
import os
import platform

from rest.utils.io_utils import IOUtils
from utils.cmd_utils import CmdUtils


class TestRunner:

    def __init__(self):
        self.cmd_utils = CmdUtils()
        self.io_utils = IOUtils()

    def run_commands(self, json_file, commands):
        status_finished = "finished"
        status_in_progress = "in progress"
        try:
            dictionary = self.io_utils.read_dict_from_file(json_file)
            dictionary['start_pid'] = os.getpid()
            start_total = datetime.datetime.now()
            for i in range(0, len(commands)):
                dictionary['commands'][commands[i].strip()]['status'] = status_in_progress
                start = datetime.datetime.now()
                dictionary['commands'][commands[i].strip()]['startedat'] = str(start)
                self.io_utils.write_to_file_dict(json_file, dictionary)
                if platform.system() == "Windows":
                    details = self.cmd_utils.run_cmd(commands[i].split())
                else:
                    details = self.cmd_utils.run_cmd([commands[i].strip()])
                dictionary['commands'][commands[i].strip()]['status'] = status_finished
                end = datetime.datetime.now()
                dictionary['commands'][commands[i].strip()]['finishedat'] = str(end)
                dictionary['commands'][commands[i].strip()]['duration'] = round((end - start).total_seconds())
                dictionary['commands'][commands[i].strip()]['details'] = details

            dictionary['finished'] = "true"
            dictionary['started'] = "false"
            end_total = datetime.datetime.now()
            dictionary['finishedat'] = str(end_total)
            dictionary['duration'] = round((end_total - start_total).total_seconds())
            self.io_utils.write_to_file_dict(json_file, dictionary)

        except Exception as e:
            raise e
