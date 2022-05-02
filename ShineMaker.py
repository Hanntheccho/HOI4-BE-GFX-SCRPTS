import tkinter as tk
import os
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilenames(title="Focus Tree Files")

focusFile = open(str(file_path).replace('(\'', '').replace('\',)', ''), 'r')
lines = focusFile.readlines()
iconArr = [""]
countryTag = ""
keepLooking = True

for line in lines:
    if "icon" in line:
        line.rstrip()
        splitLine = line.split(' ')
        iconArr.append(splitLine[2])
    if "tag" in line and keepLooking:
        line.rsplit()
        tempTag = line.split(' ')[2]
        countryTag = tempTag.rsplit()[0]
        keepLooking = False

print("Icon array completed")
iconArr.pop(0)
cleanedUpIcons = []
for icon in iconArr:
    if icon not in cleanedUpIcons:
        cleanedUpIcons.append(icon.rsplit()[0])

focusFile.close()
print("Icon cleanup completed, duplicates removed")

outputPath = filedialog.askdirectory(title="Ouput Folder")
os.chdir(outputPath)

goalFile = open('goals_{tag}.gfx'.format(tag=countryTag), 'w')
print(countryTag)
shineFile = open('goals_shine_{tag}.gfx'.format(tag=countryTag), 'w')

goalFile.write("spriteTypes = {	\n")
goalFile.write("\t##{tag}##\n".format(tag=countryTag))
print("Now writing goals_{tag}.gfx".format(tag=countryTag))
for i in range(len(cleanedUpIcons)):
    goalFile.write("\tSpriteType = {\n")
    goalFile.write("\t\tname = \"{icon}\"\n".format(icon = cleanedUpIcons[i]))
    goalFile.write("\t\ttexturefile = \"gfx/interface/goals/{icon}.dds\"\n".format(icon = cleanedUpIcons[i].replace('GFX_', '')))
    goalFile.write("\t}\n")
    goalFile.write("\n")
    
print("Done with goals_{tag}.gfx".format(tag=countryTag))
goalFile.close()
print("Now writing goals_shine_{tag}.gfx".format(tag=countryTag))
shineFile.write("spriteTypes = {	\n")
shineFile.write("\t##{tag}##\n".format(tag=countryTag))
for i in range(len(cleanedUpIcons)):
    shineFile.write("\tSpriteType = {\n")
    shineFile.write("\t\tname = \"{icon}_shine\"\n".format(icon = cleanedUpIcons[i]))
    shineFile.write("\t\ttexturefile = \"gfx/interface/goals/{icon}.dds\"\n".format(icon = cleanedUpIcons[i].replace('GFX_', '')))
    shineFile.write("\t\teffectFile = \"gfx/FX/buttonstate.lua\"\n")
    shineFile.write("\t\tanimation = {\n")
    shineFile.write("\t\t\tanimationmaskfile = \"gfx/interface/goals/{icon}.dds\"\n".format(icon = cleanedUpIcons[i].replace('GFX_', '')))
    shineFile.write("\t\t\tanimationtexturefile = \"gfx/interface/goals/shine_overlay.dds\"\n")
    shineFile.write("\t\t\tanimationrotation = -90.0		# -90 clockwise 90 counterclockwise(by default)\n")
    shineFile.write("\t\t\tanimationlooping = no			# yes or no ;)\n")
    shineFile.write("\t\t\tanimationtime = 0.75				# in seconds\n")
    shineFile.write("\t\t\tanimationdelay = 0			# in seconds\n")
    shineFile.write("\t\t\tanimationblendmode = \"add\"       #add, multiply, overlay\n")
    shineFile.write("\t\t\tanimationtype = \"scrolling\"      #scrolling, rotating, pulsing\n")
    shineFile.write("\t\t\tanimationrotationoffset = { x = 0.0 y = 0.0 }\n")
    shineFile.write("\t\t\tanimationtexturescale = { x = 1.0 y = 1.0 } \n")
    shineFile.write("\t\t}\n")
    shineFile.write("\n")
    shineFile.write("\t\tanimation = {\n")
    shineFile.write("\t\t\tanimationmaskfile = \"gfx/interface/goals/{icon}.dds\"\n".format(icon = cleanedUpIcons[i].replace('GFX_', '')))
    shineFile.write("\t\t\tanimationtexturefile = \"gfx/interface/goals/shine_overlay.dds\"\n")
    shineFile.write("\t\t\tanimationrotation = 90.0		# -90 clockwise 90 counterclockwise(by default)\n")
    shineFile.write("\t\t\tanimationlooping = no			# yes or no ;)\n")
    shineFile.write("\t\t\tanimationtime = 0.75				# in seconds\n")
    shineFile.write("\t\t\tanimationdelay = 0			# in seconds\n")
    shineFile.write("\t\t\tanimationblendmode = \"add\"       #add, multiply, overlay\n")
    shineFile.write("\t\t\tanimationtype = \"scrolling\"      #scrolling, rotating, pulsing\n")
    shineFile.write("\t\t\tanimationrotationoffset = { x = 0.0 y = 0.0 }\n")
    shineFile.write("\t\t\tanimationtexturescale = { x = 1.0 y = 1.0 } \n")
    shineFile.write("\t\t}\n")
    shineFile.write("\t\tlegacy_lazy_load = no\n")
    shineFile.write("\t}\n")

shineFile.write("}")  
print("Done with goals_shine_{tag}.gfx".format(tag=countryTag))
shineFile.close()
print("Job's done, now closing")
print("You may safely close this window! Should you wish to run the program again, please re-run the executable!")

