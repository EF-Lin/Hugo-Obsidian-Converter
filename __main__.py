import argparse
from src.converter import Convert
from src.reader import Glasses

parser = argparse.ArgumentParser()
parser.add_argument("read_path")
parser.add_argument("write_path")
# parser.add_argument("pic_path")
args = parser.parse_args()

g = Glasses(read_path=args.read_path, write_path=args.write_path, name_num=10)
file = g.read_file()
c = Convert(obsidian=file)
data = c.convert()
g.write_file(data)
