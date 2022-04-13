import os
import sys
from csv import reader
from csv import writer

def readfile(path, searchterm):
    os.chdir(path)
    namelist = []
    os.chdir(sys.path[0]+"/Stats")
    with open(searchterm+'.csv', 'r') as csvfile:
        read = reader(csvfile, delimiter=',')
        for row in read:
            namelist.append(row)
        return namelist

def addshipfleetarmor(path, shipname):
    os.chdir(path)
    os.chdir(sys.path[0]+"/Stats")
    ar = "Hull: "
    name = shipname
    with open(name+'.csv', 'r') as csfile:
        read = reader(csfile, delimiter=',')
        for row in read:
            for a in row:
                if str(ar) in a:
                    armor = a.replace("Hull: ", "")
                    return armor
