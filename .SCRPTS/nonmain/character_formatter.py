import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

# Pick input file
input_file = filedialog.askopenfilename(title="Select your leaders file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
if not input_file:
    print("No file selected. Exiting.")
    exit()

# Pick output file
output_file = filedialog.asksaveasfilename(title="Save the commented file as", defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
if not output_file:
    print("No output file selected. Exiting.")
    exit()

with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

output_lines = []
current_country = None

for line in lines:
    stripped = line.strip()

    # Only consider lines that define a leader, e.g., TAG_name = {
    if "=" in stripped and stripped.endswith("{"):
        # Get the country code (prefix before first underscore)
        country_code = stripped.split("_")[0]
        if country_code != current_country:
            # Insert comment block
            output_lines.append("#######")
            output_lines.append(f"## {country_code} ##")
            output_lines.append("#######")
            current_country = country_code

    output_lines.append(line.rstrip())

with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print(f"Done! Output written to {output_file}")
