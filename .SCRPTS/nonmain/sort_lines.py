file_path = "Untitled-1.txt"  # Change this if your file has a different name

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

lines.sort()

with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(lines)
