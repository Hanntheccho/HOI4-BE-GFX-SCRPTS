import re
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

# Regex matches fighter|CAS equipment with owner/amount inside,
# followed optionally by a name = "...".
pattern = re.compile(r"""
(?P<prefix>(?:fighter|CAS)_equipment_\d+)\s*=\s*\{\s*
(?:  # Case A: owner first
    owner\s*=\s*(?:"(?P<owner>[A-Z]{3})"|(?P<owner_u>[A-Z]{3}))\s*
    amount\s*=\s*(?P<amount>(?:1000|[0-9]{1,3}))
  |
    # Case B: amount first
    amount\s*=\s*(?P<amount2>(?:1000|[0-9]{1,3}))\s*
    owner\s*=\s*(?:"(?P<owner2>[A-Z]{3})"|(?P<owner2_u>[A-Z]{3}))
)
\s*\}
(?:\s*name\s*=\s*"(?P<name>[^"]+)")?
""", re.VERBOSE)

def transform_content(text: str):
    """Return (new_text, replacements_count)."""

    def repl(m: re.Match) -> str:
        prefix = m.group("prefix")
        owner = m.group("owner") or m.group("owner_u") or m.group("owner2") or m.group("owner2_u")
        amount = m.group("amount") or m.group("amount2")
        name = m.group("name")

        if name:
            # equipment block + name outside
            return f'{prefix} = {{ owner = "{owner}" amount = {amount} }} name = "{name}"'
        else:
            return f'{prefix} = {{ owner = "{owner}" amount = {amount} }}'

    return pattern.subn(repl, text)

def process_file(path: Path) -> int:
    try:
        original = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        original = path.read_text(encoding="latin-1")

    transformed, n = transform_content(original)
    if n:
        path.write_text(transformed, encoding="utf-8")
        print(f"Transformed {n} block(s): {path}")
    else:
        print(f"No change: {path}")
    return n

def main():
    root = tk.Tk()
    root.withdraw()

    folder = filedialog.askdirectory(title="Select folder with equipment files")
    if not folder:
        messagebox.showinfo("Cancelled", "No folder selected.")
        return

    folder_path = Path(folder)
    total_changes = 0
    file_count = 0

    for file in folder_path.rglob("*.txt"):
        file_count += 1
        total_changes += process_file(file)

    messagebox.showinfo(
        "Done",
        f"Processed {file_count} file(s) in:\n{folder}\n\n"
        f"Rewrote {total_changes} equipment block(s)."
    )

if __name__ == "__main__":
    main()
