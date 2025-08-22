import os
import re


folder = r"history\states"  # relative to your mod folder

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
        if re.match(r'\s*victory_points\s*=\s*{', line):
            # Start collecting victory point entries
            vp_line = line.strip()
            vp_entries = []
            # If there are entries on the same line, collect them
            match = re.match(r'\s*victory_points\s*=\s*{(.*)', line)
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
                vp_entries.append(l)
                i += 1
            # Write victory_points in one line
            new_lines.append(f'\t\tvictory_points={{ {" ".join(vp_entries)} }}\n')
            # Skip the closing }
            i += 1
        else:
            new_lines.append(line)
            i += 1

    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

print("Done! All victory_points are now in a single line in each file.")
