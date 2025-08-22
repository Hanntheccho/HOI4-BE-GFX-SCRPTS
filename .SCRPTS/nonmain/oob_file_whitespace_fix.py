import os
import tkinter as tk
from tkinter import filedialog

def clean_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    for line in lines:
        # Remove comments
        line = line.split('#')[0]
        # Remove leading/trailing whitespace and collapse multiple spaces to single space
        line = ' '.join(line.strip().split())
        # Remove spaces around '='
        line = line.replace(' = ', '=')
        # Remove spaces after '{' and before '}'
        line = line.replace('{ ', '{').replace(' }', '}')
        # Skip empty lines
        if line:
            cleaned_lines.append(line)

    # Keep one empty line at start and end
    cleaned_content = '\n' + '\n'.join(cleaned_lines) + '\n'

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)

def main():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select folder with files to clean")
    if not folder_path:
        print("No folder selected. Exiting.")
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            clean_file(file_path)
            print(f"Cleaned: {filename}")

    print("All files cleaned.")

if __name__ == "__main__":
    main()
