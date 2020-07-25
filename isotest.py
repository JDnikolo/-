import xml.etree.ElementTree as ET
import os,json

def findInterventions(target,dir='.\\NCT0000xxxx'):
    dir="C:\\Users\\Giannis Nikolopoulos\\Documents\\GitHub\\Ergasia\\NCT0000xxxx"
    #print(os.listdir(dir))
    results=dict()
    try:
        f=open('.\\cache\\'+target+'.json','r')
        results=dict(json.loads(f.read()))
        sortedResults=sorted(results.items(),key=lambda x:x[1])
        sortedResults.reverse()
    except OSError:
        for file in (os.listdir(dir)):
            tree=ET.parse(dir+"\\"+file)
            root=tree.getroot
            conds=tree.findall('condition')
            if conds!=[]:
                for cond in conds:
                    if cond.text==target:
                        #print("Found a hit!")
                        ventions=tree.findall("./intervention")                
                        for v in ventions:
                            inter=v.find('intervention_type')
                            if inter.text=='Drug':
                                name=v.find('intervention_name')
                                if name.text not in results:
                                    results[name.text]=1
                                else:
                                    results[name.text]+=1    
        sortedResults=sorted(results.items(),key=lambda x:x[1])
        sortedResults.reverse()
        output=json.dumps(sortedResults)
        f=open('.\\cache\\'+target+".json",'w')
        f.write(output)
        f.close()
    #print(results)
    #print('\n')
    #print(sortedResults)
    return zip(range(10),sortedResults)


if __name__=="__main__":
    a=findInterventions("Panic Attack")
    for that in a:
        print(str(that[0]+1)+' '+str(that[1]))