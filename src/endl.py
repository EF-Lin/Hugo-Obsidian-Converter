def str_endl(s: str):
    if s[-1] != '\n':
        return s + '\n'
    else:
        while s[-2] == '\n' and s[-1] == '\n':
            s = s[:-1]
        return s

def del_first_blank_line(data: list):
    while data[0] == '\n':
        data.pop(0)
    return data
