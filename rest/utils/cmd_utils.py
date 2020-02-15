import subprocess


class CmdUtils:
    @staticmethod
    def run_cmd_detached(command):
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Opened pid {} for command {}".format(p.pid, command))
        # [out, err] = p.communicate()
        # return {
        #     "out": "\n".join(out.decode("UTF-8", "replace").split("\n")[-100:]),
        #     "err": "\n".join(err.decode("UTF-8", "replace").split("\n")[-100:]),
        #     "code": p.returncode,
        #     "pid": p.pid,
        #     "args": p.args
        # }

    @staticmethod
    def run_cmd(command):
        lines_to_slice = 500
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        [out, err] = p.communicate()

        return {
            "out": "\n".join(out.decode("UTF-8", "replace").split("\n")[-lines_to_slice:]).rstrip(),
            "err": "\n".join(err.decode("UTF-8", "replace").split("\n")[-lines_to_slice:]).rstrip(),
            "code": p.returncode,
            "pid": p.pid,
            "args": p.args
        }
