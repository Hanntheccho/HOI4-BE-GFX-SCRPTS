import re
import os
import tkinter as tk
from tkinter import filedialog

# Hide the main tkinter root window
root = tk.Tk()
root.withdraw()

# Ask the user to pick a folder
folder_path = filedialog.askdirectory(title="Select folder with files")
if not folder_path:
    print("No folder selected. Exiting.")
    exit()

# Regex to match the set_technology block
pattern = re.compile(r"set_technology\s*=\s*\{.*?\}", re.DOTALL)

# Process all files in the selected folder
for filename in os.listdir(folder_path):
    if not filename.lower().endswith(".txt"):  # Adjust extension if needed
        continue

    file_path = os.path.join(folder_path, filename)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove the set_technology block
    new_content = re.sub(pattern, "", content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Processed: {filename}")

print("All files processed.")
