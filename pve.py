import os
import sys
from csv import reader
import random
from dice import diceroll as die

#-----------------------------------------------------------------------------

dirr = sys.path[0]

def hullhealth(path, shipname, guildid):
    os.chdir(f"{path}/Stats/{guildid}")
    ship = shipname.replace("\n", '')
    with open(ship+".csv", 'r', encoding='utf-8') as csvfile:
        read = reader(csvfile, delimiter=',')
        for row in read:
            for a in row:
                if "Hull Health: " in a:
                    hull = a.replace("Hull Health: ", "")
                    h = str(hull).replace(",", "")
                    return h

def shieldhealth(path, shipname, guildid):
    os.chdir(path)
    os.chdir(f"{path}/Stats/{guildid}")
    ship = shipname.replace("\n", '')
    with open(ship+".csv", 'r', encoding='utf-8') as csvfile:
        read = reader(csvfile, delimiter=',')
        for row in read:
            for a in row:
                if "Shield Health: " in a:
                    shield = a.replace("Shield Health: ", "")
                    s = str(shield).replace(",", "")
                    return s

def shieldregen(path, shipname, guildid):
    os.chdir(path)
    os.chdir(f"{path}/Stats/{guildid}")
    ship = shipname.replace("\n", '')
    with open(ship+".csv", 'r', encoding='utf-8') as csvfile:
        read = reader(csvfile, delimiter=',')
        for row in read:
            for a in row:
                if "Shield Regen: " in a:
                    regen = a.replace("Shield Regen: ", "")
                    r = str(regen).replace(",", "")
        return r

def shielddamage(path, shipname, guildid):
    shipshielddamage = 0
    os.chdir(path)
    os.chdir(f"{path}/Stats/{guildid}")
    ship = shipname.replace("\n", '')
    with open(ship+".csv", 'r', encoding='utf-8') as csvfile:
        read = reader(csvfile, delimiter=',')
        for row in read:
            for a in row:
                if "Shield Damage: " in a:
                    shipshielddamage = a.replace("Shield Damage: ", "")
                    sd = str(shipshielddamage).replace(",", "")
        return sd

def hulldamage(path, shipname, guildid):
    shiphulldamage = 0
    os.chdir(path)
    os.chdir(f"{path}/Stats/{guildid}")
    ship = shipname.replace("\n", '')
    with open(ship+".csv", 'r', encoding='utf-8') as csvfile:
        read = reader(csvfile, delimiter=',')
        for row in read:
            for a in row:
                if "Hull Damage: " in a:
                    shiphulldamage = a.replace("Hull Damage: ", "")
                    hd = str(shiphulldamage).replace(",", "")
        return hd

def damresist(path, shipname, guildid):
    os.chdir(path)
    os.chdir(f"{path}/Stats/{guildid}")
    ship = shipname.replace("\n", '')
    with open(ship+".csv", 'r', encoding='utf-8') as csvfile:
        read = reader(csvfile, delimiter=',')
        for row in read:
            for a in row:
                if "Damage Resistance: " in a:
                    resist = a.replace("Damage Resistance: ", "")
                    if str(resist) == "0":
                        resist == "1"
                    else:
                        return resist

def compileunits(path, guildid):
    unitname = []
    shields = []
    hull = []
    hdamage = []
    sdamage = []
    sregen = []
    dres = []
    filelist = os.listdir(f"{path}/Stats/{str(guildid)}")
    for a in filelist:
        name = str(a).replace(".csv", "")
        unitname.append(name)
        sregen.append(float(shieldregen(path, name, guildid)))
        shields.append(float(shieldhealth(path, name, guildid)))
        hull.append(float(hullhealth(path, name, guildid)))
        hdamage.append(float(hulldamage(path, name, guildid)))
        sdamage.append(float(shielddamage(path, name, guildid)))
        dres.append(float(damresist(path, name, guildid)))
    return unitname, sregen, shields, hull, hdamage, sdamage, dres # Returns 7 items.
    
def botgroupcreation(path, guildid, num): # num is player fleet size
    numu = die(num / 2, num)
    units = []
    shield = []
    hull = []
    regen = []
    hd = []
    sd = []
    res = []
    os.chdir(path)
    unitname, sregen, shields, h, hdamage, sdamage, dres = compileunits(path, guildid) # Calls on the 7 returned items.
    
    unitlist = random.sample(list(enumerate(unitname)), numu)
    for idx, val in unitlist:
        units.append(val)
        shield.append(shields[idx])
        hull.append(h[idx])
        regen.append(sregen[idx])
        hd.append(hdamage[idx])
        sd.append(sdamage[idx])
        res.append(dres[idx])
    return units, shield, hull, regen, hd, sd, res
    

