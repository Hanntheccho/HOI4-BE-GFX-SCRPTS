import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Only keep these extensions
allowed_extensions = {'.tga', '.dds', '.png'}

# Tkinter setup
root = tk.Tk()
root.withdraw()  # Hide main window

# Select folder
folder_path = filedialog.askdirectory(title="Select folder to clean")
if not folder_path:
    messagebox.showinfo("Cancelled", "No folder selected. Exiting.")
    exit()

# Confirm deletion
if not messagebox.askyesno("Confirm Deletion",
                           "This will permanently delete all files except: {}. Continue?".format(
                               ", ".join(allowed_extensions))):
    exit()

# Delete disallowed files
deleted_files = []
failed_files = []

for foldername, subfolders, filenames in os.walk(folder_path):
    for filename in filenames:
        ext = os.path.splitext(filename)[1].lower()
        if ext not in allowed_extensions:
            file_path = os.path.join(foldername, filename)
            try:
                os.remove(file_path)
                deleted_files.append(file_path)
            except Exception as e:
                failed_files.append((file_path, str(e)))

# Summary popup
summary = "Deleted files: {}\nFailed deletions: {}".format(len(deleted_files), len(failed_files))
messagebox.showinfo("Cleaning Complete", summary)
