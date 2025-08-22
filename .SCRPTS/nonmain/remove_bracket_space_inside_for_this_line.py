import os
import re

folder = r"history/states"  # relative to your mod folder


for filename in os.listdir(folder):
    if not filename.endswith('.txt'):
        continue
    path = os.path.join(folder, filename)
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.lstrip().startswith('victory_points=') or line.lstrip().startswith('victory_points ='):
            # Remove space(s) after an opening bracket ({ or [) and before a closing bracket (} or ])
            line = re.sub(r'([\{\[]) +', r'\1', line)
            line = re.sub(r' +([\}\]])', r'\1', line)
        new_lines.append(line)

    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

print("Done! Removed spaces after opening and before closing brackets in each file.")
