import os.path
from dataclasses import dataclass
import datetime
from src.endl import list_endl
from typing import ClassVar

@dataclass
class Head:
    """
    This object will add a header based on temp.
    """
    main_data: str
    date: str
    title: str
    temp: str = "default.md"
    default_path: ClassVar[str] = "/data/archetypes/"

    def __post_init__(self):
        self.path = os.path.normpath(f"{os.getcwd()}/Hugo-Obsidian-Converter/{self.default_path}/{self.temp}")
        self.head_data = open(self.path, 'r', encoding="utf-8").read()

    def add_head(self, is_date=True, is_title=True) -> str:
        self.__rep_date() if is_date else 0
        self.__rep_title() if is_title else 0
        return list_endl(self.head_data) + self.main_data

    def __rep_date(self):
        self.head_data = self.head_data.replace("{{date}}", f"{self.date}")
        self.head_data = self.head_data.replace("{{lastdate}}", str(datetime.date.today()))

    def __rep_title(self):
        self.head_data = self.head_data.replace("{{title}}", f"{self.title}")


if __name__ == "__main__":
    pass
