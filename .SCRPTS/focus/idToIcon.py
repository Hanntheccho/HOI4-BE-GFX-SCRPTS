import os
import sys
import tkinter  # pip install tkinter
from tkinter import filedialog

#DRAG THIS FILE INTO THE FOCUS FOLDER OTHERWISE IT WONT WORK

root = tkinter.Tk()
root.withdraw()

fFile = filedialog.askopenfilename(parent=root, title='Focus File')

focusFile = open(fFile, 'r', encoding='utf-8-sig')
outputFile = open("temp_file.txt", 'w', encoding='utf-8-sig')

idToAdd = ""
for line in focusFile:
    if "id = " in line and "_id" not in line:  # Does the line match the form "id = "
        outputFile.write(line)
        idToAdd = line[line.index("=")+2:] # Get everything after the "= " aka the ID of the focus
        outputFile.write("\t\ticon = GFX_goal_" + idToAdd +"\n") # Write the icon line with proper id
    else:
        outputFile.write(line)

outputFile.write("}")
outputFile.close()
focusFile.close()
os.remove(fFile)
os.rename("temp_file.txt", fFile)
print("done!")