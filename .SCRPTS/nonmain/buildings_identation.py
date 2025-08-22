import re
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

def fix_buildings(path: Path):
    text = path.read_text(encoding="utf-8")

    # Match 'buildings={ ... }' block and fix the last closing brace indentation
    fixed = re.sub(
        r'(buildings=\{[\s\S]*?)\n\s*\}',
        lambda m: m.group(1) + "\n\t\t}",
        text
    )

    if fixed != text:
        path.write_text(fixed, encoding="utf-8")
        print(f"Fixed: {path}")
        return True
    return False

def main():
    root = tk.Tk()
    root.withdraw()

    folder = filedialog.askdirectory(title="Select folder with text files")
    if not folder:
        messagebox.showinfo("Cancelled", "No folder selected. Exiting.")
        return

    changed = 0
    for f in Path(folder).rglob("*.txt"):  # adjust extension if needed
        if fix_buildings(f):
            changed += 1

    messagebox.showinfo("Done", f"Processed {changed} file(s).")

if __name__ == "__main__":
    main()
