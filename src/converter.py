from dataclasses import dataclass
from src.endl import *


@dataclass
class Convert:
    """
    This object will receive an obsidian-md.readlines list and return a converted hugo-md string.
    """
    obsidian: list
    pic_path: str = ""
    allow_chars = ['>', '!', '[', '#', '-', '{', '(', '-', '\n']

    def __post_init__(self):
        self.obsidian_str = ""
        if self.pic_path != "" and self.pic_path[-1] in ['/', '\\'] and len(self.pic_path) > 3:
            self.pic_path = self.pic_path[0:-1]

    def convert(self, is_delcon=True, is_sep=True, is_pic = True, is_adm = True, is_highlight=True) -> str:
        try:
            self.obsidian = del_first_blank_line(self.obsidian)
            self.__del_content() if is_delcon else 0
            self.__sep() if is_sep else 0
            self.__pic() if is_pic else 0
            self.__adm() if is_adm else 0
            self.obsidian = del_first_blank_line(self.obsidian)

            self.obsidian_str = list2str(self.obsidian)

            self.__highlight() if is_highlight else 0

            self.obsidian_str = str_endl(self.obsidian_str)

            return self.obsidian_str
        except Exception as ex:
            return str(ex)

    def _test(self):
        self.__del_content()

    def __sep(self):
        i = 0
        jump = -1
        while i < len(self.obsidian):
            j = self.obsidian[i].find("```")
            jump = -jump if j != -1 else jump
            if self.obsidian[i][0] not in self.allow_chars and jump < 0:
                self.obsidian[i] += '\n'
            elif j != -1 and jump > 0:
                self.obsidian[i] = self.obsidian[i].replace('\n', "{linenos=true}\n")
            i += 1

    def __pic(self):
        for n in range(len(self.obsidian)):
            i = self.obsidian[n].find("![[")
            if i != -1:
                j = self.obsidian[n].find("]]")
                file = self.obsidian[n][i + 3:j]
                title = self.obsidian[n][i + 3:self.obsidian[n].find('.')]
                self.obsidian[n] = self.obsidian[n].replace(self.obsidian[n][i:j + 2],
                                                            f"![{title}]({self.pic_path}/{file} \"{title}\")",
                                                            1)

    def __adm(self):
        adm_type = {
            "note": "note",
            "info": "note",
            "hint": "tip",
            "tip": "tip",
            "caution": "warning",
            "warning": "danger"
        }
        n = 0
        while n < len(self.obsidian) - 1:
            i = self.obsidian[n].find("> [!")*self.obsidian[n].find(">[!")
            if i <= 0:
                kind = self.obsidian[n][self.obsidian[n].find('!') + 1: self.obsidian[n].find(']')].lower()
                new_kind = adm_type.get(kind, "note")
                title = new_kind.capitalize()
                self.obsidian[n] = f"{{{{< admonition type=\"{kind}\" title=\"{title}\" >}}}}\n"
                j = n+1
                while self.obsidian[j].find('>') >= 0:
                    self.obsidian[j] = self.obsidian[j].replace('> ', '', 1)
                    self.obsidian[j] = self.obsidian[j].replace('>', '', 1)
                    self.obsidian[j] = str_endl(self.obsidian[j])
                    j += 1
                    if j > (len(self.obsidian) - 1):
                        break
                self.obsidian.insert(j, "{{< /admonition >}}\n")
            n += 1

    def __highlight(self):
        flag = 1
        while self.obsidian_str.find("==") >= 0:
            self.obsidian_str = self.obsidian_str.replace("==", "<mark>", 1) if flag > 0 else self.obsidian_str.replace("==", "</mark>", 1)

    def __del_content(self):
        n = 0
        while n < len(self.obsidian):
            i = self.obsidian[n].find("```table-of-contents")
            if i >= 0:
                self.obsidian.pop(n)
                while True:
                    if self.obsidian[n].find("```") >= 0:
                        self.obsidian.pop(n)
                        break
                    else:
                        self.obsidian.pop(n)
            n += 1


if __name__ == '__main__':
    f = open("../test/t1.md").readlines()
    c = Convert(f, "C:/")
    p = c.convert()
    print(p)
