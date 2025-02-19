from dataclasses import dataclass
import os
import datetime
from src.endl import *


@dataclass
class Glasses:
    """
    This is an object that read and write files.
    """
    read_path: str
    write_path: str
    name: str = ""
    name_num: int = -1
    sep_name: bool = False
    file_type: str = ".md"
    default_read_path: str = ""
    default_write_path: str = ""

    def __post_init__(self):
        self.read_path = self.add_filetype(self.path_condition(self.read_path, self.default_read_path))
        self.write_path = self.path_condition(self.write_path, self.default_write_path)
        if self.name == "":
            i = 0
            for n in range(len(self.read_path)):
                if self.read_path[n] in ['/', '\\']:
                    i = n
            if self.name_num == -1:
                self.name = self.read_path[i + 1:]
            else:
                self.name = f"{self.read_path[i + 1:i + self.name_num + 1]}{self.file_type}"

        self.name = self.add_filetype(self.name)
        self.date = self.name[:self.name.find('.')] if self.sep_name else str(datetime.date.today())
        self.title = self.read_path[len(self.read_path) - self.read_path[::-1].find('-'):len(self.read_path) - 1 - self.read_path[::-1].find('.')] if self.sep_name else "New_file"

    @staticmethod
    def path_condition(path: str, default: str) -> str:
        if path[1] == ':':
            default = ""
        if default != "":
            if default[-1] != '/':
                default += '/'
            if default[0] == '/':
                default = default[1:]
        return os.path.normpath(f"{default}{path}")

    def add_filetype(self, path):
        path += self.file_type if path.find('.') == -1 else ''
        return path

    def read_file(self) -> list:
        return open(self.read_path, encoding="utf8").readlines()

    def write_file(self, data: str):
        path = os.path.normpath(f"{self.write_path}/{self.name}")
        i = 2
        while os.path.exists(path):
            path = path.split('.')
            path[0] = path[0][:-2] if i > 2 else path[0]
            path[0] += f"-{i}."
            i += 1
            path = list2str(path)
        with open(path, "w+", encoding="utf8") as f:
            f.write(data)
            os.startfile(self.write_path)


if __name__ == "__main__":
    g = Glasses(read_path="./test/2024-03-30-uuu.md", write_path="./test/", name="ttt", sep_name=True)
    print(g.date)
    print(g.add_filetype('C:/a'))
