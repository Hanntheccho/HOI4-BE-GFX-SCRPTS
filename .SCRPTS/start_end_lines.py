import os
import sys
import tkinter as tk
from tkinter import filedialog

def fix_newlines(content: str) -> str:
    lines = content.splitlines()

    # Remove leading empty lines
    while lines and not lines[0].strip():
        lines.pop(0)

    # Remove trailing empty lines
    while lines and not lines[-1].strip():
        lines.pop()

    return "\n".join(lines) + "\n"  # always end with exactly one newline

def process_file(path: str):
    with open(path, "r", encoding="utf-8-sig") as f:
    content = f.read()

    new_content = fix_newlines(content)

    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Fixed newlines in {path}")
    else:
        print(f"No changes in {path}")

def main():
    root = tk.Tk()
    root.withdraw()

    folder = filedialog.askdirectory(title="Select folder to fix newlines")
    if not folder:
        print("No folder selected. Exiting...")
        sys.exit(0)

    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            process_file(os.path.join(dirpath, filename))

    print("Newline fixing complete.")

if __name__ == "__main__":
    main()
