def list_endl(s: str) -> str:
    if s[-1] != '\n':
        return s + '\n'
    else:
        while s[-2] == '\n' and s[-1] == '\n':
            s = s[:-1]
        return s

def form_str_endl(s: str) -> str:
    while s[0] == '\n':
        s = s[1:]
    while s[-2] == '\n' and s[-1] == '\n':
        s = s[:-1]
    if s[-1] != '\n':
        s += '\n'
    return s

def del_list_first_endl(data: list) -> list:
    while data[0] == '\n':
        data.pop(0)
    return data
