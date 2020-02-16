import errno
import json
import os
import shutil
from pathlib import Path


class IOUtils:

    @staticmethod
    def create_dir(path, permissions=0o755):
        if not os.path.exists(path):
            os.makedirs(path, permissions)

    @staticmethod
    def write_to_file(file, content=""):
        with open(file, 'w') as f:
            f.write(content)

    @staticmethod
    def append_to_file(file, content=""):
        with open(file, 'a') as f:
            f.write(content + "\n")

    @staticmethod
    def write_to_file_binary(file, content=""):
        with open(file, 'wb') as f:
            f.write(content)

    @staticmethod
    def write_to_file_dict(file, content):
        with open(file, 'w') as f:
            json.dump(content, f)

    @staticmethod
    def read_dict_from_file(file):
        try:
            with open(file, 'r') as f:
                return dict(json.loads(f.read()))
        except Exception as e:
            raise e

    @staticmethod
    def get_filtered_list_regex(input_list, regex):
        return [i.strip() for i in input_list if not regex.search(i)]

    @staticmethod
    def read_file(file):
        file_path = Path(file)
        if not file_path.is_file():
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)
        with open(file, 'r') as f:
            return f.read()

    @staticmethod
    def read_file_byte_array(file):
        file_path = Path(file)
        if not file_path.is_file():
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)
        with open(file, 'rb') as f:
            return f.read()

    @staticmethod
    def zip_file(name, path):
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)
        shutil.make_archive(f"/tmp/{name}", 'zip', f"{path}")
