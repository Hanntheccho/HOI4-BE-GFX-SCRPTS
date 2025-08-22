import os
import tkinter as tk
from tkinter import filedialog

def trim_empty_lines(file_path):
    """Remove blank lines at the start and end of a text file (keeps internal blanks)."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        # Skip likely binary files
        if "\x00" in content:
            print(f"Skipped (binary?): {file_path}")
            return

        # Split into logical lines (no newline chars kept)
        lines = content.splitlines()

        # Trim leading and trailing blank/whitespace-only lines
        start = 0
        end = len(lines)
        while start < end and lines[start].strip() == "":
            start += 1
        while end > start and lines[end - 1].strip() == "":
            end -= 1

        trimmed = "\n".join(lines[start:end])  # no trailing newline

        if trimmed != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(trimmed)
            print(f"Trimmed: {file_path}")
        else:
            print(f"No changes: {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    root = tk.Tk()
    root.withdraw()

    folder = filedialog.askdirectory(title="Select Folder Containing Files")
    if not folder:
        print("No folder selected. Exiting...")
        return

    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            trim_empty_lines(file_path)

    print("Processing complete.")

if __name__ == "__main__":
    main()
