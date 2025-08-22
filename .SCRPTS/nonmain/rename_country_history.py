import os
import re
import tkinter as tk
from tkinter import filedialog

def rename_files():
    root = tk.Tk()
    root.withdraw()

    folder = filedialog.askdirectory(title="Select folder with files to rename")
    if not folder:
        print("No folder selected.")
        return

    # Regex to match TAG - anything, capture the extension separately
    pattern = re.compile(r'^([A-Z]{3}) - .+(\.[^.]+)$')  # ensures extension is captured

    for filename in os.listdir(folder):
        match = pattern.match(filename)
        if match:
            tag = match.group(1)
            ext = match.group(2)  # this will always capture the extension
            old_path = os.path.join(folder, filename)
            new_name = f"{tag}_2200{ext}"
            new_path = os.path.join(folder, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} → {new_name}")

    print("Renaming complete.")

if __name__ == "__main__":
    rename_files()
