import os
import re
import tkinter as tk
from tkinter import filedialog

def replace_spaces_with_tabs(content: str) -> str:
    """Replace sequences of four spaces with a tab."""
    return content.replace(" " * 4, "\t")

def normalize_equals_outside_strings(line: str) -> str:
    """
    Normalize spaces around '=' (single '=' only) but skip if inside quotes.
    """
    result = []
    in_single = False
    in_double = False
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == '"' and not in_single:
            in_double = not in_double
            result.append(ch)
        elif ch == "'" and not in_double:
            in_single = not in_single
            result.append(ch)
        elif ch == "=" and not (in_single or in_double):
            # Check that it's not part of ==, >=, <=, !=, =>, :=
            prev = line[i - 1] if i > 0 else ""
            nxt = line[i + 1] if i + 1 < len(line) else ""
            if prev not in "=!<>:" and nxt not in "=<>":
                # normalize spaces around '='
                # eat any surrounding spaces
                while result and result[-1] == " ":
                    result.pop()
                result.append(" = ")
                # skip spaces after '='
                j = i + 1
                while j < len(line) and line[j] == " ":
                    j += 1
                i = j
                continue
            else:
                result.append(ch)
        else:
            result.append(ch)
        i += 1
    return "".join(result)

def clean_content(content: str) -> str:
    """
    Clean content:
      - Remove leading empty lines
      - Remove trailing empty lines (always end with exactly one newline)
      - Normalize spaces around '=' outside of strings
      - Add a space after '{' and before '}' when brace shares the line with other content
      - Re-indent blocks with tabs using { and }
    """
    # Strip trailing whitespace, but keep empty lines
    lines = [line.rstrip() for line in content.splitlines()]

    cleaned = []
    for line in lines:
        # Normalize '=' only outside of strings
        line = normalize_equals_outside_strings(line)

        # Add exactly one space AFTER '{' if more content follows on the same line
        line = re.sub(r"\{\s*(?=\S)", "{ ", line)

        # Add exactly one space BEFORE '}' if there is content earlier on the same line
        line = re.sub(r"(?<=\S)\s*\}", " }", line)

        cleaned.append(line)

    # Re-indent blocks with tabs based on { and }
    reindented = []
    indent_level = 0
    for line in cleaned:
        stripped = line.strip()

        if stripped == "}":
            indent_level -= 1
            if indent_level < 0:
                indent_level = 0

        if stripped:
            reindented.append("\t" * indent_level + stripped)
        else:
            reindented.append("")

        if stripped.endswith("{"):
            indent_level += 1

    # Remove leading empty lines
    while reindented and reindented[0] == "":
        reindented.pop(0)

    # Remove trailing empty lines
    while reindented and reindented[-1] == "":
        reindented.pop()

    # Ensure file ends with exactly one newline
    return "\n".join(reindented) + "\n"

def process_file(file_path: str):
    """Process a file by replacing spaces with tabs and cleaning."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = replace_spaces_with_tabs(content)
        new_content = clean_content(new_content)

        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated: {file_path}")
        else:
            print(f"No changes: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    root = tk.Tk()
    root.withdraw()

    folder = filedialog.askdirectory(title="Select folder with files")
    if not folder:
        print("No folder selected. Exiting...")
        return

    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            process_file(file_path)

    print("Processing complete.")

if __name__ == "__main__":
    main()
