import os
import re

folder = r"map\strategicregions"  # relative to your mod folder

for filename in os.listdir(folder):
    if not filename.endswith('.txt'):
        continue
    path = os.path.join(folder, filename)
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r'\s*provinces\s*=\s*{', line):
            # Start collecting province IDs
            province_line = line.strip()
            province_ids = []
            # If there are IDs on the same line, collect them
            match = re.match(r'\s*provinces\s*=\s*{(.*)', line)
            if match and '}' in match.group(1):
                # All on one line already
                new_lines.append(line)
                i += 1
                continue
            i += 1
            while i < len(lines):
                l = lines[i].strip()
                if l == '}':
                    break
                province_ids.extend(l.split())
                i += 1
            # Write provinces in one line
            new_lines.append(f'\tprovinces={{ {" ".join(province_ids)} }}\n')
            # Skip the closing }
            i += 1
        else:
            new_lines.append(line)
            i += 1

    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

print("Done! All provinces are now in a single line in each file.")
