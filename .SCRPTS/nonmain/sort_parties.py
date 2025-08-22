import tkinter as tk
from tkinter import filedialog

def sort_parties():
    # Hide the main tkinter window
    root = tk.Tk()
    root.withdraw()

    # Open a file picker dialog (now defaults to .yml)
    input_file = filedialog.askopenfilename(
        title="Select the parties file",
        filetypes=[("YAML files", "*.yml"), ("All files", "*.*")]
    )
    if not input_file:
        print("No file selected.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Keep header (like l_english:) at the top
    header = [line for line in lines if line.strip().startswith("l_")]
    entries = [line for line in lines if ":" in line and not line.strip().startswith("l_")]

    # Sort all entries alphabetically
    entries.sort()

    # Overwrite the same file
    with open(input_file, "w", encoding="utf-8") as f:
        for h in header:
            f.write(h.strip() + "\n")
        for line in entries:
            f.write(line.strip() + "\n")

    print(f"Sorting complete. File overwritten: {input_file}")


if __name__ == "__main__":
    sort_parties()
