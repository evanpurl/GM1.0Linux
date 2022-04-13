import os
import sys
from csv import reader

def hullhealth(path, username, shipname, guildid):
    os.chdir(path)
    os.chdir(f"{path}/Stats/{guildid}")
    ship = shipname.replace("\n", '')
    with open(ship+".csv", 'r') as csvfile:
        read = reader(csvfile, delimiter=',')
        for row in read:
            for a in row:
                if "Hull Health: " in a:
                    hull = a.replace("Hull Health: ", "")
                    h = str(hull).replace(",", "")
    return h
def hullshipname(path, username, guildid):
    os.chdir(path)
    fleetlist = []
    f = open(f"{os.getcwd()}/Players/{guildid}/{username}.txt", "r")
    for a in f.readlines():
        fleetlist.append(a)
    return fleetlist
def shieldhealth(path, username, shipname, guildid):
    os.chdir(path)
    os.chdir(f"{path}/Stats/{guildid}")
    ship = shipname.replace("\n", '')
    with open(ship+".csv", 'r') as csvfile:
        read = reader(csvfile, delimiter=',')
        for row in read:
            for a in row:
                if "Shield Health: " in a:
                    shield = a.replace("Shield Health: ", "")
                    s = str(shield).replace(",", "")
    return s

def shieldregen(path, username, shipname, guildid):
    os.chdir(path)
    os.chdir(f"{path}/Stats/{guildid}")
    ship = shipname.replace("\n", '')
    with open(ship+".csv", 'r') as csvfile:
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
    with open(ship+".csv", 'r') as csvfile:
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
    with open(ship+".csv", 'r') as csvfile:
        read = reader(csvfile, delimiter=',')
        for row in read:
            for a in row:
                if "Hull Damage: " in a:
                    shiphulldamage = a.replace("Hull Damage: ", "")
                    hd = str(shiphulldamage).replace(",", "")
    return hd

def damresist(path, username, shipname, guildid):
    os.chdir(path)
    os.chdir(f"{path}/Stats/{guildid}")
    ship = shipname.replace("\n", '')
    with open(ship+".csv", 'r') as csvfile:
        read = reader(csvfile, delimiter=',')
        for row in read:
            for a in row:
                if "Damage Resistance: " in a:
                    resist = a.replace("Damage Resistance: ", "")
                    if str(resist) == "0":
                        resist == "1"
                    else:
                        return resist

def verify(path, shipname, guildid):
    os.chdir(path)
    os.chdir(f"{path}/Stats/{guildid}")
    ship = shipname.replace("\n", '')
    try:
        with open(ship+".csv", 'r') as csvfile:
            read = reader(csvfile, delimiter=',')
            for row in read:
                for a in row:
                    if "Hull Health: " in a:
                        hull = a.replace("Hull Health: ", "")
                        h = str(hull).replace(",", "")
        return h
    except:
        return None
