import os
import subprocess
from tkinter import Tk, filedialog

# Hide the main Tkinter window
Tk().withdraw()

# Ask the user to select a folder
folder_path = filedialog.askdirectory(title="Select Folder to Format")

if not folder_path:
    print("No folder selected. Exiting.")
    exit()

# Walk through the folder recursively
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(".txt"):
            file_path = os.path.join(root, file)
            print(f"Formatting: {file_path}")
            subprocess.run(["autopep8", "--in-place", "--aggressive", "--aggressive", file_path])

print("Formatting complete.")
