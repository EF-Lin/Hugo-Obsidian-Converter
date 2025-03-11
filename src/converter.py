from dataclasses import dataclass
from src.endl import str_endl, del_first_blank_line


@dataclass
class Convert:
    """
    This object will receive an obsidian-md.readlines list and return a converted hugo-md string.
    """
    obsidian: list
    pic_path: str = ""
    allow_chars = ['>', '!', '[', '#', '-', '{', '(', '-', '\n']

    def __post_init__(self):
        if self.pic_path != "" and self.pic_path[-1] in ['/', '\\'] and len(self.pic_path) > 3:
            self.pic_path = self.pic_path[0:-1]

    def convert(self, is_delcon=True, is_sep=True, is_pic = True, is_adm = True, is_highlight=True) -> str:
        try:
            self.obsidian = del_first_blank_line(self.obsidian)
            self.__del_content() if is_delcon else 0
            self.__sep(highlight=is_highlight) if is_sep else 0
            self.__pic() if is_pic else 0
            self.__adm() if is_adm else 0
            self.obsidian = del_first_blank_line(self.obsidian)
            # self.__highlight() if is_highlight else 0
            return str_endl(''.join(self.obsidian))
        except Exception as ex:
            return str(ex)

    def _test(self):
        self.__del_content()

    def __sep(self, highlight: bool):
        i = 0
        jump = -1
        while i < len(self.obsidian):
            j = self.obsidian[i].find("```")
            jump = -jump if j != -1 else jump
            if self.obsidian[i][0] not in self.allow_chars and jump < 0:
                self.obsidian[i] += '\n'
                self.obsidian[i] = self.__highlight(self.obsidian[i]) if highlight else self.obsidian[i]
            elif jump < 0:
                self.obsidian[i] = self.__highlight(self.obsidian[i]) if highlight else self.obsidian[i]
            elif j != -1 and jump > 0:
                self.obsidian[i] = self.obsidian[i].replace('\n', "{linenos=true}\n")
            i += 1

    @staticmethod
    def __highlight(s: str) -> str:
        while s.find("==") >= 0:
            s = s.replace("==", "<mark>", 1).replace("==", "</mark>", 1)
        return s

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
        """
        adm_type = {
            "note": "note",
            "info": "info",
            "hint": "tip",
            "tip": "tip",
            "caution": "warning",
            "danger": "danger",
            "bug": "bug",
            "success": "success",
            "question": "question",
            "failure": "failure",
            "example": "example"
        }
        """
        n = 0
        while n < len(self.obsidian) - 1:
            i = self.obsidian[n].find("> [!")*self.obsidian[n].find(">[!")
            if i <= 0:
                kind = self.obsidian[n][self.obsidian[n].find('!') + 1: self.obsidian[n].find(']')].lower()
                kind = "tip" if kind == "hint" else kind
                title = kind.capitalize()
                self.obsidian[n] = f"{{{{< admonition type=\"{kind}\" title=\"{title}\" >}}}}\n"
                j = n+1
                while self.obsidian[j] != '\n' and j < len(self.obsidian):
                    self.obsidian[j] = self.obsidian[j].replace('> ', '', 1)
                    self.obsidian[j] = self.obsidian[j].replace('>', '', 1)
                    self.obsidian[j] = str_endl(self.obsidian[j]) + '\n'
                    j += 1
                self.obsidian.insert(j, "{{< /admonition >}}\n")
            n += 1

    def __highlight_old(self):
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
