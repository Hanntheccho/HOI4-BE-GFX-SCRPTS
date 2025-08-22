import os
import re

# Folder to process
folder_path = r"C:\Users\jmgp0\Documents\Paradox Interactive\Hearts of Iron IV\mod\Beyond Earth\interface"

# Regex to match lines with empty textureFile (any indentation)
pattern = re.compile(r'^\s*textureFile\s*=\s*""\s*$')

# Process only .gfx and .gui files
target_extensions = (".gfx", ".gui")

for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(target_extensions):
            file_path = os.path.join(root, file)

            # Read file
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Filter out unwanted lines
            new_lines = [line for line in lines if not pattern.match(line)]

            # Overwrite only if changes were made
            if new_lines != lines:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                print(f"Cleaned: {file_path}")

print("✅ All .gfx and .gui files cleaned!")
