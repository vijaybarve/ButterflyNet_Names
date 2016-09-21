import urllib
from pprint import pprint
import re
import requests
import json

dan=['Danaus affinis', 'Danaus chrysippus', 'Danaus cleophile', 'Danaus dorippus',
 'Danaus eresimus', 'Danaus erippus', 'Danaus genutia', 'Danaus gilippus',
 'Danaus ismare', 'Danaus melanippus', 'Danaus petilia', 'Danaus plexippus',
 'Papilio chrysippus', 'Anosia plexippus', 'Salatura genutia', 'Euploea chionippe ']
dan1= ['Anosia plexippus', 'Danaus chrysippus','Papilio chrysippus']

def getname(tcid):
    params = {'tcids': tcid,
              'getsynonyms': 'False'}
    qstr = urllib.urlencode(params)
    reply = requests.get('http://api.mol.org/1.0/taxonomy/tcinfo', qstr)
    json1 = reply.json()
    #pprint (json1)
    retname=''
    for k, i in json1.items():
        retname = i['name']

    return retname

def gettcid(name,txid):
    params = {'searchstrs': name,
              'getsynonyms': 'False',
              'taxonomyid': txid
              }
    qstr = urllib.urlencode(params)
    reply = requests.get('http://api.mol.org/1.0/taxonomy/tcsearch', qstr)
    json1 = reply.json()
    #pprint(json1)
    #print (len(json1))

    retid=''
    for k, i in json1.items():
        #print (len(i))
        if len(i)>0:
            retid = i[0]['tcid']


    return retid

def searchlst(names,txid):
    #print("--- tcsearch ---")
    namestr = ','.join(names)
    params = {'searchstrs': namestr,
              'taxonomyid':txid
              }
    qstr = urllib.urlencode(params)
    reply = requests.get('http://api.mol.org/1.0/taxonomy/tcsearch', qstr)
    json1 = reply.json()

    res=[]
    for i in json1:
        temp = json1[i]
        if len(temp)>0:
            temp=temp[0]
            if temp['validname'] != 'valid':
                vname=getname(temp['tcid'])
                res.append({'valid name': vname, 'Flag': temp['validname'],'user-supplied name':temp['name']})
                #print('invalid')
            else:
                res.append({'user-supplied name': temp['name'], 'Flag': temp['validname'],'valid name':temp['name']})
                #print(temp['name'],temp['validname'])
        else:
            res.append({'user-supplied name': i, 'Flag': u'Not found','valid name':''})

    return res

def strSentence(sentence):
    return sentence[0].upper() + sentence[1:].lower()

def searchlistdict(listdict,txid):
    res=[]
    for rec in listdict:
        namestr = rec['binomial']
        namestr = namestr.translate(None, '?!@#$')
        params = {'searchstrs': namestr,
                  'taxonomyid': txid
                  }
        qstr = urllib.urlencode(params)
        reply = requests.get('http://api.mol.org/1.0/taxonomy/tcsearch', qstr)
        json1 = reply.json()
        #temp1 = json.loads(json1)
        #print(temp1)
        #pprint(json1)

    # for i in json1:
        temp = json1
        namestr = strSentence(namestr)
        print(namestr)
        #pprint(temp)
        #print(type(temp))

        if temp[namestr]:
        #if namestr in temp1:
            temp = temp[namestr][0]
            #pprint(temp)
            #print(type(temp))
            if temp['validname'] != 'valid':
                vname = getname(temp['tcid'])
                rec['valid name'] = vname
                rec['Flag'] = 'Synonym'
                #print("Synonym")
                #pprint(rec)
                #rec.append({'valid name': vname, 'Flag': temp['validname'],'user-supplied name':temp['name']})
                #print('invalid')
            else:
                rec['valid name'] = temp['name']
                rec['Flag'] = 'Valid Name'
                #rec.append({'user-supplied name': temp['name'], 'Flag': temp['validname'],'valid name':temp['name']})
                #print(temp['name'],temp['validname'])
        else:
            rec['valid name'] = ''
            rec['Flag'] = 'Not Found'
            #rec.append({'user-supplied name': i, 'Flag': u'Not found','valid name':''})
        res.append(rec)
    return res


def searchstring(string,txid):
    lst=re.split(r'\s*,\s*',string)
    return searchlst(lst ,txid)

#n=getname('7c86b303-f8f9-4e5d-a317-8915632dedd3')
#pprint(n)

mystr = 'Anosia plexippus,Danaus chrysippus, Papilio chrysippus'
mystr = 'Heraclides thoas, 	Sericinus montela, 	Heraclides anchisiades'
mystr = 'Amphidecta calliomma, Cissia pseudoconfusa, Pseudodebis puritana, Euptychoides eugenia, Riodina lysippus, Parthenos sylvia, Palla ussheri, Dianesia carteri, Sarota gamelia, Harjesia blanda, Rareuptychia clio, Protographium marcellus, Yphthimoides pacta, Tellervo zoilus, Prothoe franck, Mesene croceella, Chloreuptychia arnaca, Hermeuptychia sosybus, Taygetina oreba, Magneuptychia keltoumae, Maniola jurtina, Ithomia patilla, Morpho sp., Liptena ferrymani, Chloreuptychia clorimena, Magneuptychia alcinoe'
mystr = 'Afrixalus fulvovittatus, Afrixalus lacteus'
mystr = 'Afrixalus fulvovittatus1'
#t = gettcid(mystr,14)
#pprint(t)

mystr = 'Afrixalus fulvovittatus'
#t = gettcid(mystr,14)
#pprint(t)

#t=searchstring(mystr,14)
#t=searchlst(dan,18)
#pprint(t)

#t= getname('8c9b1570-e419-44bc-8370-6ff66a623774')
#print t
