from dataclasses import dataclass


@dataclass
class Convert:
    """
    This object will receive an obsidian-md.readlines list and return a converted hugo-md string.
    """
    obsidian: list
    pic_path: str
    allow_chars = ['>', '!', '[', '#', '-', '{', '(', '`', '-', '\n']

    def __post_init__(self):
        self.__re_str = ""
        if self.pic_path[-1] == '/' or '\\' and len(self.pic_path) > 3:
            self.pic_path = self.pic_path[0:-1]

    def convert(self, is_delcon=True, is_sep=True, is_pic = True, is_adm = True):
        try:
            self.__del_content() if is_delcon else 0
            self.__sep() if is_sep else 0
            self.__pic() if is_pic else 0
            self.__adm() if is_adm else 0
            for i in self.obsidian:
                self.__re_str += i
            return self.__re_str
        except Exception as ex:
            return str(ex)

    def test(self):
        self.__del_content()

    def __del_first_blank_line(self):
        self.obsidian.pop(0) if self.obsidian[0] == '\n' else 0

    def __sep(self):
        for i in range(len(self.obsidian)):
            if self.obsidian[i][0] not in self.allow_chars:
                self.obsidian[i] += '\n'

    def __pic(self):
        for n in range(len(self.obsidian)):
            i = self.obsidian[n].find("![[")
            if i != -1:
                j = self.obsidian[n].find("]]")
                file = self.obsidian[n][i + 3:j]
                title = self.obsidian[n][i + 3:self.obsidian[n].find('.')]
                self.obsidian[n] = self.obsidian[n].replace(self.obsidian[n][i:j + 2],
                                                            f"![{title}]({self.pic_path}/{file})",
                                                            1)
        self.__del_first_blank_line()

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
                while self.obsidian[j][0] == '>':
                    self.obsidian[j] = self.obsidian[j].replace('>', '', 1)
                    if self.obsidian[j][0] == ' ':
                        self.obsidian[j] = self.obsidian[j][1:]
                    if j < len(self.obsidian) - 1:
                        j += 1
                    else:
                        break
                self.obsidian.insert(j+1, "{{< /admonition >}}")
            n += 1
        self.__del_first_blank_line()

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
        self.__del_first_blank_line()


if __name__ == '__main__':
    f = open("test/t1.md").readlines()
    c = Convert(f, "C:/")
    # p = c.convert(is_sep=True, is_pic=True, is_adm=True)
    c.test()
    print(c.obsidian)
