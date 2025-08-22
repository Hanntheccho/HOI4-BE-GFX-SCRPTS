import os

def remove_comments_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in lines:
            # Remove everything after '#' (including the '#'), but keep the line before it
            if '#' in line:
                line = line.split('#', 1)[0].rstrip() + '\n' if line.split('#', 1)[0].strip() else ''
            f.write(line)

folder = r'c:\Users\jmgp0\Documents\Paradox Interactive\Hearts of Iron IV\mod\Beyond Earth\history\states'

for filename in os.listdir(folder):
    if filename.endswith('.txt'):
        remove_comments_from_file(os.path.join(folder, filename))
