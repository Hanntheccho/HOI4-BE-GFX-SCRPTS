import os
import re
import tkinter as tk
from tkinter import filedialog

def clean_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove comments (# and everything after on the same line)
    content = re.sub(r"#.*", "", content)

    # Strip leading/trailing whitespace on each line
    lines = [line.strip() for line in content.splitlines()]

    # Remove empty lines
    lines = [line for line in lines if line]

    # Remove spaces around '='
    lines = [re.sub(r"\s*=\s*", "=", line) for line in lines]

    # Re-indent blocks with tabs
    cleaned_lines = []
    indent_level = 0
    for line in lines:
        if line == "}":
            indent_level -= 1

        cleaned_lines.append("\t" * indent_level + line)

        if line.endswith("{"):
            indent_level += 1

    # Join back into a single string
    new_content = "\n".join(cleaned_lines) + "\n"

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)

def main():
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Select folder with files")
    if not folder:
        print("No folder selected. Exiting.")
        return

    for filename in os.listdir(folder):
        if not filename.lower().endswith(".txt"):
            continue
        filepath = os.path.join(folder, filename)
        try:
            clean_file(filepath)
            print(f"Cleaned: {filename}")
        except Exception as e:
            print(f"Error in {filename}: {e}")

    print("All files cleaned.")

if __name__ == "__main__":
    main()
