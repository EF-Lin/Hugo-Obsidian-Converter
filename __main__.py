import argparse
from src.converter import Convert
from src.reader import Glasses
from src.header import Head
from rich import print

parser = argparse.ArgumentParser()
parser.add_argument("read_path")
parser.add_argument("write_path")
# parser.add_argument("pic_path")
args = parser.parse_args()

try:
    g = Glasses(read_path=args.read_path, write_path=args.write_path, name_num=10, sep_name=True)
    file = g.read_file()
    c = Convert(obsidian=file)
    data = c.convert()
    h = Head(main_data=data, date=g.date, title=g.title)
    data = h.add_head()
    g.write_file(data)
    print("[green]INFO: convert successful")
except Exception as ex:
    print(f"[red]ERROR: {ex}")
