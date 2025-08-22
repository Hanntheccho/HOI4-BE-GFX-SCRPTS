import os
import re

folder = r"c:\Users\jmgp0\Documents\Paradox Interactive\Hearts of Iron IV\mod\Beyond Earth\map\strategicregions"

# This pattern matches a line with only 'weather = {' (with any whitespace), a line with only '}' (with any whitespace), and removes them both, preserving the next line's indentation.
pattern = re.compile(
    r'^[ \t]*weather\s*=\s*\{\s*\r?\n[ \t]*\}\s*\r?\n', re.MULTILINE
)

for filename in os.listdir(folder):
    if filename.endswith('.txt'):
        path = os.path.join(folder, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = pattern.sub('', content)
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)