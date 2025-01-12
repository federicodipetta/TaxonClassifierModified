"""
this file is used to compare two json files and return the difference between them, this file return also a json 
and u can use the diagram generator to see the difference between the two json files
"""
import json as json 
import os
def loadJson(file):
    with open(file) as f:
        return json.load(f)

def getElementFromKey(key,data):
    for element in data:
        if element["key"] == key:
            return element
    return None

def compareScores(score1,score2):
    return {
        "rand_score"         : score1["rand_score"]         - score2["rand_score"],
        "homogeneity_score"  : score1["homogeneity_score"]  - score2["homogeneity_score"],
        "completeness_score" : score1["completeness_score"] - score2["completeness_score"],
    }

def getWinningScore(out):
    result = [0,0,0] # win,lose,draw
    for info in out["data"] : 
        for key in info["value"] : 
            for score in info["value"][key] : 
                if info["value"][key][score] > 0.00: 
                    result[0] += 1
                elif info["value"][key][score] < -0.00 : 
                    result[1] += 1
                else : 
                    result[2] += 1
    return result

def compareElements(element1,element2):
    print(element1["key"] , " - ",element2["key"])
    result = {}
    result["single"]   = compareScores(element1["single"]  ,element2["single"]  )
    result["average"]  = compareScores(element1["average"] ,element2["average"] )
    result["complete"] = compareScores(element1["complete"],element2["complete"])
    return result

settings = json.load(open('settings.json'))["jsonComparator"]

data1 = loadJson(settings['json1'])["data"]
data2 = loadJson(settings['json2'])["data"]
dataOut = []
for element in data1 : 
    elemnt2 = getElementFromKey(element["key"],data2)
    if elemnt2 is not None:
        dataOut.append({
            "key" : element["key"],
            "value" : compareElements(element,elemnt2)
        })
    else:
        raise Exception("key not found in the second json file : " + element["key"])

jsonOut = {
    "firsrJson" : os.path.basename(settings['json1']),
    "secondJson" : os.path.basename(settings['json2']),
    "data" : dataOut
}

if ('output' in settings):
    os.makedirs(os.path.dirname(settings['output']), exist_ok=True) 
    with open(settings['output'], 'w') as outfile:
        json.dump(jsonOut, outfile, indent=4)
else : 
    with open('compareOut.json', 'w') as outfile:
        json.dump(jsonOut, outfile)
print("winning score : ",getWinningScore(jsonOut))