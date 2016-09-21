import csv
from pprint import pprint
from mol02 import searchlistdict

fn = "C:\Projects\ButterflyNet\Specimen\\test.csv"
fn1 = "C:\Projects\ButterflyNet\Specimen\\test1.csv"

def makestring(filename,binom,genus,species):
    input_file = csv.DictReader(open(filename))
    Strpass=''
    if binom == '':
        for row in input_file:
            if (row[genus]+' '+row[species]) != ' ':
                Strpass = (Strpass + ', '+row[genus]+' '+row[species])
    else:
        for row in input_file:
            if (row[binom]) != '':
                Strpass = (Strpass + ', '+row[binom])
    return (Strpass)

def makelistdict(filename, binom, genus, species):
    input_file = csv.DictReader(open(filename))
    listdict = []
    if binom == '':
        for row in input_file:
            binomial = row[genus].strip() + ' ' + row[species].strip()
            row['binomial'] = binomial
            listdict.append(row)
    else:
        for row in input_file:
             binomial = row[binom].strip()
             row['binomial'] = binomial
             listdict.append(row)
    return (listdict)

def getheareds(filename):
    input_file = csv.DictReader(open(filename))
    headers = input_file.fieldnames
    return (headers)

#t = makestring(fn,'','Genus','Species')
#print(t)

#t = makestring(fn1,'','Genus','Species')
#t = makelistdict("C:\Projects\ButterflyNet\Specimen\\test1.csv",'','Genus','Species')
#t1 = searchlistdict(t,18)
#pprint(t1)