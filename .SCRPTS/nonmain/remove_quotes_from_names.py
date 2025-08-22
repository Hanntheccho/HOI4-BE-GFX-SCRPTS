import os
import re

# Path to the strategicregions directory (edit this if running from a different location)
folder = os.path.dirname(__file__)

# Regex pattern to match name="STRATEGICREGION_NAME_anything"
pattern = re.compile(r'(name=)\"(STRATEGICREGION_NAME_[^\"]+)\"')

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Replace the pattern
    new_content = pattern.sub(r'\1\2', content)
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {filepath}")
    else:
        print(f"No change: {filepath}")

def main():
    for filename in os.listdir(folder):
        if filename.endswith('.txt'):
            filepath = os.path.join(folder, filename)
            process_file(filepath)

if __name__ == "__main__":
    main()