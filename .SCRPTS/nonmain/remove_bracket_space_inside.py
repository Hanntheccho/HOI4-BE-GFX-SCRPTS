import os
import re

folder = r"map\strategicregions"  # relative to your mod folder

for filename in os.listdir(folder):
    if not filename.endswith('.txt'):
        continue
    path = os.path.join(folder, filename)
    with open(path, encoding='utf-8') as f:
        content = f.read()

    # Remove space(s) after an opening bracket ({ or [)
    content = re.sub(r'([\{\[]) +', r'\1', content)
    # Remove space(s) before a closing bracket (} or ])
    content = re.sub(r' +([\}\]])', r'\1', content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done! Removed spaces after opening and before closing brackets in each file.")
