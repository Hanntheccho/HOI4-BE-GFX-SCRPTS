import os
import re
import tkinter as tk
from tkinter import filedialog

def rename_files():
    root = tk.Tk()
    root.withdraw()

    folder = filedialog.askdirectory(title="Select folder with TAG_2200.txt files")
    if not folder:
        print("No folder selected.")
        return

    # Regex to match 3 uppercase letters + _2200.txt
    pattern = re.compile(r'^([A-Z]{3})_2200\.txt$')

    for filename in os.listdir(folder):
        match = pattern.match(filename)
        if match:
            tag = match.group(1)
            old_path = os.path.join(folder, filename)
            new_name = f"{tag}_OOB.txt"
            new_path = os.path.join(folder, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} → {new_name}")

    print("Renaming complete.")

if __name__ == "__main__":
    rename_files()
