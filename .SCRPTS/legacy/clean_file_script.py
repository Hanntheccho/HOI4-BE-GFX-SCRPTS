import os
import re
import tkinter as tk
from tkinter import filedialog

def replace_spaces_with_tabs(content: str) -> str:
    """Replace sequences of four spaces with a tab."""
    return content.replace(" " * 4, "\t")

def clean_content(content: str) -> str:
    """
    Clean content:
      - Remove comments starting with '#'
      - Strip lines and drop empty lines
      - Normalize spaces around '=' to ' = ' (avoid touching '==', '>=', '<=', '!=', '=>', ':=')
      - Add a space after '{' and before '}' when brace shares the line with other content
      - Re-indent blocks with tabs using { and }
      - Ensure exactly one trailing newline at file end
    """
    # Remove comments (# and everything after on the same line)
    content = re.sub(r"#.*", "", content)

    # Strip leading/trailing whitespace on each line
    lines = [line.strip() for line in content.splitlines()]

    # Remove empty lines
    lines = [line for line in lines if line]

    cleaned = []
    for line in lines:
        # Normalize spaces around '=' (single '=' only)
        # Avoid modifying operators like '==', '>=', '<=', '!=', '=>', ':='
        line = re.sub(r"(?<![=!<>:])\s*=\s*(?![=<>])", " = ", line)

        # Add exactly one space AFTER '{' if more content follows on the same line
        # Example: '{x' -> '{ x', '{   x' -> '{ x', but '{' at EOL remains '{'
        line = re.sub(r"\{\s*(?=\S)", "{ ", line)

        # Add exactly one space BEFORE '}' if there is content earlier on the same line
        # Example: 'x}' -> 'x }', 'x   }' -> 'x }', but a line that's only '}' stays unchanged
        line = re.sub(r"(?<=\S)\s*\}", " }", line)

        cleaned.append(line)

    # Re-indent blocks with tabs based on { and }
    reindented = []
    indent_level = 0
    for line in cleaned:
        # If the line is exactly '}', reduce indent before placing it
        if line == "}":
            indent_level -= 1
            if indent_level < 0:
                indent_level = 0  # safety

        reindented.append("\t" * indent_level + line)

        # If the line ends with '{' (no trailing space), increase indent for following lines
        if line.endswith("{"):
            indent_level += 1

    # Ensure file ends with exactly one newline
    return "\n".join(reindented).rstrip() + "\n"

def process_file(file_path: str):
    """Process a file by replacing spaces with tabs and cleaning."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace spaces with tabs
        new_content = replace_spaces_with_tabs(content)

        # Clean content for all files
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
    # Hide root Tkinter window
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
