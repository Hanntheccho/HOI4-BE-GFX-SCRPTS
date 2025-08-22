import os
import re
import tkinter as tk
from tkinter import filedialog

def parse_block(text):
    """Parses a block like state={...} into a dict preserving nested blocks."""
    stack = []
    current = {}
    key = None
    buffer = ""

    i = 0
    while i < len(text):
        if text[i] == "{":
            stack.append((current, key))
            new_block = {}
            if key:
                # If the key already exists, make it a list
                if key in current:
                    if isinstance(current[key], list):
                        current[key].append(new_block)
                    else:
                        current[key] = [current[key], new_block]
                else:
                    current[key] = new_block
            current, key = new_block, None
            i += 1
        elif text[i] == "}":
            if buffer.strip():
                if key:
                    current[key] = buffer.strip()
                buffer = ""
                key = None
            current, key = stack.pop()
            i += 1
        elif text[i] == "\n":
            if buffer.strip():
                parts = buffer.strip().split("=", 1)
                if len(parts) == 2:
                    current[parts[0].strip()] = parts[1].strip()
                else:
                    current[parts[0].strip()] = None
            buffer = ""
            key = None
            i += 1
        else:
            buffer += text[i]
            if "=" in buffer and not key:
                parts = buffer.split("=", 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    buffer = parts[1]
            i += 1
    return current

def format_block(d, indent=1, history=False):
    """Format dict back into Paradox-style text with ordering rules."""
    lines = []
    prefix = "\t" * indent

    if history:
        # Custom order for history
        order = ["owner", "add_core_of", "buildings"]
        for key in order:
            if key in d:
                val = d[key]
                if isinstance(val, dict):
                    lines.append(f"{prefix}{key}={{")
                    lines.extend(format_block(val, indent+1, history=False))
                    lines.append(f"{prefix}}}")
                elif isinstance(val, list):
                    for item in val:
                        lines.append(f"{prefix}{key}={item}")
                else:
                    lines.append(f"{prefix}{key}={val}")
        # Victory points after buildings
        if "victory_points" in d:
            val = d["victory_points"]
            if isinstance(val, list):
                for vp in val:
                    lines.append(f"{prefix}victory_points={{{vp}}}")
            else:
                lines.append(f"{prefix}victory_points={{{val}}}")
        # Add everything else
        for k, v in d.items():
            if k not in order and k != "victory_points":
                if isinstance(v, dict):
                    lines.append(f"{prefix}{k}={{")
                    lines.extend(format_block(v, indent+1))
                    lines.append(f"{prefix}}}")
                else:
                    lines.append(f"{prefix}{k}={v}")
    else:
        for k, v in d.items():
            if isinstance(v, dict):
                lines.append(f"{prefix}{k}={{")
                lines.extend(format_block(v, indent+1, history=(k=="history")))
                lines.append(f"{prefix}}}")
            elif isinstance(v, list):
                for item in v:
                    lines.append(f"{prefix}{k}={item}")
            else:
                lines.append(f"{prefix}{k}={v}")
    return lines

def reorder_state(state_dict):
    """Reorder state-level keys as requested."""
    order = ["id", "name", "manpower", "state_category", "history", "provinces"]
    reordered = {}
    for k in order:
        if k in state_dict:
            reordered[k] = state_dict[k]
    for k, v in state_dict.items():
        if k not in order:
            reordered[k] = v
    return reordered

def process_file(filepath, outpath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r"state\s*=\s*\{([\s\S]*)\}", content)
    if not match:
        print(f"Skipping {filepath}: no state block found")
        return

    body = match.group(1)
    parsed = parse_block(body)
    reordered = reorder_state(parsed)

    output_lines = ["state={"]
    output_lines.extend(format_block(reordered))
    output_lines.append("}")

    with open(outpath, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

def main():
    root = tk.Tk()
    root.withdraw()
    input_folder = filedialog.askdirectory(title="Select folder with state files")
    if not input_folder:
        print("No folder selected, exiting.")
        return

    output_folder = os.path.join(input_folder, "sorted_states")
    os.makedirs(output_folder, exist_ok=True)

    for fname in os.listdir(input_folder):
        if fname.endswith(".txt"):
            inpath = os.path.join(input_folder, fname)
            outpath = os.path.join(output_folder, fname)
            process_file(inpath, outpath)
            print(f"Processed {fname}")

if __name__ == "__main__":
    main()
