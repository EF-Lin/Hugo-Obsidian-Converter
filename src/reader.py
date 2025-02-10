from dataclasses import dataclass
import os
import datetime


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
        self.read_path = self.path_condition(self.read_path, self.default_read_path)
        self.write_path = self.path_condition(self.write_path, self.default_write_path)
        if self.name != "":
            if self.name.find('.') == -1:
                self.name += self.file_type
        else:
            i = 0
            for n in range(len(self.read_path)):
                if self.read_path[n] in ['/', '\\']:
                    i = n
            if self.name_num == -1:
                self.name = self.read_path[i+1:]
            else:
                self.name = f"{self.read_path[i+1:i+self.name_num+1]}{self.file_type}"

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

    def read_file(self) -> list:
        return open(self.read_path, encoding="utf8").readlines()

    def write_file(self, data: str):
        path = os.path.normpath(f"{self.write_path}/{self.name}")
        i = 2
        while os.path.exists(path):
            path += f"-{i}"
            i += 1
        with open(path, "w+", encoding="utf8") as f:
            f.write(data)
            os.startfile(self.write_path)


if __name__ == "__main__":
    g = Glasses(read_path="./test/2024-03-30-uuu.md", write_path="./test/", name="ttt", sep_name=True)
    print(g.date)
