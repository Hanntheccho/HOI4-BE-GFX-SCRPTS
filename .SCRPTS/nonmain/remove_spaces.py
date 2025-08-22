import os
import re

folder = r"c:\Users\jmgp0\Documents\Paradox Interactive\Hearts of Iron IV\mod\Beyond Earth\history\states"

for filename in os.listdir(folder):
    if filename.endswith(".txt"):
        path = os.path.join(folder, filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        # Remove spaces before and after '='
        new_content = re.sub(r'\s*=\s*', '=', content)
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
