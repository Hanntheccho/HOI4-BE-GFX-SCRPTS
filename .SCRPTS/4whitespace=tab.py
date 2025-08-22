import os
import tkinter as tk
from tkinter import filedialog

def replace_spaces_with_tabs_in_file(file_path):
    """Replaces four spaces with a tab in the given file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        new_content = content.replace(" " * 4, "\t")
        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated: {file_path}")
        else:
            print(f"No changes: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    # Hide root Tkinter window
    root = tk.Tk()
    root.withdraw()

    # Ask user to pick a folder
    folder = filedialog.askdirectory(title="Select Folder Containing Files")
    if not folder:
        print("No folder selected. Exiting...")
        return

    # Walk through all files in the selected folder
    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            replace_spaces_with_tabs_in_file(file_path)

    print("Processing complete.")

if __name__ == "__main__":
    main()
