import os
import sys
import tkinter as tk
from tkinter import filedialog

def remove_comments(content: str) -> str:
    lines = content.splitlines()
    # Keep only lines that are not comments (ignore leading whitespace)
    non_comment_lines = [line for line in lines if not line.lstrip().startswith("#")]
    # Always end with exactly one newline
    return "\n".join(non_comment_lines) + "\n"

def process_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = remove_comments(content)

    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Removed comments in {path}")
    else:
        print(f"No changes in {path}")

def main():
    root = tk.Tk()
    root.withdraw()

    folder = filedialog.askdirectory(title="Select folder to remove comments")
    if not folder:
        print("No folder selected. Exiting...")
        sys.exit(0)

    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            process_file(os.path.join(dirpath, filename))

    print("Comment removal complete.")

if __name__ == "__main__":
    main()
