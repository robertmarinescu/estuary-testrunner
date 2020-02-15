import datetime
import os
import platform
from multiprocessing import Process, Queue

from rest.utils.cmd_utils import CmdUtils
from rest.utils.io_utils import IOUtils


class TestRunnerParallel:

    def __init__(self):
        self.__cmd_utils = CmdUtils()
        self.__io_utils = IOUtils()

    def run_command(self, queue, dictionary, command):
        status_finished = "finished"
        status_in_progress = "in progress"
        dictionary['commands'][command.strip()]['status'] = status_in_progress
        start = datetime.datetime.now()
        dictionary['commands'][command.strip()]['startedat'] = str(start)
        details = self.__cmd_utils.run_cmd(command.split())
        dictionary['commands'][command.strip()]['status'] = status_finished
        end = datetime.datetime.now()
        dictionary['commands'][command.strip()]['finishedat'] = str(end)
        dictionary['commands'][command.strip()]['duration'] = round((end - start).total_seconds())
        dictionary['commands'][command.strip()]['details'] = details

        queue.put({command: dictionary['commands'][command.strip()]})

    def run_commands(self, json_file, commands):
        queue = Queue()

        try:
            dictionary = self.__io_utils.read_dict_from_file(json_file)
            dictionary['start_pid'] = os.getpid()
            start_total = datetime.datetime.now()

            procs = [Process(target=self.run_command, args=(queue, dictionary, command.strip(),)) for command in
                     commands]

            # start processes
            for p in procs:
                p.start()

            # join processes
            for p in procs:
                p.join()

            for _ in procs:
                result = queue.get()  # get from fifo
                for command in commands:
                    if result.get(command) is not None:
                        dictionary['commands'][command] = result.get(command)

            self.__io_utils.write_to_file_dict(json_file, dictionary)
            dictionary['finished'] = "true"
            dictionary['started'] = "false"
            end_total = datetime.datetime.now()
            dictionary['finishedat'] = str(end_total)
            dictionary['duration'] = round((end_total - start_total).total_seconds())
            self.__io_utils.write_to_file_dict(json_file, dictionary)

        except Exception as e:
            raise e
