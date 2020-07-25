import xml.etree.ElementTree as ET
import os,json,time

def secureString(target):
                target=target.replace('/',' ')
                target=target.replace('"','')
                target=target.replace('>','over')
                target=target.replace('<','under')
                target=target.replace(':','')
                target=target.replace('*','')
                target=target.replace('\\',' ')
                target=target.replace('?','')
                target=target.replace('|',' ')
                return target



cache='.\\cache'
filedir='.\\Files'
start=time.time()
for folder in os.listdir(filedir):
        for files in os.listdir(filedir+'\\'+folder):
            tree=ET.parse(filedir+'\\'+folder+'\\'+files)
            conditions=tree.findall('condition')
            interventions=tree.findall('intervention')
            for vent in interventions:
                if vent.find('intervention_type').text!='Drug':
                    interventions.remove(vent)
                #else:
                    #print(vent.text)
            for cond in conditions:
                cond.text=secureString(cond.text)
                #print(cond.text)
                try:
                    f=open(cache+'\\'+cond.text+'.json','r')
                    results=dict(json.loads(f.read()))
                    for vent in interventions:
                        name=vent.find("intervention_name").text
                        print('Writing '+name+'in file '+cond.text)
                        if name in results:
                         results[name]+=1
                        else:
                            results[name]=1
                    sortedResults=sorted(results.items(),key=lambda x:x[1])
                    sortedResults.reverse()
                    f.close()
                    f=open(cache+'\\'+cond.text+'.json','w')
                    f.write(json.dumps(sortedResults,sort_keys=True, indent=1))
                    f.close()
                except OSError or JSONDecodeError:
                    f=open(cache+'\\'+cond.text+'.json','w')
                    results=dict()
                    for vent in interventions:

                        name=vent.find("intervention_name").text
                        print('Writing '+name+'in file '+cond.text)
                        if name in results:
                            results[name]+=1
                        else:
                            results[name]=1
                    sortedResults=sorted(results.items(),key=lambda x:x[1])
                    sortedResults.reverse()
                    f.write(json.dumps(sortedResults,sort_keys=True, indent=1))
                    f.close()
end=time.time()
print(end-start / 60.0)




