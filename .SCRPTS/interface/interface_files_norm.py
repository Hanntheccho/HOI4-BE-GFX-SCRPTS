import os
import re
import sys
import tkinter as tk
from tkinter import filedialog

import re

def clean_attributes(content: str) -> str:
    lines = content.splitlines()
    cleaned = []

    # Regex patterns for removals/quotes
    orientation_remove_pattern = re.compile(r'orientation\s*=\s*["\']?UPPER_LEFT["\']?', re.IGNORECASE)
    orientation_quotes_pattern = re.compile(r'(orientation\s*=\s*)["\']([^"\']+)["\']', re.IGNORECASE)
    origo_quotes_pattern = re.compile(r'(origo\s*=\s*)["\']([^"\']+)["\']', re.IGNORECASE)
    quad_texture_quotes_pattern = re.compile(r'(quadTextureSprite\s*=\s*)["\']([^"\']+)["\']', re.IGNORECASE)
    sprite_type_quotes_pattern = re.compile(r'(spriteType\s*=\s*)["\']([^"\']+)["\']', re.IGNORECASE)
    font_quotes_pattern = re.compile(r'(font\s*=\s*)["\']([^"\']+)["\']', re.IGNORECASE)

    format_left_pattern = re.compile(r'format\s*=\s*["\']?left["\']?', re.IGNORECASE)
    zero_vector_pattern = re.compile(r'(position|bordersize)\s*=\s*\{\s*x\s*=\s*0\s+y\s*=\s*0\s*\}', re.IGNORECASE)
    empty_attr_pattern = re.compile(r'\w+\s*=\s*(\{\s*\}|""|\'\')\s*$', re.IGNORECASE)

    # Case-insensitive attribute replacements
    replacements = [
        (re.compile(r'^Orientation', re.IGNORECASE), 'orientation'),
        (re.compile(r'^buttonText', re.IGNORECASE), 'text'),
        (re.compile(r'^buttonFont', re.IGNORECASE), 'font')
    ]

    # Whitespace normalization (only for non-quoted text)
    normalize_equals = re.compile(r'\s*=\s*')
    normalize_braces = re.compile(r'\{\s*([^}]*)\s*\}')

    # Regex to capture quoted strings
    quoted_string = re.compile(r'(["\'])(?:\\.|(?!\1).)*\1')

    def normalize_outside_quotes(s: str) -> str:
        """Normalize = and {} outside quoted strings."""
        parts = []
        last_end = 0
        for m in quoted_string.finditer(s):
            segment = s[last_end:m.start()]
            segment = normalize_equals.sub(' = ', segment)
            segment = normalize_braces.sub(
                lambda m2: '{ ' + re.sub(r'\s+', ' ', m2.group(1).strip()) + ' }',
                segment
            )
            parts.append(segment)
            parts.append(m.group(0))
            last_end = m.end()
        segment = s[last_end:]
        segment = normalize_equals.sub(' = ', segment)
        segment = normalize_braces.sub(
            lambda m2: '{ ' + re.sub(r'\s+', ' ', m2.group(1).strip()) + ' }',
            segment
        )
        parts.append(segment)
        return ''.join(parts)

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Handle background blocks specially
        if re.match(r'background\s*=\s*\{', stripped, re.IGNORECASE):
            indent = re.match(r'^(\s*)', line).group(1)
            block_content = []
            raw_content = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("}"):
                inner_line = lines[i].strip()
                raw_content.append(inner_line)
                if re.match(r'(quadTextureSprite|spriteType)\s*=', inner_line, re.IGNORECASE):
                    block_content.append(normalize_outside_quotes(inner_line))
                i += 1
            # collapse only if block contains ONLY spriteType/quadTextureSprite
            if block_content and len(block_content) == len(raw_content):
                cleaned.append(f"{indent}background = {{ {' '.join(block_content)} }}")
            else:
                cleaned.append(f"{indent}background = {{")
                for inner in raw_content:
                    cleaned.append(f"{indent}\t{normalize_outside_quotes(inner)}")
                cleaned.append(f"{indent}}}")
            i += 1
            continue

        # Skip lines entirely if they match these "removal" patterns
        if orientation_remove_pattern.search(stripped) \
           or format_left_pattern.search(stripped) \
           or zero_vector_pattern.search(stripped) \
           or empty_attr_pattern.search(stripped):
            i += 1
            continue

        # Remove quotes for specific attributes
        line = orientation_quotes_pattern.sub(r'\1\2', line)
        line = origo_quotes_pattern.sub(r'\1\2', line)
        line = quad_texture_quotes_pattern.sub(r'\1\2', line)
        line = sprite_type_quotes_pattern.sub(r'\1\2', line)
        line = font_quotes_pattern.sub(r'\1\2', line)

        # Apply attribute replacements
        for pattern, replacement in replacements:
            line = pattern.sub(replacement, line, count=1)

        # Apply normalization outside of quotes (affects comments too)
        line = normalize_outside_quotes(line)

        cleaned.append(line)
        i += 1

    return "\n".join(cleaned) + "\n"


def process_file(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = clean_attributes(content)

        if new_content != content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Cleaned attributes in {path}")
        else:
            print(f"No changes in {path}")
    except Exception as e:
        print(f"Error processing {path}: {e}")

def main():
    root = tk.Tk()
    root.withdraw()

    folder = filedialog.askdirectory(title="Select folder to clean attributes")
    if not folder:
        print("No folder selected. Exiting...")
        sys.exit(0)

    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            process_file(os.path.join(dirpath, filename))

    print("Attribute cleaning complete.")

if __name__ == "__main__":
    main()
