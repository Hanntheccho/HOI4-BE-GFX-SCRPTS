import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# Mapping state_category to air_base value
def state_category_to_air_base(category):
    match = re.match(r'state_(\d+)', category)
    if match:
        return match.group(1)
    return None

# Function to select folders
def select_folder(title):
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title=title)
    root.destroy()
    return folder

# Popup log window
class LogWindow:
    def __init__(self, title):
        self.root = tk.Tk()
        self.root.title(title)
        self.text = scrolledtext.ScrolledText(self.root, width=100, height=30)
        self.text.pack()
    
    def log(self, message):
        self.text.insert(tk.END, message + "\n")
        self.text.see(tk.END)
        self.root.update()
    
    def show(self):
        self.root.mainloop()

# Choose folders via popup
folder_a = select_folder("Select Folder A (OOB files)")
folder_b = select_folder("Select Folder B (State files)")

if not folder_a or not folder_b:
    messagebox.showerror("Error", "You must select both folders!")
    exit()

# Create log window
log_win = LogWindow("Script Log")

# Process files
for filename in os.listdir(folder_a):
    # Check _OOB ignoring extension
    if not os.path.splitext(filename)[0].upper().endswith("_OOB"):
        log_win.log(f"Skipping {filename}: not an _OOB file")
        continue

    file_path = os.path.join(folder_a, filename)
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Find air_wings block
    air_wings_match = re.search(r"air_wings\s*=\s*\{(.*?)\}\s*$", content, re.DOTALL)
    if not air_wings_match:
        log_win.log(f"No air_wings block in {filename}")
        continue
    
    air_wings_content = air_wings_match.group(1)
    
    # Extract all leading numbers (state IDs) and ignore 0,1
    state_ids = [sid for sid in re.findall(r"(\d+)\s*=\s*\{", air_wings_content) if int(sid) > 1]
    
    if not state_ids:
        log_win.log(f"No valid state IDs found in air_wings of {filename}")
        continue
    
    log_win.log(f"{filename}: found state IDs {state_ids}")
    
    for state_id in state_ids:
        state_file = os.path.join(folder_b, f"{state_id}.txt")
        if not os.path.exists(state_file):
            log_win.log(f"File {state_file} not found.")
            continue
        
        with open(state_file, "r") as f:
            state_content = f.read()
        
        # Find state_category
        category_match = re.search(r"state_category\s*=\s*(state_\d+)", state_content)
        if not category_match:
            log_win.log(f"No state_category found in {state_file}")
            continue
        
        air_base_value = state_category_to_air_base(category_match.group(1))
        if not air_base_value:
            log_win.log(f"Invalid state_category in {state_file}")
            continue
        
        # Update buildings block: add air_base on a new line
        def add_air_base(match):
            buildings_content = match.group(1).rstrip()
            buildings_content += f"\nair_base={air_base_value}"
            return f"buildings={{ {buildings_content} }}"

        new_content, count = re.subn(r"buildings\s*=\s*\{(.*?)\}", add_air_base, state_content, flags=re.DOTALL)
        
        if count > 0:
            with open(state_file, "w") as f:
                f.write(new_content)
            log_win.log(f"Updated air_base in {state_file} to {air_base_value}")
        else:
            log_win.log(f"No buildings block found in {state_file}")

log_win.log("Processing complete!")
log_win.show()
