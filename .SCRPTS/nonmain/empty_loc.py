import re

input_file = r"c:\Users\jmgp0\Documents\Paradox Interactive\Hearts of Iron IV\mod\Beyond Earth\localisation\loading_tips_l_english.yml"
output_file = r"c:\Users\jmgp0\Documents\Paradox Interactive\Hearts of Iron IV\mod\Beyond Earth\localisation\loading_tips_l_english_empty.yml"

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

# Replace all content between double quotes with empty string
new_content = re.sub(r'"[^"]*"', '""', content)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(new_content)