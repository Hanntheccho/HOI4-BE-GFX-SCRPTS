import re
import os
import tkinter as tk
from tkinter import filedialog

# Regex: match a line that starts with optional whitespace, "oob", "=", then the rest of the line
# and include the EOL (either \n or \r\n) or EOF so it works even if there's no trailing newline.
OOB_PATTERN = re.compile(r"^\s*oob\s*=.*(?:\r?\n|$)", re.MULTILINE)

def remove_oob_from_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove BOM if present (helps when file starts with \ufeff)
    if content.startswith("\ufeff"):
        content = content.lstrip("\ufeff")

    new_content = re.sub(OOB_PATTERN, "", content)

    # If removal left a leading newline(s) at the start of the file, strip them.
    # (Optional — keeps files tidy when the first line was removed.)
    new_content = new_content.lstrip("\r\n")

    if new_content != content:
        # Write back (using utf-8). newline='' helps preserve the platform newline style.
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new_content)
        return True
    return False

def main():
    # Hide root window and ask for folder
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Select folder with files")
    if not folder:
        print("No folder selected. Exiting.")
        return

    changed_count = 0
    for fn in os.listdir(folder):
        if not fn.lower().endswith(".txt"):  # adjust extension if needed
            continue
        full = os.path.join(folder, fn)
        try:
            if remove_oob_from_file(full):
                print(f"Removed oob in: {fn}")
                changed_count += 1
            else:
                print(f"No oob found: {fn}")
        except Exception as e:
            print(f"Error processing {fn}: {e}")

    print(f"Done. Files changed: {changed_count}")

if __name__ == "__main__":
    main()
