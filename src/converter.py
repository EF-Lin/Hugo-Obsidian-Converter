from dataclasses import dataclass
import re
from src.endl import form_str_endl

@dataclass
class Convert:
    """
    This object will receive an obsidian-md.readlines list and return a converted hugo-md string.
    """
    obsidian: list
    pic_path: str = ""
    allow_chars = ['>', '<', '!', '[', '#', '-', '{', '(', '-', '\n']

    def __post_init__(self):
        if self.pic_path != "" and self.pic_path[-1] in ['/', '\\'] and len(self.pic_path) > 3:
            self.pic_path = self.pic_path[0:-1]
        self.obsidian: str = ''.join(self.obsidian)

    def convert(self, is_delcon=True,
                is_sep=True,
                is_pic = True,
                is_adm = True,
                is_highlight=True,
                is_link=True) -> str:
        try:
            self.__del_content() if is_delcon else 0
            self.__pic() if is_pic else 0
            self.__link() if is_link else 0
            self.__adm() if is_adm else 0
            self.__sep_code() if is_sep else 0
            self.__highlight() if is_highlight else 0
            return form_str_endl(self.obsidian)
        except Exception as ex:
            return str(ex)

    def _test(self):
        self.__del_content()
        self.__adm()
        self.__sep_code()

    def __del_content(self):
        self.obsidian = re.sub(r"```table-of-contents.*?```", "", self.obsidian, flags=re.DOTALL)

    def __pic(self):
        self.obsidian = re.sub(r"!\[\[(.*?)\.(.*?)\]\]", r"![\1](" + self.pic_path + r'/\1.\2 "\1")', self.obsidian)

    def __link(self):
        self.obsidian = re.sub(r"\[\[#*(.*?)\]\]", r"[\1](#\1)", self.obsidian)

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
        self.obsidian = re.sub(r"> *?\[!(.*?)\](.*?)\n\n", lambda s: f'{{{{< admonition type="{"tip" if s.group(1) == "hint" else s.group(1)}" title="{s.group(1).capitalize()}" >}}}}{s.group(2).replace('>', '')}\n{{{{< /admonition >}}}}\n\n', self.obsidian, flags=re.DOTALL)

    def __sep_code(self):
        self.obsidian = re.sub(r"```(.*?)\n", r"```\1{linenos=true}\n", self.obsidian)
        #self.obsidian = re.sub(r"```(.*?)\n", lambda s: r'```' if s.group(1)=='' else f"```{s.group(1)}{{linenos=true}}\n", self.obsidian)
        i = self.obsidian.find('\n')
        jump1 = -1
        jump2 = -1
        while i != -1 and i < len(self.obsidian)-1:
            jump1 = -jump1 if self.obsidian[i+1] == '`' else jump1
            jump2 = -jump2 if self.obsidian[i+1] == '{' else jump2
            if self.obsidian[i+1] not in self.allow_chars and self.obsidian[i-1] not in self.allow_chars and jump1 < 0 and jump2 < 0:
                self.obsidian = self.obsidian[:i+1] + '\n' + self.obsidian[i+1:]
            i = self.obsidian.find('\n', i+1)
        self.obsidian = re.sub(r"\n```{linenos=true}", r"```", self.obsidian)

    def __highlight(self):
        self.obsidian = re.sub(r"==(.*?)==", r"<mark>\1</mark>", self.obsidian)


if __name__ == '__main__':
    f = open("test/t1.md").readlines()
    c = Convert(f, "/post")
    #print(repr(c.obsidian))
    print(c.convert())
