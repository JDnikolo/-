import xml.etree.ElementTree as ET
import os

dir="C:\\Users\\Giannis Nikolopoulos\\Documents\\GitHub\\Ergasia\\NCT0000xxxx"
#print(os.listdir(dir))

distree=ET.Element("conditions")
ourtree=ET.ElementTree(distree)
for file in (os.listdir(dir)):
    tree=ET.parse(dir+"\\"+file)
    root=tree.getroot
    cond=tree.findall("condition")
    vention=tree.findall("./intervention/intervention_name")
    for conds in cond:
        condText=conds.text
        #print(condText)
        for a in ('@','(',')'):
            while a in condText:
                #print("Removing: "+a)
                condText=conds.text.replace(a,'')
        #print(str(condText))
        target=distree.find(condText)
        if target==None:
            print("Condition "+ condText+" from file "+file + " not found in tree. Appending.")
            orary=ET.SubElement(distree,'condition')
            orary.text=condText
            for vent in vention:
               temp=ET.SubElement(orary,'intervention')
               temp.text=vent.text
               temp.set('multiplicity','1')
        else:
            print("Condition "+ condText +" from file "+file + " found in tree. Appending Interventions.")
            for vent in vention:
                tarvent=target.find(vent.text)
                if tarvent!=None:
                    temp=ET.SubElement(target,'intervention',{'text':vent.text})
                    temp.set('multiplicity','1')
                else:
                     tarvent.set('multiplicity',str(int(tarvent.get('multiplicity'))+1))
ourtree.write('output.xml')