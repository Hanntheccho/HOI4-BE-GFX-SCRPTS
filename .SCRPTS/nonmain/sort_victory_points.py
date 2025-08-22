import os

input_file = "VICTORY_POINTS_l_english.yml"
output_file = "VICTORY_POINTS_l_english_sorted.yml"

with open(input_file, encoding="utf-8") as f:
    lines = f.readlines()

# Filter out comments and empty lines, keep header
header = []
entries = []
header_found = False
for line in lines:
    if not header_found:
        header.append(line)
        if line.strip() and not line.strip().startswith("#"):
            # First non-comment, non-empty line is the header
            header_found = True
    else:
        if line.strip() and not line.strip().startswith("#"):
            entries.append(line)
        else:
            # If there are comments or empty lines after the header, keep them with the entries
            entries.append(line)

# Only sort actual key-value lines (skip empty/comment lines)
kv_lines = [l for l in entries if l.strip() and not l.strip().startswith("#")]
other_lines = [l for l in entries if not (l.strip() and not l.strip().startswith("#"))]
import re
def extract_number(line):
    match = re.search(r"VICTORY_POINTS_(\d+)", line)
    return int(match.group(1)) if match else float('inf')
kv_lines.sort(key=extract_number)

with open(output_file, "w", encoding="utf-8") as f:
    f.writelines(header)
    f.writelines(other_lines)
    f.writelines(kv_lines)

print(f"Sorted file written to {output_file}")
