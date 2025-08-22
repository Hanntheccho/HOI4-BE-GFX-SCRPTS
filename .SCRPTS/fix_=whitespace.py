import os
import re
import sys
import tkinter as tk
from tkinter import filedialog

def normalize_equals_outside_strings(line: str) -> str:
    result = []
    in_single = False
    in_double = False
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == '"' and not in_single:
            in_double = not in_double
            result.append(ch)
        elif ch == "'" and not in_double:
            in_single = not in_single
            result.append(ch)
        elif ch == "=" and not (in_single or in_double):
            prev = line[i - 1] if i > 0 else ""
            nxt = line[i + 1] if i + 1 < len(line) else ""
            if prev not in "=!<>:" and nxt not in "=<>":
                while result and result[-1] == " ":
                    result.pop()
                result.append(" = ")
                j = i + 1
                while j < len(line) and line[j] == " ":
                    j += 1
                i = j
                continue
            else:
                result.append(ch)
        else:
            result.append(ch)
        i += 1
    return "".join(result)

def fix_whitespace(content: str) -> str:
    lines = content.splitlines()
    fixed = []
    for line in lines:
        # Skip processing if the line contains a comment
        if "#" in line:
            fixed.append(line)
            continue

        line = normalize_equals_outside_strings(line)
        line = re.sub(r"\{\s*(?=\S)", "{ ", line)   # space after {
        line = re.sub(r"(?<=\S)\s*\}", " }", line)  # space before }
        fixed.append(line)

    return "\n".join(fixed) + "\n"

def process_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = fix_whitespace(content)

    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Fixed whitespace in {path}")
    else:
        print(f"No changes in {path}")

def main():
    root = tk.Tk()
    root.withdraw()

    folder = filedialog.askdirectory(title="Select folder to fix whitespace")
    if not folder:
        print("No folder selected. Exiting...")
        sys.exit(0)

    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            process_file(os.path.join(dirpath, filename))

    print("Whitespace fixing complete.")

if __name__ == "__main__":
    main()
