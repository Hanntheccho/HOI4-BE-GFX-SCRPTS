import re
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

def process_file(path: Path):
    text = path.read_text(encoding="utf-8")

    # Regex to match province blocks with naval_base only
    pattern = re.compile(r'(\d+)=\{\s*naval_base=(\d+)\s*\}', re.MULTILINE)

    # Replacement with no spaces inside
    new_text = pattern.sub(r'\1={naval_base=\2}', text)

    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        print(f"Updated: {path}")
    else:
        print(f"No change: {path}")

def main():
    # Hide the main Tk window
    root = tk.Tk()
    root.withdraw()

    folder = filedialog.askdirectory(title="Select folder with text files")
    if not folder:
        messagebox.showinfo("Cancelled", "No folder selected. Exiting.")
        return

    root = Path(folder)
    changed = 0
    for path in root.rglob("*.txt"):  # adjust extension if needed
        before = path.read_text(encoding="utf-8")
        after = re.sub(r'(\d+)=\{\s*naval_base=(\d+)\s*\}', r'\1={naval_base=\2}', before, flags=re.MULTILINE)
        if before != after:
            path.write_text(after, encoding="utf-8")
            print(f"Updated: {path}")
            changed += 1

    messagebox.showinfo("Done", f"Processed {changed} file(s).")

if __name__ == "__main__":
    main()
