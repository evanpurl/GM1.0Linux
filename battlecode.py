import discord
from dice import diceroll as die
from dotenv import load_dotenv
import sys
import asyncio
import random
from getfleethealth import hullhealth as hull
from getfleethealth import shieldhealth as shield
from getfleethealth import hullshipname as hullname
from getfleethealth import shieldregen as regen
from getfleethealth import verify as verify
from getfleethealth import shielddamage as shielddamage
from getfleethealth import hulldamage as hulldamage
from getfleethealth import damresist as damresist
from pve import botgroupcreation as bgc

dirr = sys.path[0]

def nonzero(lis):
    ran = random.choice(lis)
    while ran == 0:
        ran = random.choice(lis)
    if ran != 0:
        return ran

game_over = False
async def battle(authorusername, message, guildid, client, u1id, channelid, username, movetext):
    channel = client.get_channel(channelid)
    playerone = authorusername
    playertwo = message.replace("!battle ", '')
    userid = playertwo.replace(">", '').replace("<@!", "").replace("<@", "").replace("!", "")
    usertwo = await client.fetch_user(int(userid))
    poneshdamage = []
    ponehulldamage = []
    ptwoshdamage = []
    ptwohulldamage = []
    hullvals = []
    shieldvals = []
    hullvalstwo = []
    shieldvalstwo = []
    playeronedefeat = []
    playertwodefeat = []
    initshieldspone = []
    initshieldsptwo = []
    try:
        playertwoname = hullname(dirr, userid, guildid)
        name = hullname(dirr, u1id, guildid)
        initplayeroneembed=discord.Embed(title=playerone+"'s Units:", description=f'Units: {len(name)}', color=discord.Color.red())
    except Exception as e:
    	print(e)
    	await channel.send("Have both players made a group? Cancelling battle.")
    	return True
    for a in range(0, len(name)): # Player one
        try:
            p1name = name[a].replace("\n", "")
            poneshdamage.append(float(shielddamage(dirr, p1name, guildid))) # Player one collective fleet shield, and below it hull damage
            ponehulldamage.append(float(hulldamage(dirr, p1name, guildid)))
            hullvals.append(float(hull(dirr, username, p1name, guildid)))
            shieldvals.append(float(shield(dirr, username, p1name, guildid)))
            initshieldspone = shieldvals
            initplayeroneembed.add_field(name=name[a].replace("\n", ''), value="- " + "🛡: "+str(shieldvals[a])+ "\n" +" "+"❤️:"+str(hullvals[a]), inline=True)
        except Exception as e:
            print(e)
            await channel.send(f"{playerone}, something went wrong with your group. Try remaking your fleet and check your spelling. Cancelling battle.")
            return True
        p1sd = poneshdamage
        p1hd = ponehulldamage
    
    await channel.send(embed=initplayeroneembed)
    await channel.send("------------------------")
    initplayertwoembed=discord.Embed(title=usertwo.display_name+"'s Units:", description=f'Units: {len(playertwoname)}', color=discord.Color.blue())
    for d in range(0, len(playertwoname)): # Player two
        try:
            p2name = playertwoname[d].replace("\n", "")
            ptwoshdamage.append(float(shielddamage(dirr, p2name, guildid))) # Player two collective fleet shield, and below it hull damage
            ptwohulldamage.append(float(hulldamage(dirr, p2name, guildid)))
            shieldvalstwo.append(float(shield(dirr, userid, p2name, guildid)))
            hullvalstwo.append(float(hull(dirr, userid, p2name, guildid)))
            initshieldsptwo = shieldvalstwo
            initplayertwoembed.add_field(name=playertwoname[d].replace("\n", ''), value="- " + "🛡: "+str(shieldvalstwo[d])+ "\n" +"- " +"❤️: "+str(hullvalstwo[d]), inline=True)
        except:
            await channel.send(f"{usertwo.display_name}, something went wrong with your group. Try remaking your group and checking the exact spelling of the units you're using. Cancelling battle")
            return True
        p2sd = ptwoshdamage
        p2hd = ptwohulldamage
    await channel.send(embed=initplayertwoembed)
    roundnum = 0
    while not game_over: # Battle code starts here now that data is compiled
        roundnum += 1
        roundembed=discord.Embed(title="Round: "+str(roundnum), description='', color=0x00ff00)
        await channel.send(embed=roundembed)
        msg = await channel.send(usertwo.display_name+movetext)
        await msg.add_reaction("🔫")
        def check(reaction, user):
            return user == usertwo and str(reaction.emoji) == "🔫"
        try:
            turn = await client.wait_for('reaction_add', check=check, timeout=1800)
        except asyncio.TimeoutError:
            await channel.send("Battle has not continued in 30 minutes, battle concluding")
            await msg.clear_reaction("🔫")
            await msg.edit(content=msg.content + " (Reaction removed, battled ended due to inactivity).")
            return True
        shipembed=discord.Embed(title=playerone+"'s Ships:", description=f'Units alive last turn: {len(name) - len(playeronedefeat)}', color=discord.Color.red())
        for c in range(0, len(name)): # Player one gets attacked
            p1name = name[c].replace("\n", "")
            ptworoll = die(0, 100)
            if ptworoll == 0:
                shieldvals[c] -= 0
                hullvals[c] -= 0
                shieldvals[c] += float(regen(dirr, username, p1name, guildid))
                shipembed.add_field(name=name[c], value="- " + "🛡: " + str(round(shieldvals[c], 0))+ "\n" +"- " +"❤️: " + str(round(hullvals[c], 0)), inline=True)
            else:
                shieldvals[c] += float(regen(dirr, username, p1name, guildid))
                shieldvals[c] -= (ptworoll + nonzero(p2sd)) / (len(name)/2) #/ float(damresist(dirr, username, p1name, guildid))
                if float(shieldvals[c]) <= 0:
                    shieldvals[c] = 0
                    hullvals[c] -= (ptworoll + nonzero(p2hd)) / (len(name)/2) #/ float(damresist(dirr, username, p1name, guildid))
                    if int(hullvals[c]) < 0:
                        hullvals[c] = 0
                        shipembed.add_field(name=p1name.capitalize(), value="- " + "🛡: "+str(round(shieldvals[c], 0))+ "\n" +"- " +"❤️: "+str(round(hullvals[c], 0))+ "\n" +"- " +"Status: Defeated", inline=True)
                        if f"s {c} " not in playeronedefeat:
                            playeronedefeat.append(f"s {c}")
                            p1sd[c] = 0
                            p1hd[c] = 0
                        if len(playeronedefeat) == len(name):
                            await msg.clear_reaction("🔫")
                            await msg.edit(content=msg.content + " (Reaction removed, turn passed).")
                            endembed=discord.Embed(title="Defeat", description='', color=discord.Color.red())
                            endembed.add_field(name=playerone + "! " + "Your fleet has been defeated", value='You have lost the battle.', inline=True)
                            await channel.send(embed=endembed)
                            return True
                    else:
                        shipembed.add_field(name=p1name.capitalize(), value="- " + "🛡: "+str(round(shieldvals[c], 0))+ "\n" +"- " +"❤️: "+str(round(hullvals[c], 0)), inline=True)
                else:
                    if shieldvals[c] > initshieldspone[c]:
                        shieldvals[c] = initshieldspone[c]
                    shipembed.add_field(name=name[c].replace("\n", '').capitalize(), value="- " + "🛡: "+str(round(shieldvals[c], 0))+ "\n" +"- " +"❤️: "+str(round(hullvals[c], 0)), inline=True)
        await channel.send(embed=shipembed) # Sends message into discord with damage done to player one's ship.
        await msg.clear_reaction("🔫")
        await msg.edit(content=msg.content + " (Reaction removed, turn passed).")
            

            
        msg = await channel.send(playerone+movetext) # Start of player one's turn
        await msg.add_reaction("🔫")
        def check(reaction, user):
            return user == username and str(reaction.emoji) == "🔫"
        try:
            turntwo = await client.wait_for('reaction_add', check=check, timeout=1800)
        except asyncio.TimeoutError:
            await channel.send("Battle has not continued in 30 minutes, battle concluding.")
            await msg.clear_reaction("🔫")
            await msg.edit(content=msg.content + " (Reaction removed, battled ended due to inactivity).")
            return True
        shipembed=discord.Embed(title=usertwo.display_name+"'s Ships:", description=f'Units alive last turn: {len(playertwoname)- len(playertwodefeat)}', color=discord.Color.blue())
        for c in range(0, len(playertwoname)): # Player two gets attacked
            poneroll = die(0, 100)
            p2name = playertwoname[c].replace("\n", "")
            if poneroll == 0:
                shieldvalstwo[c] -= 0
                hullvalstwo[c] -= 0
                shieldvalstwo[c] += float(regen(dirr, usertwo.id, p2name, guildid))
                shipembed.add_field(name=p2name.capitalize(), value="- " + "🛡: "+str(round(shieldvalstwo[c], 0))+ "\n" +"- " +"❤️: "+str(round(hullvalstwo[c], 0)), inline=True)
            else:
                shieldvalstwo[c] -= (poneroll + nonzero(p1sd)) / (len(playertwoname)/2) #/ float(damresist(dirr, usertwo.id, p2name, guildid))
                shieldvalstwo[c] += float(regen(dirr, usertwo.id, p2name, guildid))
                if float(shieldvalstwo[c]) <= 0:
                    shieldvalstwo[c] = 0
                    hullvalstwo[c] -= (poneroll + nonzero(p1hd)) / (len(playertwoname)/2)  #/ float(damresist(dirr, usertwo.id, p2name, guildid))
                    if float(hullvalstwo[c]) < 0:
                        hullvalstwo[c] = 0
                        shipembed.add_field(name=playertwoname[c].replace("\n", '').capitalize(), value="- " + "🛡: "+str(round(shieldvalstwo[c], 0))+ "\n" +"- " +"❤️: "+str(round(hullvalstwo[c], 0))+ "\n" +"- " +"Status: Defeated", inline=True)
                        if f"s {c}" not in playertwodefeat:
                            playertwodefeat.append(f"s {c}")
                            p2sd[c] = 0
                            p2hd[c] = 0
                        if len(playertwodefeat) == len(playertwoname):
                            await msg.clear_reaction("🔫")
                            await msg.edit(content=msg.content + " (Reaction removed, turn passed).")
                            endembed=discord.Embed(title="Defeat", description='', color=discord.Color.blue())
                            endembed.add_field(name=usertwo.display_name + "! " + "Your fleet has been defeated", value='You have lost the battle.', inline=True)
                            await channel.send(embed=endembed)
                            return True
                    else:
                        shipembed.add_field(name=playertwoname[c].replace("\n", '').capitalize(), value="- " + "🛡: "+str(round(shieldvalstwo[c], 0))+ "\n" +"- " +"❤️: "+str(round(hullvalstwo[c], 0)), inline=True)
                else:
                    if shieldvalstwo[c] > initshieldsptwo[c]:
                        shieldvalstwo[c] = initshieldsptwo[c]
                    shipembed.add_field(name=playertwoname[c].replace("\n", '').capitalize(), value="- " + "🛡: "+str(round(shieldvalstwo[c], 0))+ "\n" +"- " +"❤️: "+str(round(hullvalstwo[c], 0)), inline=True)
        await channel.send(embed=shipembed) # Sends message into discord with damage done to player two's ship.
        await msg.clear_reaction("🔫")
        await msg.edit(content=msg.content + " (Reaction removed, turn passed).")
