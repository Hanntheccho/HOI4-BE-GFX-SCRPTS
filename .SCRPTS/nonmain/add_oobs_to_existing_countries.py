import os
import tkinter as tk
from tkinter import filedialog

def main():
    root = tk.Tk()
    root.withdraw()

    # Select Folder A (source with TAG_2200.txt files)
    folder_a = filedialog.askdirectory(title="Select source folder with TAG_2200.txt files")
    if not folder_a:
        print("No source folder selected.")
        return

    # Select Folder B (target with "TAG - Country" files)
    folder_b = filedialog.askdirectory(title="Select target folder with 'TAG - Country' files")
    if not folder_b:
        print("No target folder selected.")
        return

    # Collect tags and codes from Folder A
    tag_codes = []
    for file in os.listdir(folder_a):
        if file.endswith(".txt") and "_" in file:
            tag, rest = file.split("_", 1)
            code = rest.replace(".txt", "")
            if len(tag) == 3 and code.isdigit():  # enforce strict format
                tag_codes.append((tag, code))

    # Process each tag_code
    for tag, code in tag_codes:
        match_file = None
        for file in os.listdir(folder_b):
            if file.startswith(f"{tag} - "):  # Match by tag prefix
                match_file = os.path.join(folder_b, file)
                break

        if not match_file:
            print(f"No matching file found for {tag} in target folder.")
            continue

        # Prepare the line to add
        new_line = f'oob="{tag}_{code}"\n'

        # Read target file
        with open(match_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Append only if not already present
        if new_line not in lines:
            lines.append(new_line)
            with open(match_file, "w", encoding="utf-8") as f:
                f.writelines(lines)
            print(f'Updated: {match_file} with {new_line.strip()}')
        else:
            print(f'Skipped (already present): {match_file}')

    print("All matching files processed.")


if __name__ == "__main__":
    main()
