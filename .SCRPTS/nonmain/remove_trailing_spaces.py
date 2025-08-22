input_path = r'c:/Users/jmgp0/Documents/Paradox Interactive/Hearts of Iron IV/mod/Beyond Earth/localisation/replace/_names_l_english.yml'
output_path = input_path  # Overwrite the original file

with open(input_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open(output_path, 'w', encoding='utf-8') as f:
    for line in lines:
        f.write(line.rstrip() + '\n')
