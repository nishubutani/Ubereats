import re


class Utility():

    def Beautifier(newline):
        d = re.sub(r'\n{4, 50}','\n', newline)
        d = re.sub(r'\n{3}', '\n', d)
        des = re.sub(r'(\n\s*)+\n+', '\n\n', d).replace('#','').strip()
        return des.strip()