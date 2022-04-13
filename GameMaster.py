import discord
from dialoguecompiler import compiler as dialogue
from battlecode import battle as battle
import datetime, time
import os
import sys
import asyncio
import shutil

intents = discord.Intents.all()

bot = discord.Bot(intents=intents)

dirr = sys.path[0]


def tokengrabber():
    os.chdir(dirr + "/config")
    with open("token.txt", 'r') as token:
        return token.readline()


# This section of code is used to compile almost all dialogue used by the bot.
print("Compiling dialogue")
movetext = dialogue("movetext")
print("Dialogue Compiled!")


# =============================================================================


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('Powered by NLS: https://www.nitelifesoftware.com'))
    channel = bot.get_channel(905430483305897985)
    await channel.send("Restarted!")
    print('Connected!')
    print(discord.__version__)
    global start_time
    start_time = time.time()
    await bot.wait_until_ready()
    global guildnumber
    await check_guilds()


@bot.event
async def on_guild_join(guild):
    channel = bot.get_channel(905430483305897985)
    await channel.send(f"Bot joined server {str(guild.name)} with id {str(guild.id)}")
    if not os.path.exists(f"{dirr}/Stats/{str(guild.id)}"):
        os.mkdir(f"{dirr}/Stats/{str(guild.id)}")
    if not os.path.exists(f"{dirr}/Players/{str(guild.id)}"):
        os.mkdir(f"{dirr}/Players/{str(guild.id)}")


@bot.event
async def on_message(message):
    def is_auth(m):
        return m.author == message.author

    user1id = str(message.author.id)
    guildid = str(message.guild.id)
    chid = message.channel.id
    gid = message.guild.id
    gname = message.guild.name
    searchlowercase = message.content
    if message.author == bot.user:
        return
    username = message.author

    if message.content.startswith("!units"):
        os.chdir(dirr)
        un = []
        if os.path.exists(f"{os.getcwd()}/Stats/{guildid}"):
            filelist = os.listdir(f"{os.getcwd()}/Stats/{guildid}")
            if len(filelist) != 0:
                for a in filelist:
                    un.append(a.replace(".csv", ""))
                await message.channel.send(f"**{gname}'s Units:**")
                await message.channel.send('\n'.join(un))
            else:
                await message.channel.send(
                    "No units are currently on the server, create some using the !createunit command!")
    elif message.content.startswith("!start"):
        await message.channel.send(
            "To get started with GameMaster, please turn your attention towards our install guide on our website. There you can see all of my commands and how to use them! https://www.nitelifesoftware.com/gamemaster/install/")

    elif message.content.startswith("!deleteunit"):  # Unit deletion starts here.
        if message.author.guild_permissions.administrator:
            os.chdir(f"{dirr}/Stats/{guildid}")
            un = []
            if os.path.exists(f"{dirr}/Stats/{guildid}"):
                filelist = os.listdir(f"{dirr}/Stats/{guildid}")
                if len(filelist) != 0:
                    for a in filelist:
                        un.append(a.replace(".csv", ""))
                    await message.channel.send(f"**{gname}'s Units:**")
                    await message.channel.send('\n'.join(un))
                    await message.channel.send("Which unit do you want to delete?")
                    unitname = await bot.wait_for('message', check=is_auth, timeout=300)
                    if unitname.content in un:
                        os.remove(f"{unitname.content}.csv")
                        await message.channel.send(f"{unitname.content} has been removed!")
                    else:
                        await message.channel.send(f"{unitname.content} does not exist, run the command again.")
        else:
            await message.channel.send(f"You do not have permission to remove units from the server!")


    elif message.content.startswith("!createunit"):  # Unit creation starts here.
        if message.author.guild_permissions.administrator:
            if os.path.exists(f"{dirr}/Stats/{guildid}"):
                filelist = os.listdir(f"{dirr}/Stats/{guildid}")
                if len(filelist) == 50:
                    await message.channel.send(
                        "Max amount of units have been created, try deleting some before creating more.")
                else:
                    os.chdir(dirr)

                    unitstart = discord.Embed(title="Welcome", description=f'Version 0.3',
                                              color=discord.Color.from_rgb(255, 255, 255))

                    unitstart.add_field(name="Step 1:",
                                        value="Please create a name for your unit! **Warning**, the next message you type must be the unit's name.",
                                        inline=True)

                    await message.channel.send(embed=unitstart)

                    unitname = await bot.wait_for('message', check=is_auth, timeout=300)

                    unitsh = discord.Embed(title="Shields", description=f'Version 0.3',
                                           color=discord.Color.from_rgb(255, 255, 255))

                    unitsh.add_field(name="Step 1:", value=f"Chosen name: {unitname.content}.", inline=True)
                    unitsh.add_field(name="Step 2:",
                                     value=f"Please choose the desired shield strength your unit should have, if none, then type 0.",
                                     inline=True)

                    await message.channel.send(embed=unitsh)

                    unitshields = await bot.wait_for('message', check=is_auth, timeout=300)

                    unith = discord.Embed(title="Health", description=f'Version 0.3',
                                          color=discord.Color.from_rgb(255, 255, 255))

                    unith.add_field(name="Step 1:", value=f"Chosen name: {unitname.content}.", inline=True)
                    unith.add_field(name="Step 2:", value=f"Chosen shields: {unitshields.content}.", inline=True)
                    unith.add_field(name="Step 3:",
                                    value=f"Please choose the desired health your unit should have. **Warning**, typing 0 will cause the unit to instantly die.",
                                    inline=True)

                    await message.channel.send(embed=unith)

                    unithealth = await bot.wait_for('message', check=is_auth, timeout=300)

                    unitshd = discord.Embed(title="Shield Damage", description=f'Version 0.3',
                                            color=discord.Color.from_rgb(255, 255, 255))

                    unitshd.add_field(name="Step 1:", value=f"Chosen name: {unitname.content}.", inline=True)
                    unitshd.add_field(name="Step 2:", value=f"Chosen shields: {unitshields.content}.", inline=True)
                    unitshd.add_field(name="Step 3:", value=f"Chosen health: {unithealth.content}.", inline=True)
                    unitshd.add_field(name="Step 4:",
                                      value=f"Please choose the desired shield damage this unit should do. If your units do not have shields, then type 0.",
                                      inline=True)

                    await message.channel.send(embed=unitshd)

                    unitshieldd = await bot.wait_for('message', check=is_auth, timeout=300)

                    unitre = discord.Embed(title="Shield Regen", description=f'Version 0.3',
                                           color=discord.Color.from_rgb(255, 255, 255))

                    unitre.add_field(name="Step 1:", value=f"Chosen name: {unitname.content}.", inline=True)
                    unitre.add_field(name="Step 2:", value=f"Chosen shields: {unitshields.content}.", inline=True)
                    unitre.add_field(name="Step 3:", value=f"Chosen health: {unithealth.content}.", inline=True)
                    unitre.add_field(name="Step 4:", value=f"Chosen shield damage: {unitshieldd.content}.", inline=True)
                    unitre.add_field(name="Step 5:",
                                     value=f"Please choose the desired shield regeneration this unit should do. If your units do not have shields, then type 0.",
                                     inline=True)

                    await message.channel.send(embed=unitre)

                    unitregen = await bot.wait_for('message', check=is_auth, timeout=300)

                    unithd = discord.Embed(title="Damage", description=f'Version 0.3',
                                           color=discord.Color.from_rgb(255, 255, 255))

                    unithd.add_field(name="Step 1:", value=f"Chosen name: {unitname.content}.", inline=True)
                    unithd.add_field(name="Step 2:", value=f"Chosen shields: {unitshields.content}.", inline=True)
                    unithd.add_field(name="Step 3:", value=f"Chosen health: {unithealth.content}.", inline=True)
                    unithd.add_field(name="Step 4:", value=f"Chosen shield damage: {unitshieldd.content}.", inline=True)
                    unithd.add_field(name="Step 5:", value=f"Chosen shield regen: {unitregen.content}", inline=True)
                    unithd.add_field(name="Step 6:", value=f"Please choose the desired damage this unit should do.",
                                     inline=True)

                    await message.channel.send(embed=unithd)

                    unithdamage = await bot.wait_for('message', check=is_auth, timeout=300)

                    summary = discord.Embed(title="Summary", description=f'Version 0.3',
                                            color=discord.Color.from_rgb(255, 255, 255))

                    summary.add_field(name="Step 1:", value=f"Chosen name: {unitname.content}.", inline=True)
                    summary.add_field(name="Step 2:", value=f"Chosen shields: {unitshields.content}.", inline=True)
                    summary.add_field(name="Step 3:", value=f"Chosen health: {unithealth.content}.", inline=True)
                    summary.add_field(name="Step 4:", value=f"Chosen shield damage: {unitshieldd.content}.",
                                      inline=True)
                    summary.add_field(name="Step 5:", value=f"Chosen shield regen: {unitregen.content}", inline=True)
                    summary.add_field(name="Step 6:", value=f"Chosen damage: {unithdamage.content}.", inline=True)

                    await message.channel.send(embed=summary)
                    os.chdir(f"{dirr}/Stats/{guildid}")
                    csv_file = open(f"{unitname.content}.csv", "w+")
                    csv_file.write(
                        f"{unitname.content}\nHull Health: {unithealth.content}\nShield Health: {unitshields.content}\nShield Regen: {unitregen.content}\nShield Damage: {unitshieldd.content}\nHull Damage: {unithdamage.content}")  # Unit is written to file here.
                    csv_file.close()
                    await message.channel.send("Unit created!")
        else:
            await message.channel.send(
                "You don't have permission to add units to the server")  # Unit Creation finishes here.




    elif message.content.startswith("!groupadd"):
        glist = []
        auth = message.author.id
        os.chdir(dirr)
        un = []
        unn = []
        num = []
        units = []
        if os.path.exists(f"{os.getcwd()}/Stats/{guildid}"):
            filelist = os.listdir(f"{os.getcwd()}/Stats/{guildid}")
            if len(filelist) != 0:
                for a, b in enumerate(filelist):
                    un.append(f"{b.replace('.csv', '')}")
                    unn.append(f"{a + 1}. {b.replace('.csv', '')}")
                    num.append(f"{a + 1}")
                await message.channel.send(f"**{gname}'s Units:**")
                await message.channel.send('\n'.join(unn))
                await message.channel.send(
                    f"Please select your units! '1, 2, 3, 4, etc.' Warning, your next message must be your units, or you will have to re run the command.")
                unitmsg = await bot.wait_for('message', check=is_auth, timeout=300)
                choseunit = unitmsg.content.split(", ")
                for a in choseunit:
                    if not a.isdigit():
                        await message.channel.send(f"{a} is not a valid entry.")
                    else:
                        if a in num:
                            ind = num.index(a)
                            units.append(un[ind])
                        else:
                            await message.channel.send(f"{a} is not a valid number.")
                await message.channel.send("You Chose: \n" + '\n'.join(units))
                f = open(f"{os.getcwd()}/Players/{guildid}/{message.author.id}.txt", "w+")
                for a in units:
                    f.write(a + "\n")
                f.close()
            else:
                await message.channel.send("You have not uploaded any units to the server!")
    # Group adding process is complete

    elif searchlowercase.startswith("!battle"):  ############## battle function
        # if not str(897256834677739560) in searchlowercase:
        await battle(message.author.display_name, searchlowercase, guildid, bot, user1id, chid, username, movetext)
        # else:
        # await pvebattle(message.author.display_name, guildid, bot, user1id, chid, username, movetext) # PvE battle function (Not working currently)
        await message.channel.send("Command completed")

    elif searchlowercase.startswith("!support"):
        await message.channel.send("Join our support server if you need help! https://discord.gg/RgTH7xEW3z")


    elif searchlowercase.startswith("!uptime"):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=0xc8dc6c)
        embed.add_field(name="GameMaster Uptime", value=text)
        try:
            await message.channel.send(embed=embed)
        except discord.HTTPException:
            await message.channel.send("GameMaster Uptime: " + text)


async def check_guilds():  # System that checks once daily if any folders the bot has in the database is not a server the bot is in. If not, deletes the folders.
    listofids = []
    for guild in bot.guilds:
        listofids.append(str(guild.id))
    channel = bot.get_channel(905430483305897985)
    await channel.send(f"Bot is active on {len(listofids)} servers!")
    while True:
        os.chdir(dirr)
        if os.path.exists(f"{os.getcwd()}/Players"):
            folders = [x[1] for x in os.walk(f"{os.getcwd()}/Players")]
            guildlist = folders[0]
            for b in guildlist:
                if b not in listofids:
                    os.chdir(dirr)
                    shutil.rmtree(f"{os.getcwd()}/Players/{str(b)}")
                    shutil.rmtree(f"{os.getcwd()}/Stats/{str(b)}")
                    await channel.send(f"Bot is no longer in server with id {str(b)}")

        await asyncio.sleep(86400)  # 24 hour sleep function, bot runs loop again after 24 hours.


bot.run(tokengrabber())
