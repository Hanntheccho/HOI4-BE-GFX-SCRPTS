import os
import sys
import tkinter as tk
from tkinter import filedialog

def replace_spaces_with_tabs(content: str) -> str:
    lines = content.splitlines()
    new_lines = []
    for line in lines:
        stripped = line.strip()
        # Skip replacing spaces in comment lines
        if stripped.startswith("#"):
            new_lines.append(line)
        else:
            new_lines.append(line.replace(" " * 4, "\t"))
    return "\n".join(new_lines)

def fix_indentation(content: str) -> str:
    lines = [line.rstrip() for line in content.splitlines()]

    reindented = []
    indent_level = 0
    for line in lines:
        stripped = line.strip()

        # Skip indentation adjustment for comment lines
        if stripped.startswith("#"):
            reindented.append(line)
            continue

        if stripped == "}":
            indent_level -= 1
            if indent_level < 0:
                indent_level = 0

        if stripped:
            reindented.append("\t" * indent_level + stripped)
        else:
            reindented.append("")

        if stripped.endswith("{"):
            indent_level += 1

    return "\n".join(reindented) + "\n"

def process_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = replace_spaces_with_tabs(content)
    new_content = fix_indentation(new_content)

    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Fixed indentation in {path}")
    else:
        print(f"No changes in {path}")

def main():
    root = tk.Tk()
    root.withdraw()

    folder = filedialog.askdirectory(title="Select folder to fix indentation")
    if not folder:
        print("No folder selected. Exiting...")
        sys.exit(0)

    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            process_file(os.path.join(dirpath, filename))

    print("Indentation fixing complete.")

if __name__ == "__main__":
    main()
