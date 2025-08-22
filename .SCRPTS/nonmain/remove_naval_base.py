import tkinter as tk
from tkinter import filedialog

# Hide the root Tk window
root = tk.Tk()
root.withdraw()

# Ask the user to select a file
file_path = filedialog.askopenfilename(title="Select file to clean", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

if file_path:
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if ';naval_base;' not in line:
                file.write(line)

    print("Lines with 'naval_base' removed successfully.")
else:
    print("No file selected.")
