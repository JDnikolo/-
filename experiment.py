import xml.etree.ElementTree as ET
import os

dir="C:\\Users\\Giannis Nikolopoulos\\Documents\\GitHub\\Ergasia\\NCT0000xxxx"

for file in (os.listdir(dir)):
    i=0
    tree=ET.parse(dir+"\\"+file)
    root=tree.getroot
    inter=tree.findall('intervention')
    for v in inter:
        if len(v.findall('*'))>2:
            print(file)
    if ++i>11:
        break
