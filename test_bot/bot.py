import os
import random
import json
import praw
import discord

from discord import client
from discord import embeds

from prawcore import auth

import pytz
import time
import datetime
import sched


from dotenv import load_dotenv

from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')# gets the token of the bot from the .env file so they confidentional token won't be shared in the terminal
GUILD = os.getenv('DISCORD_GUILD')# gets the name of the guild from .env file about which you want the info
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')


reddit = praw.Reddit(
        client_id = REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
)


intents = discord.Intents.default()# sets intents as an instant if intents
intents.members = True# sets intents for members true so we use members from the server


bot = commands.Bot(command_prefix="icy ", intents=intents)


#all the global variables
if True:
        suggestion_num = 0
        suggestions = {}

        autoroles = []

        send_welcome_dm = False
        custom_welcome_dm = None

        welcome_channel = None
        send_welcome_message = True
        custom_welcome_message = None
        send_welcome_gif = True
        custom_welcome_gif = None
        welcome_member_count_show = True
        send_welcome_emote = True
        send_welcome_thumbnail = True
        custom_welcome_thumbnail = None

        goodbye_channel = None
        send_goodbye_message = True
        custom_goodbye_message = None
        send_goodbye_gif = True
        custom_goodbye_gif = None
        goodbye_member_count_show = True
        send_goodbye_emote = True
        send_goodbye_thumbnail = True
        custom_goodbye_thumbnail = None

        first_welcome_set = True
        first_goodbye_set = True


        server_name = None

        muterole = None

        # post starting limits (later will be reset using a clock)
        thoughtlimit = 2
        memelimit = 2
        catlimit = 2

        testvar = None
        testvar2 = None

        disposable = None

        muted_user_roles = {}

        dataindexdict = None
        default_join = None




def extract_user_and_role(user_and_role_id):
        user_and_role_id = user_and_role_id[:-1]
        user_and_role_id = user_and_role_id[3:]

        return user_and_role_id

def extract_channel(channelid):
        channelid = channelid[:-1]
        channelid = channelid[2:]

        return channelid

def extract_string(args):

        var = ""
        for i in args:
                var = var+ " " + i
                var = var[0:]

        return var

def getjson(serverid, variable, variable_string):

        global dataindexdict

        server_in_file = False

        with open("C:\\pythonWay\\PROJECTS\\DISCORD_BOT\\botdatatest.json", "r") as jsonfile:

                loaddata = json.load(jsonfile)

                print(f"SERVER ID> {serverid}")


                for i in loaddata["guilddata"]:
                        #loaddata["guilddata"]

                        print("ye")
                        try:
                                i[serverid]

                                print(i)
                                print("FUCK YEA")


                                server_in_file = True
                                dataindex = loaddata["guilddata"].index(i)
                                dataindexdict = dataindex

                                try:

                                        print("JUST GETTING THE VARRIABLE 0")
                                        variable = i.get(serverid).get(variable_string)

                                        print("JUST GETTING THE VARRIABLE")
                                        break
                                except:

                                        print("THE VARIABLE ISN'T PRESENT 0")
                                        savejson(serverid, variable, variable_string)

                                        print("THE VARIABLE WASN'T PRESENT")
                                        break

                        except:
                                pass


        if server_in_file == False:
                
                print("THE SERVER ISN'T PRESENT IN THE LIST 0")

                with open("C:\\pythonWay\\PROJECTS\\DISCORD_BOT\\botdatatest.json", "w") as dumpfile:
                        loaddata["guilddata"].append({serverid: {}})
                        json.dump(loaddata, dumpfile, indent=8)

                dataindex = -1
                dataindexdict = -1

                print("NEW SERVER ADDED")
                print(loaddata)

        
        return variable

def savejson(serverid, newvalue, variable_string):

        global dataindexdict

        dataindex = dataindexdict

        with open("C:\\pythonWay\\PROJECTS\\DISCORD_BOT\\botdatatest.json", "r") as jsonfile:

                loaddata = json.load(jsonfile)

        #UPDATING THE VARIALE
        loaddata["guilddata"][dataindex][serverid][variable_string] = newvalue#update({variable_string: newvalue})


        #DUMPS
        with open("C:\\pythonWay\\PROJECTS\\DISCORD_BOT\\botdatatest.json", "w") as dumpfile:
                json.dump(loaddata, dumpfile, indent=8)

        print("IT SAVED BABY")

def default_json(guild):
        
        global welcome_channel

        global custom_welcome_message
        global send_welcome_gif
        global custom_welcome_gif
        global send_welcome_message
        global welcome_member_count_show
        global send_welcome_emote
        global custom_welcome_thumbnail
        global send_welcome_thumbnail
        global send_welcome_dm
        global custom_welcome_dm


        global goodbye_channel

        global custom_goodbye_message
        global send_goodbye_gif
        global custom_goodbye_gif
        global send_goodbye_message
        global goodbye_member_count_show
        global send_goodbye_emote
        global custom_goodbye_thumbnail
        global send_goodbye_thumbnail

        global server_name
        global autoroles

        global muterole

        global suggestion_num
        global suggestions

        global thoughtlimit
        global memelimit
        global catlimit

        global disposable

        global dataindexdict

        serverid = str(guild.id)

        #disposable = getjson(serverid, disposable, "disposable")

        savejson(serverid, guild.name, "server_name")

        savejson(serverid, welcome_channel, "welcome_channel")
        savejson(serverid, custom_welcome_message, "custom_welcome_message")
        savejson(serverid, send_welcome_gif, "send_welcome_gif")
        savejson(serverid, custom_welcome_gif, "custom_welcome_gif")
        savejson(serverid, send_welcome_message, "send_welcome_message")
        savejson(serverid, welcome_member_count_show, "welcome_member_count_show")
        savejson(serverid, send_welcome_emote, "send_welcome_emote")
        savejson(serverid, custom_welcome_thumbnail, "custom_welcome_thumbnail")
        savejson(serverid, send_welcome_thumbnail, "send_welcome_thumbnail")
        savejson(serverid, send_welcome_dm, "send_welcome_dm")
        savejson(serverid, custom_welcome_dm, "custom_welcome_dm")
        savejson(serverid, autoroles, "autoroles")

        savejson(serverid, goodbye_channel, "goodbye_channel")
        savejson(serverid, custom_goodbye_message, "custom_goodbye_message")
        savejson(serverid, send_goodbye_gif, "send_goodbye_gif")
        savejson(serverid, custom_goodbye_gif, "custom_goodbye_gif")
        savejson(serverid, send_goodbye_message, "send_goodbye_message")
        savejson(serverid, goodbye_member_count_show, "goodbye_member_count_show")
        savejson(serverid, send_goodbye_emote, "send_goodbye_emote")
        savejson(serverid, custom_goodbye_thumbnail, "custom_goodbye_thumbnail")
        savejson(serverid, send_goodbye_thumbnail, "send_goodbye_thumbnail")

        savejson(serverid, muterole, "muterole")

        savejson(serverid, suggestion_num, "suggestion_num")
        savejson(serverid, suggestions, "suggestions")

        savejson(serverid, thoughtlimit, "thoughtlimit")
        savejson(serverid, memelimit, "memelimit")
        savejson(serverid, catlimit, "catlimit")

        savejson(serverid, muted_user_roles, "muted_user_roles")

        savejson(serverid, True, "default_join")
        
        
        
        dataindexdict = None

def reddit_hot_reset():

        global thoughtlimit
        global memelimit
        global catlimit

        thoughtlimit = 2
        memelimit = 2
        catlimit = 2


        now = datetime.datetime.now().astimezone(pytz.timezone("UTC"))
        nextday = datetime.datetime.now().astimezone(pytz.timezone("UTC")) + datetime.timedelta(days=1)
        utcmidnight = datetime.datetime(hour=5, minute=30, second=0, day=nextday.day, month=nextday.month, year=nextday.year).astimezone(pytz.timezone("UTC"))
        
        sleep_time = utcmidnight - now
        sleep_time = sleep_time.total_seconds()
        
        sched.threading.Timer(sleep_time, reddit_hot_reset).start()
        print("resetted reddit hot limits")


reddit_hot_reset()



#prints when the bot is connected to discord and the guild members
@bot.event
async def on_ready():

        global default_join

        print(f'{bot.user.name} has connected to Discord!')# takes the name of the bot and then prints the given string

        guild = discord.utils.get(bot.guilds, name=GUILD)# gets the guild name using the .env file and the get function from discord.utils
        memberss = [member.name for member in guild.members]# creates a list of members
        print(f'server members are: {memberss}')# prints the members

        print(discord.utils.get(bot.guilds))

        now = datetime.datetime.now().astimezone(pytz.timezone("UTC"))
        print(f"connected at: {now} UTC")

        for guild in bot.guilds:
                
                guild_id = str(guild.id)

                if getjson(guild_id, default_join, "default_join") == None:
                        default_json(guild)








@bot.event
async def on_guild_join(guild):

        global dataindexdict

        serverid = str(guild.id)

        with open("C:\\pythonWay\\PROJECTS\\DISCORD_BOT\\botdata.json", "r") as jsonfile:
                loaddata = json.load(jsonfile)
                loaddata["guilddata"].append({serverid: {}})

                dataindexdict = -1
        
        default_json(guild)











#sends the welcome message in the server
@bot.event
async def on_member_join(member):

        global welcome_channel

        global custom_welcome_message
        global send_welcome_gif
        global custom_welcome_gif
        global send_welcome_message
        global welcome_member_count_show
        global send_welcome_emote
        global custom_welcome_thumbnail
        global send_welcome_thumbnail

        global send_welcome_dm
        global custom_welcome_dm

        global server_name
        global autoroles

        global dataindexdict

        serverid = str(member.guild.id)

        if True:                

                welcome_channel           = getjson(serverid, welcome_channel, "welcome_channel")
                custom_welcome_message    = getjson(serverid, custom_welcome_message, "custom_welcome_message")
                send_welcome_gif          = getjson(serverid, send_welcome_gif, "send_welcome_gif")
                custom_welcome_gif        = getjson(serverid, custom_welcome_gif, "custom_welcome_gif")
                send_welcome_message      = getjson(serverid, send_welcome_message, "send_welcome_message")
                welcome_member_count_show = getjson(serverid, welcome_member_count_show, "welcome_member_count_show")
                send_welcome_emote        = getjson(serverid, send_welcome_emote, "send_welcome_emote")
                custom_welcome_thumbnail  = getjson(serverid, custom_welcome_thumbnail, "custom_welcome_thumbnail")
                send_welcome_thumbnail    = getjson(serverid, send_welcome_thumbnail, "send_welcome_thumbnail")
                send_welcome_dm           = getjson(serverid, send_welcome_dm, "send_welcome_dm")
                custom_welcome_dm         = getjson(serverid, custom_welcome_dm, "custom_welcome_dm")
                server_name               = getjson(serverid, server_name, "server_name")
                autoroles                 = getjson(serverid, autoroles, "autoroles")

                dataindexdict = None

        # gets the server object using the server name got from the welcome_channel function
        server = discord.utils.get(bot.guilds, name=server_name)


        if welcome_channel:

                welcome_channel = discord.utils.get(member.guild.channels, id=int(welcome_channel))# converts the channel id into a channel object

                print(welcome_channel)

                member_number = len(server.members)# gets the number of members in the server

                if not send_welcome_message:

                        # if the welcome message is turned off by the admin
                        welcome_message_text = None
                else:

                        # the default welcome message to be used when custom message isn't given
                        welcome_message_text = f"WELCOMEEEE to {server.name}, glad to have you here and hope you enjoy your stay"

                        # when welcome message is set up
                        if custom_welcome_message:
                                # checks if there is a custom message given by the admin when a user enters
                                welcome_message_text = custom_welcome_message



                # all the default welcome gifs
                welcome_gifs = (
                        "https://media1.tenor.com/images/6830c5f9430da0b5bd9f3e55f66a4fca/tenor.gif?itemid=19063102",
                        "https://media1.tenor.com/images/08c2c8535404c39f2fb3cb5de85c97d7/tenor.gif?itemid=16281444",
                        "https://media1.tenor.com/images/c5fad21f9828d19044a58f8b84a6e14b/tenor.gif?itemid=6013419",
                        "https://media1.tenor.com/images/5210b05939cdafd508346f8e714c1595/tenor.gif?itemid=17715386",
                )



                title = f"WELCOME TO {server.name}"# the main title for welcome message
                name = f"Welcome {member.name}#{member.discriminator}"# welcomes the user with the full username
                members = f"**server now has {member_number} members!!!**"# variable for the new member count of the server(can be removed)



                embeded = discord.Embed(title=title, description=None, color=0x8871bf)# sets the title


                # customizing the member count and the emoji thingy and adding the welcome message in the embed
                if send_welcome_emote and welcome_member_count_show:

                        # when all the varriables are to be sent
                        value = welcome_message_text + "\n" + members + "\n" + "(>̃ ㅅ<̃)"

                        embeded.add_field(name=name, value=value, inline=False)# the main welocme message and shows the number of members and the emoji thingy
                elif send_welcome_emote and not welcome_member_count_show:

                        # when the emote and the message is to be sent without the member count
                        value = welcome_message_text + "\n" + "(>̃ ㅅ<̃)"

                        embeded.add_field(name=name, value=value, inline=False)# the main welocme message and shows only the the emoji thingy
                elif not send_welcome_emote and welcome_member_count_show:

                        # when only the member count and the message is to be sent without the emote
                        value = welcome_message_text + "\n" + members

                        embeded.add_field(name=name, value=value, inline=False)# the main welocme message and shows the number of members and not the emoji thingy
                else:

                        # when both the emote and the member left count is removed
                        if not welcome_message_text:
                                name = "**" + name + "**"

                                embeded = discord.Embed(title=title, description=name, color=0x8871bf)# sets the title
                        else:
                                value = welcome_message_text
                        
                                embeded.add_field(name=name, value=value, inline=False)# the main welocme message

                if send_welcome_thumbnail:

                        if custom_welcome_thumbnail:
                                # if a custom thumbnail is given by the admin
                                thumbnail = custom_welcome_thumbnail
                        else:
                                # by default the welcome message thumbnail is the user avatar
                                thumbnail = member.avatar_url# gets the user avatar
                        
                        embeded.set_thumbnail(url=thumbnail)# sets the thumbnail(shows the user avatar or the custom thumbnail in the side)

                if send_welcome_gif:

                        if custom_welcome_gif:
                                #checks if there is a custom gif given by the admin for welcome message
                                welcome_gif = custom_welcome_gif
                        else:
                                # selects any random welcome gif when a custom gif isn't given by the admin
                                welcome_gif = random.choice(welcome_gifs)

                        embeded.set_image(url=welcome_gif)# sets the gif as the main image in embed


                await welcome_channel.send(embed=embeded)


        # checks if the autoroles are setted up
        if autoroles:
                for role in autoroles:

                        # adds the role/roles when a member joins
                        await member.add_roles(role)


        if send_welcome_dm:

                dm_text = f'Hiiiiiiiiiii {member.name}, welcomeeeeeeeee to {member.guild.name}, hope you enjoy your stay :)'

                if custom_welcome_dm:
                        dm_text = custom_welcome_dm
                
                await member.create_dm()# creates a dm channel with the new user
                await member.dm_channel.send(
                        # sends the dm and takes the members name from member taken as an argument
                        dm_text
                )





#sends goodbye message in the server
@bot.event
async def on_member_remove(member):

        global goodbye_channel

        global custom_goodbye_message
        global send_goodbye_gif
        global custom_goodbye_gif
        global send_goodbye_message
        global goodbye_member_count_show
        global send_goodbye_emote
        global custom_goodbye_thumbnail
        global send_goodbye_thumbnail

        global server_name

        global dataindexdict

        serverid = str(member.guild.id)

        if True:

                goodbye_channel           = getjson(serverid, goodbye_channel, "goodbye_channel")
                custom_goodbye_message    = getjson(serverid, custom_goodbye_message, "custom_goodbye_message")
                send_goodbye_gif          = getjson(serverid, send_goodbye_gif, "send_goodbye_gif")
                custom_goodbye_gif        = getjson(serverid, custom_goodbye_gif, "custom_goodbye_gif")
                send_goodbye_message      = getjson(serverid, send_goodbye_message, "send_goodbye_message")
                goodbye_member_count_show = getjson(serverid, goodbye_member_count_show, "goodbye_member_count_show")
                send_goodbye_emote        = getjson(serverid, send_goodbye_emote, "send_goodbye_emote")
                custom_goodbye_thumbnail  = getjson(serverid, custom_goodbye_thumbnail, "custom_goodbye_thumbnail")
                send_goodbye_thumbnail    = getjson(serverid, send_goodbye_thumbnail, "send_goodbye_thumbnail")
                server_name               = getjson(serverid, server_name, "server_name")

                dataindexdict = None

        # gets the server object using the server name recieved from the welcome/goodbye channel command
        server = discord.utils.get(bot.guilds, name=server_name)


        if goodbye_channel:

                goodbye_channel = discord.utils.get(server.channels, id=int(goodbye_channel))# converts the channel id into a channel object

                member_number = len(server.members)# gets the number of server members

                if not send_goodbye_message:

                        # if the goodbye message is turned off by the admin
                        goodbye_message_text = None
                else:

                        # the default goodbye message to be used when custom message isn't given
                        goodbye_message_text = f"Goodbye {member.name}, hope you enjoyed your stay"

                        # when goodbye message is set up
                        if custom_goodbye_message:
                                # checks if there is a custom message given by the admin when a user enters
                                goodbye_message_text = custom_goodbye_message



                # all default the goodbye gifs
                goodbye_gifs = (
                        "https://media1.tenor.com/images/6ff14029eb25bbbe796bcec5112eff67/tenor.gif?itemid=17172673",
                        "https://media1.tenor.com/images/86a81a4a4e63afc759800f452b396787/tenor.gif?itemid=15151699",
                        "https://media1.tenor.com/images/9555ccb50d3ca7fb8a705411da351272/tenor.gif?itemid=17194414",
                        "https://media1.tenor.com/images/699f87bf9ab92a23cbec699b7cc002dc/tenor.gif?itemid=15875440",
                )


                title = f"{member.name} left {server.name}..."# the main title of the goodbye message
                name = f"Goodbye {member.name}#{member.discriminator}"# says goodbye to the user
                members = f"now we have {member_number} members left"# variable to show the remaining member count(can be turned off)



                embeded = discord.Embed(title=title, description=None, color=0x8871bf)# sets the title
                

                # customizing the member count and the emoji thingy and adding the goodbye message in the embed
                if send_goodbye_emote and goodbye_member_count_show:

                        # when all the varriables are to be sent
                        value = goodbye_message_text + "\n" + members + "\n" + "( ╥︣ ﹏ ╥︣ )"

                        embeded.add_field(name=name, value=value, inline=False)# the main goodbye message and shows the number of members and the emoji thingy
                elif send_goodbye_emote and not goodbye_member_count_show:

                        # when the emote and the message is to be sent without the member count
                        value = goodbye_message_text + "\n" + "( ╥︣ ﹏ ╥︣ )"

                        embeded.add_field(name=name, value=value, inline=False)# the main goodbye message and shows only the the emoji thingy
                elif not send_goodbye_emote and goodbye_member_count_show:

                        # when only the member count and the message is to be sent without the emote
                        value = goodbye_message_text + "\n" + members

                        embeded.add_field(name=name, value=value, inline=False)# the main goodbye message and shows the number of members and not the emoji thingy
                else:

                        # when both the emote and the member left count is removed
                        if not goodbye_message_text:
                                name = "**" + name + "**"

                                embeded = discord.Embed(title=title, description=name, color=0x8871bf)# sets the title
                        else:
                                value = goodbye_message_text
                        
                                embeded.add_field(name=name, value=value, inline=False)# the main goodbye message

                if send_goodbye_thumbnail:

                        if custom_goodbye_thumbnail:
                                # if a custom thumbnail is given by the admin
                                thumbnail = custom_goodbye_thumbnail
                        else:
                                # by default the goodbye message thumbnail is the user avatar
                                thumbnail = member.avatar_url# gets the user avatar

                        embeded.set_thumbnail(url=thumbnail)# sets the thumbnail(shows the user avatar or the custom thumbnail in the side)

                if send_goodbye_gif:

                        if custom_goodbye_gif:
                                #checks if there is a custom gif given by the admin for goodbye message
                                goodbye_gif = custom_goodbye_gif
                        else:
                                # selects any random goodbye gif when a custom gif isn't given by the admin
                                goodbye_gif = random.choice(goodbye_gifs)

                        embeded.set_image(url=goodbye_gif)# sets the gif as the main image in embed


                await goodbye_channel.send(embed=embeded)







@bot.command(name="setwelcomechannel")
async def on_message(ctx, *args):

        global welcome_channel
        global server_name
        global default_join

        global dataindexdict


        serverid = str(ctx.author.guild.id)
        server_name = ctx.author.guild.name# gets the server name and sets it as the global varriable

        welcome_channel = getjson(serverid, welcome_channel, "welcome_channel")
        welcome_channel = extract_channel(args[0])# gets the channel id from the arguments

        server_name = getjson(serverid, server_name, "server_name")
        server_name = ctx.author.guild.name# gets the server name and sets it as the global varriable

        if "None" in args[0] or "none" in args[0]:

                welcome_channel = None
                print(f"command: \"setwelcomechannel\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                await ctx.send("Icy will not send any welcome messages")

        else:

                welcome_channel = extract_channel(args[0])# gets the channel id from the arguments


                try:
                        try_this = await commands.TextChannelConverter().convert(ctx, welcome_channel)# converts the channel id into a channel object


                        print(f"command: \"setwelcomechannel\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                        await ctx.send(f"<#{welcome_channel}> channel will recieve the welcome messages")# confirms the command in the chat

                except:
                        heat_up_message = "The given channel doesn't exists, please make sure to tag the channel correctely"

                        embeded = discord.Embed(title="Icy's heating up..", description=heat_up_message, color=0x5fb79d)
                        await ctx.send(embed=embeded)


        savejson(serverid, welcome_channel, "welcome_channel")
        savejson(serverid, server_name, "server_name")

        dataindexdict = None



@bot.command(name="setwelcomemessage")
async def on_message(ctx, *args):

        global custom_welcome_message
        global send_welcome_message

        global dataindexdict

        serverid = str(ctx.author.guild.id)


        custom_welcome_message = getjson(serverid, custom_welcome_message, "custom_welcome_message")
        send_welcome_message = getjson(serverid, send_welcome_message, "send_welcome_message")

        custom_welcome_message = extract_string(args)# gets the message given by user and sets it as the global varriable

        if "None" in args[0] or "none" in args[0]:

                custom_welcome_message = None

                send_welcome_message = False

                print(f"command: \"setwelcomemessage\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                await ctx.send(f"Icy won't send the welcome message when a user joins the server")

        else:
                
                send_welcome_message = True

                print(f"command: \"setwelcomemessage\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                await ctx.send(f"The following message is set as the welcome message: \"{custom_welcome_message}\"")# confirms the command in the chat

        savejson(serverid, custom_welcome_message, "custom_welcome_message")
        savejson(serverid, send_welcome_message, "send_welcome_message")

        dataindexdict = None



@bot.command(name="resetwelcomemessage")
async def on_message(ctx):

        global send_welcome_message

        global dataindexdict

        serverid = str(ctx.author.guild.id)
        send_welcome_message = getjson(serverid, send_welcome_message, "send_welcome_message")

        # a way to go back to the defualt welcome message
        send_welcome_message = True
        

        print(f"command: \"resetwelcomemessage\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

        await ctx.send(f"Icy will send the default message as the welcome message")# confirms the command in the chat

        savejson(serverid, send_welcome_message, "send_welcome_message")
        dataindexdict = None



@bot.command(name="setwelcomegif")
async def on_message(ctx, *args):

        global custom_welcome_gif
        global send_welcome_gif

        global dataindexdict

        serverid = str(ctx.author.guild.id)

        custom_welcome_gif = getjson(serverid, custom_welcome_gif, "custom_welcome_gif")
        send_welcome_gif = getjson(serverid, send_welcome_gif, "send_welcome_gif")

        print(f"command: \"setwelcomegif\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

        if "None" in args or "none" in args:

                send_welcome_gif = False

                await ctx.send("Icy won't add a gif in the welcome message")


        elif "True" in args or "True" in args:

                send_welcome_gif = True

                await ctx.send("Icy will add a gif in the welcome message")


        else:
                
                custom_welcome_gif = args
                send_welcome_gif = True

                try:
                        await ctx.send("The following gif will be used as welcoming gif:")
                        await ctx.send(url=custom_welcome_gif)

                except:
                        await ctx.send("Invalid link. Please make sure to give the link of the gif location")

        savejson(serverid, custom_welcome_gif, "custom_welcome_gif")
        savejson(serverid, send_welcome_gif, "send_welcome_gif")

        dataindexdict = None



@bot.command(name="showwelcomemembercount")
async def on_message(ctx, *args):

        global welcome_member_count_show

        global dataindexdict

        serverid = str(ctx.author.guild.id)

        welcome_member_count_show = getjson(serverid, welcome_member_count_show, "welcome_member_count_show")

        if "True" in args[0] or "true" in args[0]:
                welcome_member_count_show = True

                print(f"command: \"showwelcomemembercount\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal
                await ctx.send("Icy will add the number of members left to the message")
        
        elif "False" in args[0] or "false" in args[0]:
                welcome_member_count_show = False

                print(f"command: \"showwelcomemembercount\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal
                await ctx.send("Icy won't add the number of members left to the message")

        else:
                heat_up_message = "Please make sure that the input is either \"True\" or \"False\""
                embeded = discord.Embed(title="Icy's heating up..", description=heat_up_message, color=0x5fb79d)

                print(f"command: \"showwelcomemembercount\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                await ctx.send(embed=embeded)

        savejson(serverid, welcome_member_count_show, "welcome_member_count_show")

        dataindexdict = None



@bot.command(name="sendwelcomeemote")
async def on_message(ctx, *args):

        global send_welcome_emote

        global dataindexdict

        serverid = str(ctx.author.guild.id)

        send_welcome_emote = getjson(serverid, send_welcome_emote, "send_welcome_emote")

        if "True" in args[0] or "true" in args[0]:
                send_welcome_emote = True

                print(f"command: \"sendwelcomeemote\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal
                await ctx.send("Icy will add the emoticon in the welcome message")

        elif "False" in args[0] or "false" in args[0]:
                send_welcome_emote = False

                print(f"command: \"sendwelcomeemote\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal
                await ctx.send("Icy won't add the emoticon in the welcome message")

        else:
                heat_up_message = "Please make sure that the input is either \"True\" or \"False\""
                embeded = discord.Embed(title="Icy's heating up..", description=heat_up_message, color=0x5fb79d)

                print(f"command: \"sendwelcomeemote\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                await ctx.send(embed=embeded)

        savejson(serverid, send_welcome_emote, "send_welcome_emote")

        dataindexdict = None



@bot.command(name="setwelcomethumbnail")
async def on_message(ctx, *args):

        global custom_welcome_thumbnail

        global dataindexdict

        serverid = str(ctx.author.guild.id)

        custom_welcome_thumbnail = getjson(serverid, custom_welcome_thumbnail, "custom_welcome_thumbnail")

        if "None" in args[0] or "none" in args[0]:
                custom_welcome_thumbnail = None

                print(f"command: \"setwelcomethumbnail\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal
                await ctx.send("Icy will add the user profile picture as the thumbnail, to stop that use command: \"icy removewelcomethumbnail\"")

        else:

                custom_welcome_thumbnail = args[0]

                print(f"command: \"setwelcomethumbnail\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                
                try:
                        await ctx.send("The following image will be used as the welcome thumbnail:")
                        await ctx.send(url=custom_goodbye_thumbnail)

                except:
                        heat_up_message = "Invalid link. Please make sure that the image location is correct"
                        embeded = discord.Embed(title="Icy's heating up..", description=heat_up_message, color=0x5fb79d)

                        await ctx.send(embed=embeded)

        savejson(serverid, custom_welcome_thumbnail, "custom_welcome_thumbnail")

        dataindexdict = None



@bot.command(name="sendwelcomethumbnail")
async def on_message(ctx, *args):

        global send_welcome_thumbnail

        global dataindexdict

        serverid = str(ctx.author.guild.id)

        send_welcome_thumbnail = getjson(serverid, send_welcome_thumbnail, "send_welcome_thumbnail")

        if "True" in args[0] or "true" in args[0]:
                send_welcome_thumbnail = True

                print(f"command: \"sendwelcomethumbnail\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal
                await ctx.send("Icy will add the thumbnail in the welcome message")

        elif "False" in args[0] or "false" in args[0]:
                send_welcome_thumbnail = False

                print(f"command: \"sendwelcomethumbnail\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal
                await ctx.send("Icy won't add the thumbnail in the welcome message")

        else:
                heat_up_message = "Please make sure that the input is either \"True\" or \"False\""
                embeded = discord.Embed(title="Icy's heating up..", description=heat_up_message, color=0x5fb79d)

                print(f"command: \"sendwelcomethumbnail\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                await ctx.send(embed=embeded)

        savejson(serverid, send_welcome_thumbnail, "send_welcome_thumbnail")

        dataindexdict = None





@bot.command(name="setgoodbyechannel")
async def on_message(ctx, *args):

        global goodbye_channel
        global server_name

        global dataindexdict

        serverid = str(ctx.author.guild.id)
        server_name = ctx.author.guild.name# gets the server name and sets it as the global varriable


        goodbye_channel = getjson(serverid, goodbye_channel, "goodbye_channel")
        server_name = getjson(serverid, server_name, "server_name")

        if "None" in args[0] or "none" in args[0]:

                goodbye_channel = None
                print(f"command: \"setgoodbyechannel\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                await ctx.send("Icy will not send any goodbye messages")

        else:

                goodbye_channel = extract_channel(args[0])# gets the channel id from the arguments


                try:
                        test_goodbye_channel = await commands.TextChannelConverter().convert(ctx, goodbye_channel)# converts the channel id into a channel object


                        print(f"command: \"setwelcomechannel\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                        await ctx.send(f"<#{goodbye_channel}> channel will recieve the welcome messages")# confirms the command in the chat

                except:

                        heat_up_message = "The given channel doesn't exists, please make sure to tag the channel correctely"

                        embeded = discord.Embed(title="Icy's heating up..", description=heat_up_message, color=0x5fb79d)
                        await ctx.send(embed=embeded)

        savejson(serverid, goodbye_channel, "goodbye_channel")
        savejson(serverid, server_name, "server_name")

        dataindexdict = None




@bot.command(name="setgoodbyemessage")
async def on_message(ctx, *args):

        global custom_goodbye_message
        global send_goodbye_message

        global dataindexdict

        serverid = str(ctx.author.guild.id)

        custom_goodbye_message = getjson(serverid, custom_goodbye_message, "custom_goodbye_message")
        send_goodbye_message = getjson(serverid, send_goodbye_message, "send_goodbye_message")

        custom_goodbye_message = extract_string(args)# gets the message given by user and sets it as the global varriable

        if "None" in args[0] or "none" in args[0]:

                custom_goodbye_message = None
                send_goodbye_message = False
                print(f"command: \"setgoodbyemessage\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                await ctx.send(f"Icy won't send a goodbye message when a user leaves")

        else:

                send_goodbye_message = True
                print(f"command: \"setgoodbyemessage\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                await ctx.send(f"The following message is set as the goodbye message: \"{custom_goodbye_message}\"")# confirms the command in the chat

        savejson(serverid, custom_goodbye_message, "custom_goodbye_message")
        savejson(serverid, send_goodbye_message, "send_goodbye_message")

        dataindexdict = None



@bot.command(name="resetgoodbyemessage")
async def on_message(ctx):

        global send_goodbye_message

        global dataindexdict

        serverid = str(ctx.author.guild.id)

        send_goodbye_message = getjson(serverid, send_goodbye_message, "send_goodbye_message")

        # a way to go back to the defualt goodbye message
        send_goodbye_message = True

        print(f"command: \"resetgoodbyemessage\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

        await ctx.send(f"Icy will send the default message as the goodbye message")# confirms the command in the chat

        savejson(serverid, send_goodbye_message, "send_goodbye_message")

        dataindexdict = None



@bot.command(name="setgoodbyegif")
async def on_message(ctx, *args):

        global custom_goodbye_gif
        global send_goodbye_gif

        global dataindexdict

        serverid = str(ctx.author.guild.id)

        custom_goodbye_gif = getjson(serverid, custom_goodbye_gif, "custom_goodbye_gif")
        send_goodbye_gif = getjson(serverid, send_goodbye_gif, "send_goodbye_gif")

        if "None" in args[0] or "none" in args[0]:

                send_goodbye_gif = False

                await ctx.send("Icy won't add a gif in the goodbye message")


        else:

                custom_goodbye_gif = args

                try:
                        await ctx.send("The following gif will be used as goodbye gif:")
                        await ctx.send(url=custom_welcome_gif)

                except:
                        await ctx.send("Invalid link. Please make sure to give the link of the gif location")

        savejson(serverid, custom_goodbye_gif, "custom_goodbye_gif")
        savejson(serverid, send_goodbye_gif, "send_goodbye_gif")

        dataindexdict = None



@bot.command(name="showgoodbyemembercount")
async def on_message(ctx, *args):

        global goodbye_member_count_show

        global dataindexdict

        serverid = str(ctx.author.guild.id)

        goodbye_member_count_show = getjson(serverid, goodbye_member_count_show, "goodbye_member_count_show")

        if "True" in args[0] or "true" in args[0]:
                goodbye_member_count_show = True

                print(f"command: \"showgoodbyemembercount\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal
                await ctx.send("Icy will add the number of members left")

        elif "False" in args[0] or "false" in args[0]:
                goodbye_member_count_show = False

                print(f"command: \"showgoodbyemembercount\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal
                await ctx.send("Icy won't add the number of members left")

        else:
                heat_up_message = "Please make sure that the input is either \"True\" or \"False\""
                embeded = discord.Embed(title="Icy's heating up..", description=heat_up_message, color=0x5fb79d)

                print(f"command: \"showgoodbyemembercount\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                await ctx.send(embed=embeded)

        savejson(serverid, goodbye_member_count_show, "goodbye_member_count_show")

        dataindexdict = None



@bot.command(name="sendgoodbyeemote")
async def on_message(ctx, *args):

        global send_goodbye_emote

        global dataindexdict

        serverid = str(ctx.author.guild.id)

        send_goodbye_emote = getjson(serverid, send_goodbye_emote, "send_goodbye_emote")

        if "True" in args[0] or "true" in args[0]:
                send_goodbye_emote = True

                print(f"command: \"sendgoodbyeemote\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal
                await ctx.send("Icy will add the emoticon in the goodbye message")

        elif "False" in args[0] or "false" in args[0]:
                send_goodbye_emote = False

                print(f"command: \"sendgoodbyeemote\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal
                await ctx.send("Icy won't add the emoticon in the goodbye message")

        else:
                heat_up_message = "Please make sure that the input is either \"True\" or \"False\""
                embeded = discord.Embed(title="Icy's heating up..", description=heat_up_message, color=0x5fb79d)

                print(f"command: \"sendgoodbyeemote\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                await ctx.send(embed=embeded)

        savejson(serverid, send_goodbye_emote, "send_goodbye_emote")

        dataindexdict = None



@bot.command(name="setgoodbyethumbnail")
async def on_message(ctx, *args):

        global custom_goodbye_thumbnail

        global dataindexdict

        serverid = str(ctx.author.guild.id)

        custom_goodbye_thumbnail = getjson(serverid, custom_goodbye_thumbnail, "custom_goodbye_thumbnail")

        if "None" in args[0] or "none" in args[0]:

                custom_goodbye_thumbnail = None

                print(f"command: \"setgoodbyethumbnail\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal
                await ctx.send("Icy will add the user profile picture as the thumbnail, to stop that use command: \"icy removegoodbyethumbnail\"")

        else:

                custom_goodbye_thumbnail = args[0]

                print(f"command: \"setgoodbyethumbnail\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal
                

                try:
                        await ctx.send("The following image will be used as the goodbye thumbnail:")
                        await ctx.send(url=custom_goodbye_thumbnail)

                except:
                        heat_up_message = "Invalid link. Please make sure that the image location is correct"
                        embeded = discord.Embed(title="Icy's heating up..", description=heat_up_message, color=0x5fb79d)

                        await ctx.send(embed=embeded)

        savejson(serverid, custom_goodbye_thumbnail, "custom_goodbye_thumbnail")

        dataindexdict = None



@bot.command(name="sendgoodbyethumbnail")
async def on_message(ctx, *args):

        global send_goodbye_thumbnail

        global dataindexdict

        serverid = str(ctx.author.guild.id)

        send_goodbye_thumbnail = getjson(serverid, send_goodbye_thumbnail, "send_goodbye_thumbnail")

        if "True" in args[0] or "true" in args[0]:
                send_goodbye_thumbnail = True

                print(f"command: \"sendgoodbyethumbnail\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal
                await ctx.send("Icy will add the thumbnail in the goodbye message")

        elif "False" in args[0] or "false" in args[0]:
                send_goodbye_thumbnail = False

                print(f"command: \"sendgoodbyethumbnail\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal
                await ctx.send("Icy won't add the thumbnail in the goodbye message")

        else:
                heat_up_message = "Please make sure that the input is either \"True\" or \"False\""
                embeded = discord.Embed(title="Icy's heating up..", description=heat_up_message, color=0x5fb79d)

                print(f"command: \"sendgoodbyethumbnail\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                await ctx.send(embed=embeded)

        savejson(serverid, send_goodbye_thumbnail, "send_goodbye_thumbnail")

        dataindexdict = None



@bot.command("setwelcomedm")
async def on_message(ctx, *args):

        global send_welcome_dm
        global custom_welcome_dm

        global dataindexdict

        serverid = str(ctx.author.guild.id)

        send_welcome_dm = getjson(serverid, send_welcome_dm, "send_welcome_dm")
        custom_welcome_dm = getjson(serverid, custom_welcome_dm, "custom_welcome_dm")

        if "None" in args[0] or "none" in args[0]:
                send_welcome_dm = False

                print(f"command: \"setwelcomedm\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal
                await ctx.send("Icy won't send a dm to the new user")

        else:

                send_welcome_dm = True
                custom_welcome_dm = extract_string(args)


                print(f"command: \"setwelcomedm\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal
                
                await ctx.send(f"Icy will send the following dm to the new user: \"{custom_welcome_dm}\"")

        savejson(serverid, send_welcome_dm, "send_welcome_dm")
        savejson(serverid, custom_welcome_dm, "custom_welcome_dm")

        dataindexdict = None





@bot.command("testjoin")
async def on_message(ctx):

        global custom_welcome_message
        global send_welcome_gif
        global custom_welcome_gif
        global send_welcome_message
        global welcome_member_count_show
        global send_welcome_emote
        global custom_welcome_thumbnail
        global send_welcome_thumbnail

        global send_welcome_dm
        global custom_welcome_dm

        global autoroles

        global dataindexdict


        # sets the server variable as a guild object
        server = ctx.author.guild
        serverid = str(server.id)


        if True:
                
                        custom_welcome_message    = getjson(serverid, custom_welcome_message, "custom_welcome_message")
                        send_welcome_gif          = getjson(serverid, send_welcome_gif, "send_welcome_gif")
                        custom_welcome_gif        = getjson(serverid, custom_welcome_gif, "custom_welcome_gif")
                        send_welcome_message      = getjson(serverid, send_welcome_message, "send_welcome_message")
                        welcome_member_count_show = getjson(serverid, welcome_member_count_show, "welcome_member_count_show")
                        send_welcome_emote        = getjson(serverid, send_welcome_emote, "send_welcome_emote")
                        custom_welcome_thumbnail  = getjson(serverid, custom_welcome_thumbnail, "custom_welcome_thumbnail")
                        send_welcome_thumbnail    = getjson(serverid, send_welcome_thumbnail, "send_welcome_thumbnail")
                        send_welcome_dm           = getjson(serverid, send_welcome_dm, "send_welcome_dm")
                        custom_welcome_dm         = getjson(serverid, custom_welcome_dm, "custom_welcome_dm")
                        autoroles                 = getjson(serverid, autoroles, "autoroles")

                        dataindexdict = None



        member_number = len(server.members)# gets the number of members in the server


        if not send_welcome_message:

                # if the welcome message is turned off by the admin
                welcome_message_text = None
        else:

                # the default welcome message to be used when custom message isn't given
                welcome_message_text = f"WELCOMEEEE to {server.name}, glad to have you here and hope you enjoy your stay"

                # when welcome message is set up
                if custom_welcome_message:

                        # checks if there is a custom message given by the admin when a user enters
                        welcome_message_text = custom_welcome_message



        # all the default welcome gifs
        welcome_gifs = (
                "https://media1.tenor.com/images/6830c5f9430da0b5bd9f3e55f66a4fca/tenor.gif?itemid=19063102",
                "https://media1.tenor.com/images/08c2c8535404c39f2fb3cb5de85c97d7/tenor.gif?itemid=16281444",
                "https://media1.tenor.com/images/c5fad21f9828d19044a58f8b84a6e14b/tenor.gif?itemid=6013419",
                "https://media1.tenor.com/images/5210b05939cdafd508346f8e714c1595/tenor.gif?itemid=17715386",
        )



        title = f"WELCOME TO {server.name}"# the main title for welcome message
        name = f"Welcome {ctx.author.name}#{ctx.author.discriminator}"# welcomes the user with the full username
        members = f"**server now has {member_number} members!!!**"# variable for the member count of the server(can be removed)



        embeded = discord.Embed(title=title, description=None, color=0x8871bf)# sets the title
        

        # customizing the member count and the emoji thingy and adding the welcome message in the embed
        if send_welcome_emote and welcome_member_count_show:

                # when all the varriables are to be sent
                value = welcome_message_text + "\n" + members + "\n" + "(>̃ ㅅ<̃)"

                embeded.add_field(name=name, value=value, inline=False)# the main welocme message and shows the number of members and the emoji thingy
        elif send_welcome_emote and not welcome_member_count_show:

                # when the emote and the message is to be sent without the member count
                value = welcome_message_text + "\n" + "(>̃ ㅅ<̃)"

                embeded.add_field(name=name, value=value, inline=False)# the main welocme message and shows only the the emoji thingy
        elif not send_welcome_emote and welcome_member_count_show:
                
                # when only the member count and the message is to be sent without the emote
                value = welcome_message_text + "\n" + members

                embeded.add_field(name=name, value=value, inline=False)# the main welocme message and shows the number of members and not the emoji thingy
        else:

                # when both the emote and the member left count is removed
                if not welcome_message_text:
                        name = "**" + name + "**"
                        embeded = discord.Embed(title=title, description=name, color=0x8871bf)# sets the title
                else:
                        value = welcome_message_text
                
                        embeded.add_field(name=name, value=value, inline=False)# the main welocme message

        if send_welcome_thumbnail:

                if custom_welcome_thumbnail:
                        # if a custom thumbnail is given by the admin
                        thumbnail = custom_welcome_thumbnail
                else:
                        # by default the welcome message thumbnail is the user avatar
                        thumbnail = ctx.author.avatar_url# gets the user avatar
                
                embeded.set_thumbnail(url=thumbnail)# sets the thumbnail(shows the user avatar or the custom thumbnail in the side)

        if send_welcome_gif:

                if custom_welcome_gif:
                        #checks if there is a custom gif given by the admin for welcome message
                        welcome_gif = custom_welcome_gif
                else:
                        # selects any random welcome gif when a custom gif isn't given by the admin
                        welcome_gif = random.choice(welcome_gifs)

                embeded.set_image(url=welcome_gif)# sets the gif as the main image in embed

        
        await ctx.send(embed=embeded)


        # checks if the autoroles are setted up
        if autoroles:
                for role in autoroles:

                        # adds the role/roles to the user
                        await ctx.author.add_roles(role)


        if send_welcome_dm:

                dm_text = f'Hiiiiiiiiiii {ctx.author.name}, welcomeeeeeeeee to {ctx.author.guild.name}, hope you enjoy your stay :)'

                if custom_welcome_dm:
                        dm_text = custom_welcome_dm

                await ctx.author.create_dm()# creates a dm channel with the user
                await ctx.author.dm_channel.send(
                        # sends the dm to the user
                        dm_text
                )



@bot.command("testleave")
async def on_message(ctx):

        global custom_goodbye_message
        global send_goodbye_gif
        global custom_goodbye_gif
        global send_goodbye_message
        global goodbye_member_count_show
        global send_goodbye_emote
        global custom_goodbye_thumbnail
        global send_goodbye_thumbnail

        global dataindexdict


        # sets the server variable as a guild object
        server = ctx.author.guild
        serverid = str(server.id)


        if True:

                custom_goodbye_message    = getjson(serverid, custom_goodbye_message, "custom_goodbye_message")
                send_goodbye_gif          = getjson(serverid, send_goodbye_gif, "send_goodbye_gif")
                custom_goodbye_gif        = getjson(serverid, custom_goodbye_gif, "custom_goodbye_gif")
                send_goodbye_message      = getjson(serverid, send_goodbye_message, "send_goodbye_message")
                goodbye_member_count_show = getjson(serverid, goodbye_member_count_show, "goodbye_member_count_show")
                send_goodbye_emote        = getjson(serverid, send_goodbye_emote, "send_goodbye_emote")
                custom_goodbye_thumbnail  = getjson(serverid, custom_goodbye_thumbnail, "custom_goodbye_thumbnail")
                send_goodbye_thumbnail    = getjson(serverid, send_goodbye_thumbnail, "send_goodbye_thumbnail")

                dataindexdict = None



        member_number = len(server.members)# gets the number of server members

        if not send_goodbye_message:

                # if the goodbye message is turned off by the admin
                goodbye_message_text = None
        else:

                # the default goodbye message to be used when custom message isn't given
                goodbye_message_text = f"Goodbye {ctx.author.name}, hope you enjoyed your stay"

                # when goodbye message is set up
                if custom_goodbye_message:

                        # checks if there is a custom message given by the admin
                        goodbye_message_text = custom_goodbye_message



        # all default the goodbye gifs
        goodbye_gifs = (
                "https://media1.tenor.com/images/6ff14029eb25bbbe796bcec5112eff67/tenor.gif?itemid=17172673",
                "https://media1.tenor.com/images/86a81a4a4e63afc759800f452b396787/tenor.gif?itemid=15151699",
                "https://media1.tenor.com/images/9555ccb50d3ca7fb8a705411da351272/tenor.gif?itemid=17194414",
                "https://media1.tenor.com/images/699f87bf9ab92a23cbec699b7cc002dc/tenor.gif?itemid=15875440",
        )



        title = f"{ctx.author.name} left {server.name}..."# the main title of the goodbye message
        name = f"Goodbye {ctx.author.name}#{ctx.author.discriminator}"# says goodbye to the user
        members = f"now we have {member_number} members left"# variable to show the member count(can be turned off)



        embeded = discord.Embed(title=title, description=None, color=0x8871bf)# sets the title


        # customizing the member count and the emoji thingy and adding the goodbye message in the embed
        if send_goodbye_emote and goodbye_member_count_show:

                # when all the varriables are to be sent
                value = goodbye_message_text + "\n" + members + "\n" + "( ╥︣ ﹏ ╥︣ )"

                embeded.add_field(name=name, value=value, inline=False)# the main goodbye message and shows the number of members and the emoji thingy
        elif send_goodbye_emote and not goodbye_member_count_show:

                # when the emote and the message is to be sent without the member count
                value = goodbye_message_text + "\n" + "( ╥︣ ﹏ ╥︣ )"

                embeded.add_field(name=name, value=value, inline=False)# the main goodbye message and shows only the the emoji thingy
        elif not send_goodbye_emote and goodbye_member_count_show:

                # when only the member count and the message is to be sent without the emote
                value = goodbye_message_text + "\n" + members

                embeded.add_field(name=name, value=value, inline=False)# the main goodbye message and shows the number of members and not the emoji thingy
        else:

                # when both the emote and the member left count is removed
                if not goodbye_message_text:
                        name = "**" + name + "**"

                        embeded = discord.Embed(title=title, description=name, color=0x8871bf)# sets the title
                else:
                        value = goodbye_message_text
                        
                        embeded.add_field(name=name, value=value, inline=False)# the main goodbye message

        if send_goodbye_thumbnail:

                if custom_goodbye_thumbnail:
                        # if a custom thumbnail is given by the admin
                        thumbnail = custom_goodbye_thumbnail
                else:
                        # by default the goodbye message thumbnail is the user avatar
                        thumbnail = ctx.author.avatar_url# gets the user avatar

                embeded.set_thumbnail(url=thumbnail)# sets the thumbnail(shows the user avatar or the custom thumbnail in the side)

        if send_goodbye_gif:

                if custom_goodbye_gif:
                        #checks if there is a custom gif given by the admin for goodbye message
                        goodbye_gif = custom_goodbye_gif
                else:
                        # selects any random goodbye gif when a custom gif isn't given by the admin
                        goodbye_gif = random.choice(goodbye_gifs)

                embeded.set_image(url=goodbye_gif)# sets the gif as the main image in embed


        await ctx.send(embed=embeded)





@bot.command(name="autorole")
async def on_message(ctx, *args):

        global autoroles

        global dataindexdict

        serverid = str(ctx.author.guild.id)

        autoroles = getjson(serverid, autoroles, "autoroles")

        autoroles_raw = list(args)# the list containing mentioned roles
        roles = extract_string(args)# gets the roles as string


        for i in autoroles_raw:
                role_id = extract_user_and_role(i)# gets the role id
                role = await commands.RoleConverter().convert(ctx, role_id)# converts id into a role object

                autoroles.append(role)# adds role into the tuple

        # confirmation in the chat
        await ctx.send(f"icy will add {roles}, when a new memer joins")

        savejson(serverid, autoroles, "autoroles")
        dataindexdict = None







#suggestion
@bot.command(name="suggest", help="posts your suggestion in the chat in a better way")
async def on_message(ctx, *args):

        global suggestion_num# gets the global varriable to have the latest number of suggestion in
        global suggestions# the global dictionary to store suggestion info respect to their number

        global dataindexdict

        serverid = str(ctx.author.guild.id)

        suggestion_num = getjson(serverid, suggestion_num, "suggestion_num")
        suggestions = getjson(serverid, suggestions, "suggestions")

        welp = args
        sug = ""

        # extracts the main suggestion
        for i in welp:
                sug = sug + i + " "# contains the suggestion

        suggestion_num = suggestion_num + 1# adds a number to add a suggestion number for the new suggestion

        title = f"Suggestion #{str(suggestion_num)} by {ctx.author}"
        suggested = "Suggestion: "
        suggestion = sug# the main suggestion

        #adds the info in the suggestions info dictionary with name and the suggestion
        suggestion_info = {
                "name": f"{ctx.author.name}#{ctx.author.discriminator}",
                "suggestion": suggestion,
        }


        embeded = discord.Embed(title=title, description="", color=0xe12c7b)# creates the embed
        embeded.add_field(name=suggested, value=suggestion, inline=False)# adds the field contaning the suggestion


        print(f"command: \"suggestion\" sent by:{ctx.author} time:{ctx.message.created_at}")

        await ctx.message.delete()# deletes the original message

        sent_message = await ctx.send(embed=embeded)# varriable is set to be equal to the sent message
        sent_id = str(sent_message.id)# gets the id of the sent message

        message = await commands.MessageConverter().convert(ctx, sent_id)# converts the id into the message object

        # creates an dictionary with associating the suggestion number with suggestion info creating a nested dictionary
        current_suggestion = {suggestion_num : suggestion_info}
        suggestions.update(current_suggestion)


        await message.add_reaction("⬆️")# adds the reaction to the message
        await message.add_reaction("⬇️")# adds the reaction to the message

        savejson(serverid, suggestion_num, "suggestion_num")
        savejson(serverid, suggestions, "suggestions")

        dataindexdict = None



#suggestion accepted
@bot.command(name="accept", help="posts your suggestion in the chat in a better way \nformat: icy accept <suggestion no> <reason>")
async def on_message(ctx, *args):

        global suggestions# imports the global dictionary containing the suggestions

        global dataindexdict

        serverid = str(ctx.author.guild.id)

        suggestions = getjson(serverid, suggestions, "suggestions")

        welp = list(args)

        suggestion_number = welp[0]# gets the suggestion number from the content of the message
        welp.pop(0)# removes the number from the list so it can be used to extract the reason

        reason = ""

        # extracts the reason from the content list
        for i in welp:
                reason = reason + i + " "


        try:

                suggestion_number = str(suggestion_number)# converts the suggestion number to int datatype

                suggester_name = suggestions.get(suggestion_number).get("name")# gets the name from the nested dictionary
                suggestion_content = suggestions.get(suggestion_number).get("suggestion")# gets the main suggestion from the nested dictionart

                title = f"Accepted by {ctx.author}"
                suggested = f"Suggestion #{str(suggestion_number)} by {suggester_name}"

                embeded = discord.Embed(title=title, description="", color=0x73c387)# creates the embed
                embeded.add_field(name=suggested, value=suggestion_content, inline=False)# adds the field containing the  suggestion
                embeded.add_field(name="Reason for acceptance: ", value=reason, inline=False)# adds the field containing the reason for acceptance

        except:

                # if the suggestion isn't present in the suggestions dictionary
                embeded = discord.Embed(title="ERROR", description="suggestion doesn't exists", color=0x090202)


        print(f"command: \"accept\" sent by:{ctx.author} time:{ctx.message.created_at}")

        await ctx.message.delete()# deletes the original message
        await ctx.send(embed=embeded)# sends the embed in the chat

        savejson(serverid, suggestions, "suggestions")

        dataindexdict = None



#suggestion denied
@bot.command(name="deny", help="posts your suggestion in the chat in a better way")
async def on_message(ctx, *args):

        global suggestions# imports the global dictionary containing the suggestions

        global dataindexdict

        serverid = str(ctx.author.guild.id)

        suggestions = getjson(serverid, suggestions, "suggestions")

        welp = list(args)

        suggestion_number = welp[0]# gets the suggestion number from the content of the message
        welp.pop(0)# removes the suggestion number from the content list

        reason = ""

        # extracts the reason from the content list
        for i in welp:
                reason = reason + i + " "


        try:

                suggestion_number = str(suggestion_number)# converts the suggestion number to an int datatype

                suggester_name = suggestions.get(suggestion_number).get("name")# gets the name from the nested dictionary
                suggestion_content = suggestions.get(suggestion_number).get("suggestion")# gets the suggestion from the nested dictionary

                title = f"Denied by {ctx.author}"
                suggested = f"Suggestion #{str(suggestion_number)} by {suggester_name}"

                embeded = discord.Embed(title=title, description="", color=0xdb696a)# creates the embed
                embeded.add_field(name=suggested, value=suggestion_content, inline=False)# adds the field containing the suggestion
                embeded.add_field(name="Reason for denial: ", value=reason, inline=False)# adds the field containing the reason

        except:

                # if the suggestion doesn't exists in the main suggestion dictionary
                embeded = discord.Embed(title="ERROR", description="suggestion doesn't exists", color=0x090202)


        print(f"command: \"deny\" sent by:{ctx.author} time:{ctx.message.created_at}")

        await ctx.message.delete()# deletes the original message
        await ctx.send(embed=embeded)# sends the embed in the chat

        savejson(serverid, suggestions, "suggestions")

        dataindexdict = None



#suggestion considering
@bot.command(name="consider", help="posts your suggestion in the chat in a better way")
async def on_message(ctx, *args):

        global suggestions# imports the global dictionary containing the suggestions

        global dataindexdict

        serverid = str(ctx.author.guild.id)

        suggestions = getjson(serverid, suggestions, "suggestions")

        welp = list(args)

        suggestion_number = welp[0]# gets the suggestion number form the message content
        welp.pop(0)# removes the suggestion number from the list containing the message content

        reason = ""

        # extracts the reason from the content list
        for i in welp:
                reason = reason + i + " "

        try:

                suggestion_number = str(suggestion_number)# converts suggestion number to an int datatype

                suggester_name = suggestions.get(suggestion_number).get("name")# gets the name from the nested dictionary
                suggestion_content = suggestions.get(suggestion_number).get("suggestion")# gets the suggestion from the nested dictionary

                title = f"Considered by {ctx.author}"
                suggested = f"Suggestion #{str(suggestion_number)} by {suggester_name}"

                embeded = discord.Embed(title=title, description="", color=0x7369db)# creates the embed
                embeded.add_field(name=suggested, value=suggestion_content, inline=False)# adds the field containing the suggestion
                embeded.add_field(name="Reason for consideration: ", value=reason, inline=False)# adds the field containing the reason

        except:

                # if the suggestion doesn't exists in the main suggestions dictionary
                embeded = discord.Embed(title="ERROR", description="suggestion doesn't exists", color=0x090202)


        print(f"command: \"consider\" sent by:{ctx.author} time:{ctx.message.created_at}")

        await ctx.message.delete()# deletes the original message
        await ctx.send(embed=embeded)# sends the embed in the chat

        savejson(serverid, suggestions, "suggestions")

        dataindexdict = None







#mute role
@bot.command(name="muterole", help="sets the mute role for the bot", pass_context=True)
async def on_message(ctx, *args):

        global muterole# umports the global varriable so it can again be used in the mute function

        global muted_user_roles

        global dataindexdict

        serverid = str(ctx.author.guild.id)

        muterole = getjson(serverid, muterole, "muterole")

        mentioned_role = args

        muterole = extract_user_and_role(mentioned_role[0])# sets the muterole as mentioned by user in the message


        try :
                role = await commands.RoleConverter().convert(ctx, str(muterole))# converts muterole to a role object
                permissions = discord.Permissions()# sets permissions as a Permissions object from discord lib


                # contains all the values for the permissions for the role and updates them in the permissions object
                permissions.update(
                        read_messages=True,
                        read_message_history=True,
                        view_channel=True,
                        external_emojis=False,
                        deafen_members=False,
                        create_instant_invite=False,
                        use_external_emojis=False,
                        use_voice_activation=False,
                        connect=False,
                        stream=False,
                        change_nickname=False,
                        embed_links=False,
                        speak=False,
                        add_reactions=False,
                        send_messages=False,
                        send_tts_messages=False,
                        view_audit_log=False,
                        view_guild_insights=False,
                        move_members=False,
                        mute_members=False,
                        priority_speaker=False,
                        manage_permissions=False,
                        manage_roles=False,
                        manage_nicknames=False,
                        manage_emojis=False,
                        manage_webhooks=False,
                        manage_channels=False,
                        manage_guild=False,
                        mention_everyone=False,
                        kick_members=False,
                        ban_members=False,
                )

                await role.edit(reason=None, color=0xd7090b, permissions=permissions)# changes the roles perms according to perms mentioned in the permissions tuple

                description = f"{mentioned_role} has been set up as the mute role"# description for the embed
                embeded = discord.Embed(title="Mute Role Setted Up", description=description, color=0x2ca26f)# creates the embed

        except:
                embeded = discord.Embed(title="ERROR", description="Role doesn't exists", color=0x090202)# for the end case where the role entered by user doesn't exists


        print(f"command: \"muterole\" sent by:{ctx.author} time:{ctx.message.created_at}")

        await ctx.send(embed=embeded)# sends the embed in the chat

        savejson(serverid, muterole, "muterole")
        savejson(serverid, muted_user_roles, "muted_user_roles")

        dataindexdict = None



#mute
@bot.command(name="mute", help="mute's the mentioned user")
async def on_message(ctx, *args):

        global muterole# gets the global varriable consisting the mute role

        global muted_user_roles

        global dataindexdict

        serverid = str(ctx.author.guild.id)

        muterole = getjson(serverid, muterole, "muterole")
        savejson(serverid, {}, "muted_user_roles")

        muted_user_roles = getjson(serverid, muted_user_roles, "muted_user_roles")


        muterole_obj = await commands.RoleConverter().convert(ctx, str(muterole))# converts muterole to a role object

        mentioned_user = args
        userid = extract_user_and_role(mentioned_user[0])# gets the userid from the mentioned user string format


        time_of_message = ctx.message.created_at# gets the time at which the message was sent by author

        delay = list(args)# converts the context of the message into a list
        delay.pop(0)# removes the mentioned user

        reason = ""

        timedelta = datetime.timedelta()# creates an empty time lenght to be added into later


        # block to extract the time
        for i in delay:# selects each word from the delay which were split by spaces in the original message

                # if the content is in the format of time
                try :

                        stripped = int(i[:-1])# main check for the try function for time format


                        if "d" in i or "D" in i:# the day gap

                                stripped = int(i[:-1])# slices the last part of the string which will only leave an int part
                                                      # as the input will only consist <number of time><which level> and as level
                                                      # is only one letter it slices it off and leaves a number

                                timedays = datetime.timedelta(days=stripped)# sets the timedays to the no of days in the stripped
                                timedelta = timedelta + timedays# adds the time gap in timedays to the main time gap "timedelta"

                        elif "h" in i or "H" in i:# the hour gap

                                stripped = int(i[:-1])# slices the last part of the string which will only leave an int part

                                timehours = datetime.timedelta(hours=stripped)# sets the timehours to the no of hours in the stripped
                                timedelta = timedelta + timehours# adds the time gap in timehours to the main time gap "timedelta"

                        elif "m" in i or "M" in i:

                                stripped = int(i[:-1])# slices the last part of the string which will only leave an int part

                                timeminutes = datetime.timedelta(minutes=stripped)# sets the timeminutes to the no of minutes in the stripped
                                timedelta = timedelta + timeminutes# adds the time gap in timeminutes to the main time gap "timedelta"

                        elif "s" in i or "S" in i:

                                stripped = int(i[:-1])# slices the last part of the string which will only leave an int part

                                timeseconds = datetime.timedelta(seconds=stripped)# sets the timeseconds to the no of seconds in the stripped
                                timedelta = timedelta + timeseconds# adds the time gap in timeseconds to the main time gap "timedelta"

                except:
                        reason = i# if the content isn't in the format of time it adds it to the reason string


        time_unmute = time_of_message + timedelta# time to unmute the user


        # block to mute and time the unmute
        try:

                member = await commands.MemberConverter().convert(ctx, userid)# converts userid into a member object

                muted_user_role_ids = []

                mentioned_roles_list = member.roles
                mentioned_roles_list.pop(0)


                for i in mentioned_roles_list:

                        await member.remove_roles(i)
                        muted_user_role_ids.append(i.id)


                await member.add_roles(muterole_obj)# adds the muterole to the member

                # if no time is mentioned
                if time_unmute == time_of_message:

                        title = f"{member.name} muted"
                        desc = f"{member.name} has been muted indefinitely"

                        muted_user_roles.update({member.id: muted_user_role_ids})# will only happen when muted indefinitely


                        embeded = discord.Embed(title=title, description=desc, color=0xd60e11)# creates the ember

                        if reason:
                                embeded.add_field(name="Reason", value=reason, inline=False)# adds the reason field to the embed if reason is given

                        await ctx.send(embed=embeded)# sends the embed in the chat

                else :

                        title = f"{member.name} muted"
                        desc = f"{member.name} has been muted for {timedelta}"


                        embeded = discord.Embed(title=title, description=desc, color=0xd60e11)# creates the embed

                        if reason:
                                embeded.add_field(name="Reason", value=reason, inline=False)# adds the reason field to the embed if reason is given

                        await ctx.send(embed=embeded)# sends the embed in the chat

                        print(f"command: \"mute\" sent by:{ctx.author} time:{ctx.message.created_at}")

                        time.sleep(timedelta.total_seconds())

                        for i in mentioned_roles_list:
                        
                                await member.add_roles(i)


                        await member.remove_roles(muterole_obj)# removes the muterole from the user
                        await ctx.send(f"{member.name} is unmuted")# confirms the unmute in the chat


        except:

                # if any error occurs in the try
                embeded = discord.Embed(title="ERROR", description="mentioned user doesn't exist or used in wrong format.", color=0x090202)
                print(f"command: \"mute\" sent by:{ctx.author} time:{ctx.message.created_at}")

                await ctx.send(embed=embeded)# sends the embed in the chat

        savejson(serverid, muted_user_roles, "muted_user_roles")

        dataindexdict = None



#unmute
@bot.command(name="unmute", help="unmutes the mentioned user")
async def on_message(ctx, *args):

        global muterole# gets the global mute role

        global muted_user_roles

        global dataindexdict

        serverid = str(ctx.author.guild.id)

        muted_user_roles = getjson(serverid, muted_user_roles, "muted_user_roles")
        muterole = getjson(serverid, muterole, "muterole")

        user_id = extract_user_and_role(args[0])# gets the user id

        muterole_obj = await commands.RoleConverter().convert(ctx, str(muterole))# converts muterole to a role object

        try:
                # converts the id into the member object
                member = await commands.MemberConverter().convert(ctx, user_id)

                mentioned_roles_id_list = muted_user_roles.get(str(member.id))

                muted_user_roles.pop(str(member.id))

                # removes the mute role from user
                await member.remove_roles(muterole_obj)

                for i in mentioned_roles_id_list:

                        role = await commands.RoleConverter().convert(ctx, str(i))
                        await member.add_roles(role)

                await ctx.send(f"{member.name} has been unmuted")

        except:
                # if the mentioned user is invalid
                embeded = discord.Embed(title="ERROR", description="mentioned user doesn't exists or isn't muted", color=0x090202)
                await ctx.send(embed=embeded)

        savejson(serverid, muted_user_roles, "muted_user_roles")

        dataindexdict = None







#greets the member in weird ways
@bot.command(name="hey", help="greets for you because your stupid ass is too lazy")
async def on_message(ctx, *args):

        welp = args# takes the first argument from the message after the command

        if welp:# checks whether other person has been mentioned

                userid = extract_user_and_role(welp[0])# gets the user id from mentioned
                mentioned = await commands.MemberConverter().convert(ctx, userid)# converts the user id to a member object


                greets_other = [
                        f'heyyyy {mentioned.name}',
                        f'sup {mentioned.name}',
                        f'well well if it isn\'t {mentioned.name}'
                ]

                greet_gifs = [
                        "https://media1.tenor.com/images/3535009c4a5e1d6c611dc436183b2be3/tenor.gif?itemid=17222872",
                        "https://media1.tenor.com/images/134212ba34a8099c993e07a686345f84/tenor.gif?itemid=8215787",
                        "https://media1.tenor.com/images/1cfc32f7e8a85028d8738ebe6c2546f4/tenor.gif",
                        "https://media1.tenor.com/images/8a8969c821880a51372c71d541342d9d/tenor.gif?itemid=17051695",
                        "https://media1.tenor.com/images/e33ba2692a2709b8fbcc8fa5c712a663/tenor.gif?itemid=18377734",
                        "https://media1.tenor.com/images/6ed94dee684b748c25eb840e21adec60/tenor.gif?itemid=16626368",
                        "https://media1.tenor.com/images/254777755be10be26721137259f96e57/tenor.gif?itemid=17298557",
                        "https://media1.tenor.com/images/51550ce52d6b691e4830bff6b441e061/tenor.gif?itemid=17321760",
                        "https://media1.tenor.com/images/1653e12af18cefa75e42f6efbfcc1055/tenor.gif?itemid=15453209",
                        "https://media1.tenor.com/images/cf0088a98ce0493052dcd9bb12d5e61c/tenor.gif?itemid=5473280",
                        "https://media1.tenor.com/images/e60cc0fdc1074fdf52160fe9ad3bd5b3/tenor.gif?itemid=18041517",
                        "https://media1.tenor.com/images/056c584d9335fcabf080ca43e583e3c4/tenor.gif?itemid=8994845",
                        "https://media1.tenor.com/images/c2e21a9d8e17c1d335166dbcbe0bd1bf/tenor.gif?itemid=5459102",
                        "https://media1.tenor.com/images/2ef78ab2f3e2acbf077388e26d3bc2da/tenor.gif?itemid=14815980",
                        "https://media1.tenor.com/images/d10c3d213be6893235d97ae768db8c07/tenor.gif?itemid=4608178",
                        "https://media1.tenor.com/images/a251caa1a2f4ca8db9da1ec9dfd95c2b/tenor.gif?itemid=13358680",
                        "https://media1.tenor.com/images/36aea41cbdf37fa770f1affb573785e0/tenor.gif?itemid=15269190",
                        "https://media1.tenor.com/images/58707124f314cebc98639478e295ea66/tenor.gif?itemid=8644350",
                        "https://media1.tenor.com/images/972424767943ed34a19f6ff2a9cbe976/tenor.gif?itemid=14192312",
                        "https://media1.tenor.com/images/5ff1438afccf129c7f22176e065b12aa/tenor.gif?itemid=12276833",
                        "https://media1.tenor.com/images/a4d30300af7eded0f616578b9ebbeb40/tenor.gif?itemid=5354245",
                        "https://media1.tenor.com/images/a4d30300af7eded0f616578b9ebbeb40/tenor.gif?itemid=5354245",
                        "https://media1.tenor.com/images/43b26f57280c43f77e87a546bf6c6011/tenor.gif?itemid=5634610",
                        "https://media1.tenor.com/images/d55fe094fe9c9272dc768b1462feaff3/tenor.gif?itemid=19114407",
                        "https://media1.tenor.com/images/32e9bad77165434df8f62aac4344967c/tenor.gif?itemid=15792788",
                        "https://media1.tenor.com/images/fcc3854ad5ee2c22eb0189998be4c8f8/tenor.gif?itemid=14835859",
                        "https://media1.tenor.com/images/94cfaf3becbef687fd29dbc8842e70b6/tenor.gif?itemid=17556391",
                        "https://media1.tenor.com/images/99352a7ea80f7e7611d5e4657bd56169/tenor.gif?itemid=14899337",
                        "https://media1.tenor.com/images/98840ed2735a145c48695d25839b7171/tenor.gif?itemid=12096623",
                        "https://media1.tenor.com/images/ee8251069c19304a9937f0dccbcf24f8/tenor.gif?itemid=5517449",
                        "https://media1.tenor.com/images/b0ee305bfadeb98752d7410688a7fcab/tenor.gif?itemid=12719749",
                        "https://media1.tenor.com/images/9ee571803fdbea520d723280a6c2c573/tenor.gif?itemid=15054962",
                        "https://media1.tenor.com/images/1898f99ff4ce6348bb0738c28d2e2894/tenor.gif?itemid=14813413",
                        "https://media1.tenor.com/images/37a585471f5e895489a03ae705430218/tenor.gif?itemid=12142150",
                        "https://media1.tenor.com/images/76402488ccf1f4daac62608add05467a/tenor.gif?itemid=13451206",
                        "https://media1.tenor.com/images/9ee571803fdbea520d723280a6c2c573/tenor.gif?itemid=15054962",
                        "https://cdn.discordapp.com/attachments/785174324264828958/785521976134598677/2020_12_06_0aw_Kleki.png",
                ]



                response_gif = random.choice(greet_gifs)# gets a random gif from the list

                if mentioned.nick and ctx.author.nick:

                        greets_other = [
                                f'heyyyy {mentioned.nick}',
                                f'sup {mentioned.nick}',
                                f'well well if it isn\'t {mentioned.nick}'
                        ]

                        title = f"{ctx.author.nick} says hi to you {mentioned.nick}"
                        response = random.choice(greets_other)# randomly chooses a response from the greet_others list
                elif mentioned.nick and not ctx.author.nick:

                        greets_other = [
                                f'heyyyy {mentioned.nick}',
                                f'sup {mentioned.nick}',
                                f'well well if it isn\'t {mentioned.nick}'
                        ]

                        title = f"{ctx.author.name} says hi to you {mentioned.nick}"
                        response = random.choice(greets_other)# randomly chooses a response from the greet_others list
                elif ctx.author.nick and not mentioned.nick:

                        greets_other = [
                                f'heyyyy {mentioned.name}',
                                f'sup {mentioned.name}',
                                f'well well if it isn\'t {mentioned.name}'
                        ]

                        title = f"{ctx.author.nick} says hi to you {mentioned.name}"
                        response = random.choice(greets_other)# randomly chooses a response from the greet_others list
                else :

                        greets_other = [
                                f'heyyyy {mentioned.name}',
                                f'sup {mentioned.name}',
                                f'well well if it isn\'t {mentioned.name}'
                        ]

                        title = f"{ctx.author.name} says hi to you {mentioned.name}"
                        response = random.choice(greets_other)# randomly chooses a response from the greet_others list


                embeded = discord.Embed(title=title, desc="description just so you know", color=0xdc8dc5)# creates a discord embed with the title and the color
                embeded.add_field(name="for you icy says..." ,value=response, inline=False)# adds a field with name and the response under it
                embeded.set_image(url=response_gif)# sets the gif in the embed


                print(f"command: \"hey\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                await ctx.send(embed=embeded)# sends the embed in the discord chat

        if not welp:# when another user isn't mentioned

                greets_self = [
                        f"heyyyy <@!{ctx.author.id}>",
                        "sup bitch",
                        "heyo",
                        "*fuck am too nervous*",
                        "OwO",
                        "uwu",
                        "shakie shakie",
                        "welpwelpwelp",
                        "lol",
                        "you know, you\'re a waste of hair",
                        "dont talk to me peasant",
                        "st-step bro/sis/sibling-",
                        "dont talk to me peasant",
                        "umm",
                        "flIpPiN moThEr DipIn",
                        "bonk",
                        "flippity dippity you fuckity lickity dickity shitity",
                        "what?",
                        f"hello. <@!{ctx.author.id}>.",
                        "no.",
                        "ew",
                        "schwepite innt mate",
                        "SHAKIESHAKIE WAKIEWAKIE MF",
                        "how you doin 😳",
                        "shut",
                        "no.",
                        "NO.",
                        "NOOOOO.",
                        "ew",
                        "can you just... go away-",
                        "bye",
                        "hate it here",
                        "sup you beautiful son of a beautiful cat 😳",
                        "damnnnnnn",
                        "uhuhuhuhuhuhhh 😳",
                        "hey seggsy 😳",
                        "bye seggsy 😔",
                        "no seggsy 😩",
                        "ew seggsy 😩",
                        "hey 😳",
                        "Owo",
                        "😳",
                        "😏",
                        "😔",
                        "😩",
                ]

                greet_gifs = [
                        "https://media1.tenor.com/images/3535009c4a5e1d6c611dc436183b2be3/tenor.gif?itemid=17222872",
                        "https://media1.tenor.com/images/134212ba34a8099c993e07a686345f84/tenor.gif?itemid=8215787",
                        "https://media1.tenor.com/images/1cfc32f7e8a85028d8738ebe6c2546f4/tenor.gif",
                        "https://media1.tenor.com/images/8a8969c821880a51372c71d541342d9d/tenor.gif?itemid=17051695",
                        "https://media1.tenor.com/images/e33ba2692a2709b8fbcc8fa5c712a663/tenor.gif?itemid=18377734",
                        "https://media1.tenor.com/images/6ed94dee684b748c25eb840e21adec60/tenor.gif?itemid=16626368",
                        "https://media1.tenor.com/images/254777755be10be26721137259f96e57/tenor.gif?itemid=17298557",
                        "https://media1.tenor.com/images/51550ce52d6b691e4830bff6b441e061/tenor.gif?itemid=17321760",
                        "https://media1.tenor.com/images/1653e12af18cefa75e42f6efbfcc1055/tenor.gif?itemid=15453209",
                        "https://media1.tenor.com/images/cf0088a98ce0493052dcd9bb12d5e61c/tenor.gif?itemid=5473280",
                        "https://media1.tenor.com/images/e60cc0fdc1074fdf52160fe9ad3bd5b3/tenor.gif?itemid=18041517",
                        "https://media1.tenor.com/images/056c584d9335fcabf080ca43e583e3c4/tenor.gif?itemid=8994845",
                        "https://media1.tenor.com/images/c2e21a9d8e17c1d335166dbcbe0bd1bf/tenor.gif?itemid=5459102",
                        "https://media1.tenor.com/images/2ef78ab2f3e2acbf077388e26d3bc2da/tenor.gif?itemid=14815980",
                        "https://media1.tenor.com/images/d10c3d213be6893235d97ae768db8c07/tenor.gif?itemid=4608178",
                        "https://media1.tenor.com/images/a251caa1a2f4ca8db9da1ec9dfd95c2b/tenor.gif?itemid=13358680",
                        "https://media1.tenor.com/images/36aea41cbdf37fa770f1affb573785e0/tenor.gif?itemid=15269190",
                        "https://media1.tenor.com/images/58707124f314cebc98639478e295ea66/tenor.gif?itemid=8644350",
                        "https://media1.tenor.com/images/972424767943ed34a19f6ff2a9cbe976/tenor.gif?itemid=14192312",
                        "https://media1.tenor.com/images/5ff1438afccf129c7f22176e065b12aa/tenor.gif?itemid=12276833",
                        "https://media1.tenor.com/images/a4d30300af7eded0f616578b9ebbeb40/tenor.gif?itemid=5354245",
                        "https://media1.tenor.com/images/a4d30300af7eded0f616578b9ebbeb40/tenor.gif?itemid=5354245",
                        "https://media1.tenor.com/images/43b26f57280c43f77e87a546bf6c6011/tenor.gif?itemid=5634610",
                        "https://media1.tenor.com/images/d55fe094fe9c9272dc768b1462feaff3/tenor.gif?itemid=19114407",
                        "https://media1.tenor.com/images/32e9bad77165434df8f62aac4344967c/tenor.gif?itemid=15792788",
                        "https://media1.tenor.com/images/fcc3854ad5ee2c22eb0189998be4c8f8/tenor.gif?itemid=14835859",
                        "https://media1.tenor.com/images/94cfaf3becbef687fd29dbc8842e70b6/tenor.gif?itemid=17556391",
                        "https://media1.tenor.com/images/99352a7ea80f7e7611d5e4657bd56169/tenor.gif?itemid=14899337",
                        "https://media1.tenor.com/images/98840ed2735a145c48695d25839b7171/tenor.gif?itemid=12096623",
                        "https://media1.tenor.com/images/ee8251069c19304a9937f0dccbcf24f8/tenor.gif?itemid=5517449",
                        "https://media1.tenor.com/images/b0ee305bfadeb98752d7410688a7fcab/tenor.gif?itemid=12719749",
                        "https://media1.tenor.com/images/9ee571803fdbea520d723280a6c2c573/tenor.gif?itemid=15054962",
                        "https://media1.tenor.com/images/1898f99ff4ce6348bb0738c28d2e2894/tenor.gif?itemid=14813413",
                        "https://media1.tenor.com/images/37a585471f5e895489a03ae705430218/tenor.gif?itemid=12142150",
                        "https://media1.tenor.com/images/76402488ccf1f4daac62608add05467a/tenor.gif?itemid=13451206",
                        "https://media1.tenor.com/images/9ee571803fdbea520d723280a6c2c573/tenor.gif?itemid=15054962",
                        "https://cdn.discordapp.com/attachments/785174324264828958/785521976134598677/2020_12_06_0aw_Kleki.png",
                ]



                response_gifs = random.choice(greet_gifs)# gets a random gif from the list
                response = random.choice(greets_self)# randomly chooses a response from the greet_self list

                if ctx.author.nick:
                        title = f"Heyyyy {ctx.author.nick}"
                else :
                        title = f"Heyyyy {ctx.author.name}"


                embeded = discord.Embed(title=title, desc="description just so you know", color=0xdc8dc5)# creates a discord embed with the title and the color
                embeded.add_field(name="icy says...", value=response, inline=False)# adds a field with name and the response under it
                embeded.set_image(url=response_gifs)# sets the gif in the embed


                print(f"command: \"hey\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                await ctx.send(embed=embeded)# sends the embed in the discord chat



#dances with you
@bot.command(name="dance", help="dances dances dances")
async def on_message(ctx, *args):

        welp = args# sets welp as the arguments given after the command

        if welp:# checks whether another user is mentioned

                userid = extract_user_and_role(welp[0])# gets the user id from mentioned
                mentioned = await commands.MemberConverter().convert(ctx, userid)# converts the user id to a member object

                dance_gifs = [
                        "https://media1.tenor.com/images/9ee571803fdbea520d723280a6c2c573/tenor.gif?itemid=15054962",
                        "https://media1.tenor.com/images/1898f99ff4ce6348bb0738c28d2e2894/tenor.gif?itemid=14813413",
                        "https://media1.tenor.com/images/56350dfdcd3a5fa4fd66e9e87f9574bb/tenor.gif?itemid=4718162",
                        "https://media1.tenor.com/images/2ba4b3c691dc6a4712ddf9eef7631ca0/tenor.gif?itemid=11984235",
                        "https://media1.tenor.com/images/b230b5d7dfd3b73d1d315bbed99bef67/tenor.gif?itemid=14046968",
                        "https://media1.tenor.com/images/c925511d32350cc04411756d623ebad6/tenor.gif?itemid=13462237",
                        "https://media1.tenor.com/images/8df28ac0b72e04b6f464759d909a160f/tenor.gif?itemid=15776666",
                        "https://media1.tenor.com/images/7b6948d143f331bc5c3730470fd197bf/tenor.gif?itemid=16325823",
                        "https://media1.tenor.com/images/000967a668507d728baa1aec3e38503b/tenor.gif?itemid=19624886",
                        "https://media1.tenor.com/images/1b7201a1d521f676e4fa27f5e7b87d03/tenor.gif?itemid=13076927",
                        "https://media1.tenor.com/images/8fdcda26512797826631511017a11f93/tenor.gif?itemid=9765182",
                        "https://media1.tenor.com/images/04c39f437de3bda67d2dc35bbb563d88/tenor.gif?itemid=12817361",
                        "https://media1.tenor.com/images/d85d9011c6c866057ca2e6780c6fedd8/tenor.gif?itemid=13266349",
                        "https://media1.tenor.com/images/42803ed59f21b034f440243557ff2736/tenor.gif?itemid=11049076",
                        "https://media1.tenor.com/images/97514c64332ac4660b16513fed65de84/tenor.gif?itemid=4874892",
                        "https://media1.tenor.com/images/81c0b8d3c0617d2902319b7f67e6ce01/tenor.gif?itemid=7560551",
                        "https://media1.tenor.com/images/766599022416cc0b7b7b1bd2040eb2db/tenor.gif?itemid=12039886",
                        "https://media1.tenor.com/images/aa9374ef547c871d4626a22d24042d1f/tenor.gif?itemid=10495378",
                        "https://media1.tenor.com/images/40877c628584984f44a5d441000b71bd/tenor.gif?itemid=7627209",
                        "https://media1.tenor.com/images/8f0385b075b2142dde6acc43f0927cbc/tenor.gif?itemid=12200645",
                        "https://media1.tenor.com/images/68514372455203bb299461159aa28056/tenor.gif?itemid=12503868",
                        "https://media1.tenor.com/images/7223978d7ea3087fc36a16c1056d45c5/tenor.gif?itemid=16172051",
                        "https://media1.tenor.com/images/6c21b5fcca08d28b42dacfab6f2f65ab/tenor.gif?itemid=15636787",
                        "https://media1.tenor.com/images/dc24029de47091555c2ecd8ac91d2069/tenor.gif?itemid=13048072",
                        "https://media1.tenor.com/images/078d0df8e8fc0d28533b647326bf8f3d/tenor.gif?itemid=13706721",
                        "https://media1.tenor.com/images/21e860a31f32d5e3e6bdf2963cadfebf/tenor.gif?itemid=5897404",
                        "https://media1.tenor.com/images/c516ca70e76578431857f15f880a93f2/tenor.gif?itemid=9214433",
                        "https://media1.tenor.com/images/bb12086e528b3d977d71c69d6ec0ddf5/tenor.gif?itemid=14919611",
                        "https://media1.tenor.com/images/6662e11ce285527de039e51f2ce48010/tenor.gif?itemid=11956706",
                        "https://media1.tenor.com/images/8deaaa9949ebd265e9a5818402b60395/tenor.gif?itemid=7423521",
                        "https://media1.tenor.com/images/9b89ddf1522e582dad4fd7950f0a62be/tenor.gif?itemid=5646380",
                        "https://media1.tenor.com/images/047aad18b1f360ae0f3f6ef74010fe40/tenor.gif?itemid=19184126",
                        "https://media1.tenor.com/images/ae99d25cb99b543d210446504450d949/tenor.gif?itemid=18755157",
                        "https://media1.tenor.com/images/23b9ab88db7299e78413555e0c57458e/tenor.gif?itemid=9007334",
                        "https://media1.tenor.com/images/6a85fa01a531afd84a54ba7c008a367a/tenor.gif?itemid=12042607",
                        "https://media1.tenor.com/images/37a585471f5e895489a03ae705430218/tenor.gif?itemid=12142150",
                        "https://media1.tenor.com/images/76402488ccf1f4daac62608add05467a/tenor.gif?itemid=13451206",
                        "https://media1.tenor.com/images/0884bb89a026d49791aa404008843108/tenor.gif?itemid=12793536",
                ]



                response_gif = random.choice(dance_gifs)# gets a random gif from the list

                if mentioned.nick and ctx.author.nick:
                        title = f"{ctx.author.nick} wanna dance with you {mentioned.nick}"
                        response = f"dance {mentioned.nick}, dance with me baby"
                elif mentioned.nick and not ctx.author.nick:
                        title = f"{ctx.author.name} wanna dance with you {mentioned.nick}"
                        response = f"dance {mentioned.nick}, dance with me baby"
                elif ctx.author.nick and not mentioned.nick:
                        title = f"{ctx.author.nick} wanna dance with you {mentioned.name}"
                        response = f"dance {mentioned.name}, dance with me baby"
                else :
                        title = f"{ctx.author.name} wanna dance with you {mentioned.name}"
                        response = f"dance {mentioned.name}, dance with me baby"


                embeded = discord.Embed(title=title, desc="description just so you know", color=0x7a62ad)# creates a discord embed with the title and the color
                embeded.add_field(name="dance baby dance with me" ,value=response, inline=False)# adds a field with name and the response under it
                embeded.set_image(url=response_gif)# sets the gif in the embed


                print(f"command: \"dance\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                await ctx.send(embed=embeded)# sends the embed in the discord chat

        if not welp:# when another user isn't mentioned

                dance_gifs = [
                        "https://media1.tenor.com/images/9ee571803fdbea520d723280a6c2c573/tenor.gif?itemid=15054962",
                        "https://media1.tenor.com/images/1898f99ff4ce6348bb0738c28d2e2894/tenor.gif?itemid=14813413",
                        "https://media1.tenor.com/images/56350dfdcd3a5fa4fd66e9e87f9574bb/tenor.gif?itemid=4718162",
                        "https://media1.tenor.com/images/2ba4b3c691dc6a4712ddf9eef7631ca0/tenor.gif?itemid=11984235",
                        "https://media1.tenor.com/images/b230b5d7dfd3b73d1d315bbed99bef67/tenor.gif?itemid=14046968",
                        "https://media1.tenor.com/images/c925511d32350cc04411756d623ebad6/tenor.gif?itemid=13462237",
                        "https://media1.tenor.com/images/8df28ac0b72e04b6f464759d909a160f/tenor.gif?itemid=15776666",
                        "https://media1.tenor.com/images/7b6948d143f331bc5c3730470fd197bf/tenor.gif?itemid=16325823",
                        "https://media1.tenor.com/images/000967a668507d728baa1aec3e38503b/tenor.gif?itemid=19624886",
                        "https://media1.tenor.com/images/1b7201a1d521f676e4fa27f5e7b87d03/tenor.gif?itemid=13076927",
                        "https://media1.tenor.com/images/8fdcda26512797826631511017a11f93/tenor.gif?itemid=9765182",
                        "https://media1.tenor.com/images/04c39f437de3bda67d2dc35bbb563d88/tenor.gif?itemid=12817361",
                        "https://media1.tenor.com/images/d85d9011c6c866057ca2e6780c6fedd8/tenor.gif?itemid=13266349",
                        "https://media1.tenor.com/images/42803ed59f21b034f440243557ff2736/tenor.gif?itemid=11049076",
                        "https://media1.tenor.com/images/97514c64332ac4660b16513fed65de84/tenor.gif?itemid=4874892",
                        "https://media1.tenor.com/images/81c0b8d3c0617d2902319b7f67e6ce01/tenor.gif?itemid=7560551",
                        "https://media1.tenor.com/images/766599022416cc0b7b7b1bd2040eb2db/tenor.gif?itemid=12039886",
                        "https://media1.tenor.com/images/aa9374ef547c871d4626a22d24042d1f/tenor.gif?itemid=10495378",
                        "https://media1.tenor.com/images/40877c628584984f44a5d441000b71bd/tenor.gif?itemid=7627209",
                        "https://media1.tenor.com/images/8f0385b075b2142dde6acc43f0927cbc/tenor.gif?itemid=12200645",
                        "https://media1.tenor.com/images/68514372455203bb299461159aa28056/tenor.gif?itemid=12503868",
                        "https://media1.tenor.com/images/7223978d7ea3087fc36a16c1056d45c5/tenor.gif?itemid=16172051",
                        "https://media1.tenor.com/images/6c21b5fcca08d28b42dacfab6f2f65ab/tenor.gif?itemid=15636787",
                        "https://media1.tenor.com/images/dc24029de47091555c2ecd8ac91d2069/tenor.gif?itemid=13048072",
                        "https://media1.tenor.com/images/078d0df8e8fc0d28533b647326bf8f3d/tenor.gif?itemid=13706721",
                        "https://media1.tenor.com/images/21e860a31f32d5e3e6bdf2963cadfebf/tenor.gif?itemid=5897404",
                        "https://media1.tenor.com/images/c516ca70e76578431857f15f880a93f2/tenor.gif?itemid=9214433",
                        "https://media1.tenor.com/images/bb12086e528b3d977d71c69d6ec0ddf5/tenor.gif?itemid=14919611",
                        "https://media1.tenor.com/images/6662e11ce285527de039e51f2ce48010/tenor.gif?itemid=11956706",
                        "https://media1.tenor.com/images/8deaaa9949ebd265e9a5818402b60395/tenor.gif?itemid=7423521",
                        "https://media1.tenor.com/images/9b89ddf1522e582dad4fd7950f0a62be/tenor.gif?itemid=5646380",
                        "https://media1.tenor.com/images/047aad18b1f360ae0f3f6ef74010fe40/tenor.gif?itemid=19184126",
                        "https://media1.tenor.com/images/ae99d25cb99b543d210446504450d949/tenor.gif?itemid=18755157",
                        "https://media1.tenor.com/images/23b9ab88db7299e78413555e0c57458e/tenor.gif?itemid=9007334",
                        "https://media1.tenor.com/images/6a85fa01a531afd84a54ba7c008a367a/tenor.gif?itemid=12042607",
                        "https://media1.tenor.com/images/37a585471f5e895489a03ae705430218/tenor.gif?itemid=12142150",
                        "https://media1.tenor.com/images/76402488ccf1f4daac62608add05467a/tenor.gif?itemid=13451206",
                        "https://media1.tenor.com/images/0884bb89a026d49791aa404008843108/tenor.gif?itemid=12793536",
                ]



                response_gif = random.choice(dance_gifs)# gets a random gif from the list

                if ctx.author.nick:
                        title = f"{ctx.author.nick} is dancing"
                        response = f"dance baby dance with me baby"
                else :
                        title = f"{ctx.author.name} is dancing"
                        response = f"dance baby dance with me baby"


                embeded = discord.Embed(title=title, desc="description just so you know", color=0x7a62ad)# creates a discord embed with the title and the color
                embeded.add_field(name="dance baby dance with me" ,value=response, inline=False)# adds a field with name and the response under it
                embeded.set_image(url=response_gif)# sets the gif in the embed


                print(f"command: \"dance\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                await ctx.send(embed=embeded)# sends the embed in the discord chat



#gives a kiss
@bot.command(name="kiss", help="dances dances dances")
async def on_message(ctx, *args):

        welp = args# sets welp as the arguments given after the command

        if welp:# checks whether another user is mentioned

                userid = extract_user_and_role(welp[0])# gets the user id from mentioned
                mentioned = await commands.MemberConverter().convert(ctx, userid)# converts the user id to a member object


                kiss_gifs = [
                        "https://media1.tenor.com/images/4d5566be4e1bef0ceb5a5a108ebf5676/tenor.gif?itemid=15384224",
                        "https://media1.tenor.com/images/f5167c56b1cca2814f9eca99c4f4fab8/tenor.gif?itemid=6155657",
                        "https://media1.tenor.com/images/78095c007974aceb72b91aeb7ee54a71/tenor.gif?itemid=5095865",
                        "https://media1.tenor.com/images/d307db89f181813e0d05937b5feb4254/tenor.gif?itemid=16371489",
                        "https://media1.tenor.com/images/7fd98defeb5fd901afe6ace0dffce96e/tenor.gif?itemid=9670722",
                        "https://media1.tenor.com/images/621ceac89636fc46ecaf81824f9fee0e/tenor.gif?itemid=4958649",
                        "https://media1.tenor.com/images/a1f7d43752168b3c1dbdfb925bda8a33/tenor.gif?itemid=10356314",
                        "https://media1.tenor.com/images/bc5e143ab33084961904240f431ca0b1/tenor.gif?itemid=9838409",
                        "https://media1.tenor.com/images/6f455ef36a0eb011a60fad110a44ce68/tenor.gif?itemid=13658106",
                        "https://media1.tenor.com/images/e76e640bbbd4161345f551bb42e6eb13/tenor.gif?itemid=4829336",
                        "https://media1.tenor.com/images/b8d0152fbe9ecc061f9ad7ff74533396/tenor.gif?itemid=5372258",
                        "https://media1.tenor.com/images/02d9cae34993e48ab5bb27763d5ca2fa/tenor.gif?itemid=4874618",
                        "https://media1.tenor.com/images/a390476cc2773898ae75090429fb1d3b/tenor.gif?itemid=12837192",
                        "https://media1.tenor.com/images/1306732d3351afe642c9a7f6d46f548e/tenor.gif?itemid=6155670",
                        "https://media1.tenor.com/images/4b56464510f4c9cfbec9eda5a25c3a72/tenor.gif?itemid=17193768",
                        "https://media1.tenor.com/images/4b5d5afd747fe053ed79317628aac106/tenor.gif?itemid=5649376",
                        "https://media1.tenor.com/images/9fac3eab2f619789b88fdf9aa5ca7b8f/tenor.gif?itemid=12925177",
                        "https://media1.tenor.com/images/4c66d14c58838d05376b5d2712655d91/tenor.gif?itemid=15009390",
                        "https://media1.tenor.com/images/105a7ad7edbe74e5ca834348025cc650/tenor.gif?itemid=9158317",
                        "https://media1.tenor.com/images/f34f73decaef049f9354b27984dfb09c/tenor.gif?itemid=14958166",
                        "https://media1.tenor.com/images/31bba031acb022eaf437214be20da84d/tenor.gif?itemid=11830666",
                        "https://media1.tenor.com/images/693602b39a071644cebebdce7c459142/tenor.gif?itemid=6206552",
                        "https://media1.tenor.com/images/632a3db90c6ecd87f1242605f92120c7/tenor.gif?itemid=5608449",
                        "https://media1.tenor.com/images/227aa4313c6c4d4e2091148f4fa37645/tenor.gif?itemid=13975815",
                        "https://media1.tenor.com/images/230e9fd40cd15e3f27fc891bac04248e/tenor.gif?itemid=14751754",
                        "https://media1.tenor.com/images/37633f0b8d39daf70a50f69293e303fc/tenor.gif?itemid=13344412",
                        "https://media1.tenor.com/images/61dba0b61a2647a0663b7bde896c966c/tenor.gif?itemid=5262571",
                        "https://media1.tenor.com/images/68a37a5a1b86f227b8e1169f33a6a6bb/tenor.gif?itemid=13344389",
                        "https://media1.tenor.com/images/7ea0b8822e5390c2393ef6f18a40893d/tenor.gif?itemid=16687888",
                        "https://media1.tenor.com/images/49304ecdf46e62f340d1b790734f37c9/tenor.gif?itemid=12982889",
                        "https://media1.tenor.com/images/af1216d35f8ec076b593401b19ddd0bf/tenor.gif?itemid=13188942",
                        "https://media1.tenor.com/images/d93c9a9c201ec1fe3c8011718b18a83c/tenor.gif?itemid=16317577",
                        "https://media1.tenor.com/images/d7bddc2032a53da99f9a3e5bfadf3cf2/tenor.gif?itemid=17708192",
                        "https://media1.tenor.com/images/2182d81bc459732fdf9bf94d1dd068c4/tenor.gif?itemid=6155634",
                        "https://media1.tenor.com/images/ad514e809adc14f0b7722a324c2eb36e/tenor.gif?itemid=14375355",
                        "https://media1.tenor.com/images/4a7cda16c0eb5ef234fab063dac512c2/tenor.gif?itemid=14590116",
                        "https://media1.tenor.com/images/af50852d633a2f77828a7018eed43ea8/tenor.gif?itemid=17845616",
                        "https://media1.tenor.com/images/5654c7b35e067553e99bb996535c0a75/tenor.gif?itemid=10358833",
                        "https://media1.tenor.com/images/6bd9c3ba3c06556935a452f0a3679ccf/tenor.gif?itemid=13387677",
                        "https://media1.tenor.com/images/d7296b6473bbf41490b5448db41b7f68/tenor.gif?itemid=17706821",
                        "https://media1.tenor.com/images/d9115cb8f24162cf70428d8cb8d96558/tenor.gif?itemid=9382690",
                ]



                response_gif = random.choice(kiss_gifs)# gets a random gif from the list

                if mentioned.nick and ctx.author.nick:
                        title = f"{ctx.author.nick} is giving you a kiss {mentioned.nick}"
                        response = f"kiss has shared a kiss with {mentioned.nick}"
                elif mentioned.nick and not ctx.author.nick:
                        title = f"{ctx.author.name} is giving you a kiss {mentioned.nick}"
                        response = f"kiss has shared a kiss with {mentioned.nick}"
                elif ctx.author.nick and not mentioned.nick:
                        title = f"{ctx.author.nick} is giving you a kiss {mentioned.name}"
                        response = f"kiss has shared a kiss with {mentioned.name}"
                else :
                        title = f"{ctx.author.name} is giving you a kiss {mentioned.name}"
                        response = f"kiss has shared a kiss with {mentioned.name}"


                embeded = discord.Embed(title=title, desc="description just so you know", color=0x7a62ad)# creates a discord embed with the title and the color
                embeded.add_field(name="Kiss meeee" ,value=response, inline=False)# adds a field with name and the response under it
                embeded.set_image(url=response_gif)# sets the gif in the embed


                print(f"command: \"kiss\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                await ctx.send(embed=embeded)# sends the embed in the discord chat

        if not welp:# when another user isn't mentioned

                kiss_gifs = [
                        "https://media1.tenor.com/images/4d5566be4e1bef0ceb5a5a108ebf5676/tenor.gif?itemid=15384224",
                        "https://media1.tenor.com/images/f5167c56b1cca2814f9eca99c4f4fab8/tenor.gif?itemid=6155657",
                        "https://media1.tenor.com/images/78095c007974aceb72b91aeb7ee54a71/tenor.gif?itemid=5095865",
                        "https://media1.tenor.com/images/d307db89f181813e0d05937b5feb4254/tenor.gif?itemid=16371489",
                        "https://media1.tenor.com/images/7fd98defeb5fd901afe6ace0dffce96e/tenor.gif?itemid=9670722",
                        "https://media1.tenor.com/images/621ceac89636fc46ecaf81824f9fee0e/tenor.gif?itemid=4958649",
                        "https://media1.tenor.com/images/a1f7d43752168b3c1dbdfb925bda8a33/tenor.gif?itemid=10356314",
                        "https://media1.tenor.com/images/bc5e143ab33084961904240f431ca0b1/tenor.gif?itemid=9838409",
                        "https://media1.tenor.com/images/6f455ef36a0eb011a60fad110a44ce68/tenor.gif?itemid=13658106",
                        "https://media1.tenor.com/images/e76e640bbbd4161345f551bb42e6eb13/tenor.gif?itemid=4829336",
                        "https://media1.tenor.com/images/b8d0152fbe9ecc061f9ad7ff74533396/tenor.gif?itemid=5372258",
                        "https://media1.tenor.com/images/02d9cae34993e48ab5bb27763d5ca2fa/tenor.gif?itemid=4874618",
                        "https://media1.tenor.com/images/a390476cc2773898ae75090429fb1d3b/tenor.gif?itemid=12837192",
                        "https://media1.tenor.com/images/1306732d3351afe642c9a7f6d46f548e/tenor.gif?itemid=6155670",
                        "https://media1.tenor.com/images/4b56464510f4c9cfbec9eda5a25c3a72/tenor.gif?itemid=17193768",
                        "https://media1.tenor.com/images/4b5d5afd747fe053ed79317628aac106/tenor.gif?itemid=5649376",
                        "https://media1.tenor.com/images/9fac3eab2f619789b88fdf9aa5ca7b8f/tenor.gif?itemid=12925177",
                        "https://media1.tenor.com/images/4c66d14c58838d05376b5d2712655d91/tenor.gif?itemid=15009390",
                        "https://media1.tenor.com/images/105a7ad7edbe74e5ca834348025cc650/tenor.gif?itemid=9158317",
                        "https://media1.tenor.com/images/f34f73decaef049f9354b27984dfb09c/tenor.gif?itemid=14958166",
                        "https://media1.tenor.com/images/31bba031acb022eaf437214be20da84d/tenor.gif?itemid=11830666",
                        "https://media1.tenor.com/images/693602b39a071644cebebdce7c459142/tenor.gif?itemid=6206552",
                        "https://media1.tenor.com/images/632a3db90c6ecd87f1242605f92120c7/tenor.gif?itemid=5608449",
                        "https://media1.tenor.com/images/227aa4313c6c4d4e2091148f4fa37645/tenor.gif?itemid=13975815",
                        "https://media1.tenor.com/images/230e9fd40cd15e3f27fc891bac04248e/tenor.gif?itemid=14751754",
                        "https://media1.tenor.com/images/37633f0b8d39daf70a50f69293e303fc/tenor.gif?itemid=13344412",
                        "https://media1.tenor.com/images/61dba0b61a2647a0663b7bde896c966c/tenor.gif?itemid=5262571",
                        "https://media1.tenor.com/images/68a37a5a1b86f227b8e1169f33a6a6bb/tenor.gif?itemid=13344389",
                        "https://media1.tenor.com/images/7ea0b8822e5390c2393ef6f18a40893d/tenor.gif?itemid=16687888",
                        "https://media1.tenor.com/images/49304ecdf46e62f340d1b790734f37c9/tenor.gif?itemid=12982889",
                        "https://media1.tenor.com/images/af1216d35f8ec076b593401b19ddd0bf/tenor.gif?itemid=13188942",
                        "https://media1.tenor.com/images/d93c9a9c201ec1fe3c8011718b18a83c/tenor.gif?itemid=16317577",
                        "https://media1.tenor.com/images/d7bddc2032a53da99f9a3e5bfadf3cf2/tenor.gif?itemid=17708192",
                        "https://media1.tenor.com/images/2182d81bc459732fdf9bf94d1dd068c4/tenor.gif?itemid=6155634",
                        "https://media1.tenor.com/images/ad514e809adc14f0b7722a324c2eb36e/tenor.gif?itemid=14375355",
                        "https://media1.tenor.com/images/4a7cda16c0eb5ef234fab063dac512c2/tenor.gif?itemid=14590116",
                        "https://media1.tenor.com/images/af50852d633a2f77828a7018eed43ea8/tenor.gif?itemid=17845616",
                        "https://media1.tenor.com/images/5654c7b35e067553e99bb996535c0a75/tenor.gif?itemid=10358833",
                        "https://media1.tenor.com/images/6bd9c3ba3c06556935a452f0a3679ccf/tenor.gif?itemid=13387677",
                        "https://media1.tenor.com/images/d7296b6473bbf41490b5448db41b7f68/tenor.gif?itemid=17706821",
                        "https://media1.tenor.com/images/d9115cb8f24162cf70428d8cb8d96558/tenor.gif?itemid=9382690",
                ]



                response_gif = random.choice(kiss_gifs)# gets a random gif from the list

                if ctx.author.nick:
                        title = f"{ctx.author.nick} is kissing random people"
                        response = f"{ctx.author.nick} wanna kiss someone"
                else :
                        title = f"{ctx.author.name} is kissing random people"
                        response = f"{ctx.author.name} wanna kiss someone"


                embeded = discord.Embed(title=title, desc="description just so you know", color=0x7a62ad)# creates a discord embed with the title and the color
                embeded.add_field(name="Someone kiss me " ,value=response, inline=False)# adds a field with name and the response under it
                embeded.set_image(url=response_gif)# sets the gif in the embed


                print(f"command: \"kiss\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                await ctx.send(embed=embeded)# sends the embed in the discord chat







#sends the avatar of the sender
@bot.command(name="av", help="shows your beautiful face")
async def on_message(ctx, *args):

        welp = args# sets welp as the arguments given after the command

        # checks whether another user is mentioned
        try:

                userid = extract_user_and_role(welp[0])# gets the user id from mentioned
                mentioned = await commands.MemberConverter().convert(ctx, userid)# converts the user id to a member object


                avatar = mentioned.avatar_url_as(size=256)# url for the mentioned users avatar

                if mentioned.nick and ctx.author.nick:
                        title = f"here is {mentioned.nick}'s beautiful face for you {ctx.author.nick}"
                elif mentioned.nick and not ctx.author.nick:
                        title = f"here is {mentioned.nick}'s beautiful face for you {ctx.author.name}"
                elif ctx.author.nick and not mentioned.nick:
                        title = f"here is {mentioned.name}'s beautiful face for you {ctx.author.nick}"
                else :
                        title = f"here is {mentioned.name}'s beautiful face for you {ctx.author.name}"


                embeded = discord.Embed(title=title, color=0x5643ba)# creates a discord embed with the title and the color
                embeded.set_image(url=avatar)# sets the user avatar in the embed


                print(f"command: \"av\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                await ctx.send(embed=embeded)# sends the embed in the discord chat



        except:

                if welp:

                        embeded = discord.Embed(title="ERROR", description="User doesn't exists", color=0x090202)
                        await ctx.send(embed=embeded)


                avatar = ctx.author.avatar_url_as(size=256)# url for the users avatar

                if ctx.author.nick:
                        title = f"here's your beautiful face {ctx.author.nick}"
                else :
                        title = f"here's your beautiful face {ctx.author.name}"


                embeded = discord.Embed(title=title, color=0x5643ba)# creates a discord embed with the title and the color
                embeded.set_image(url=avatar)# sets the user avatar in the embed


                print(f"command: \"av\" sent by:{ctx.author} time:{ctx.message.created_at}")# confirms the command and prints info in the terminal

                await ctx.send(embed=embeded)# sends the embed in the discord chat







#
@bot.command(name="showerthought")
async def on_message(ctx):

        global thoughtlimit

        showerthoughts_sub = reddit.subreddit("Showerthoughts")

        author_name = None
        try:
                author_name = {ctx.author.nick}
        except:
                author_name = {ctx.author.name}

        thought = None
        name = f"Thought for you {author_name} is,"

        thoughtlimit += 1
        for submission in showerthoughts_sub.hot(limit=thoughtlimit):
                thought = submission.title

        embeded = discord.Embed(name=name, description="", color=0xe07265)
        embeded.add_field(name=thought, value="have fun ^^- ye idk what to say here", inline=False)

        await ctx.send(embed=embeded)



#
@bot.command(name="meme")
async def on_message(ctx):

        global memelimit

        meme_sub = reddit.subreddit("dankmemes")

        meme_title = None
        meme_url = None
        meme_score = None

        memelimit += 1
        for meme in meme_sub.hot(limit=memelimit):
                meme_title = meme.title
                meme_url = meme.url
                meme_score = meme.score

        embeded = discord.Embed(title=meme_title, description="", color=0xe07265)
        embeded.set_image(url=meme_url)

        await ctx.send(embed=embeded)



#
@bot.command(name="cat")
async def on_message(ctx):

        global catlimit

        cat_sub = reddit.subreddit("cats")

        cat_title = None
        cat_url = None
        cat_score = None

        catlimit += 1
        for cat in cat_sub.hot(limit=catlimit):
                cat_title = cat.title
                cat_url = cat.url
                cat_score = cat.score

        embeded = discord.Embed(title=cat_title, description="", color=0xe07265)
        embeded.set_image(url=cat_url)

        await ctx.send(embed=embeded)







#...
@bot.command(name="daddy", command_prefix="", help="well....")
async def on_message(ctx):

        await ctx.send()







#reminder
@bot.command(name="remindin", help="reminds you in the given time [<hours>h <minutes>m <seconds>s]")
async def on_message(ctx, *args):

        time_of_message = ctx.message.created_at# gets the time at which the message was sent by author
        message_type = ctx.message.type# get's the type of the message

        delay = list(args)# gets the full string after the preffix and the command name

        reminder_message = ""
        reminder_message_true = ""
        reminder_message_dm = ""

        timedelta = datetime.timedelta()# creates an empty time lenght to be added into later
        for i in delay:# selects each word from the delay which were split by spaces in the original message

                try :# checks whether it's a time varriable or a reminder message
                        stripped = int(i[:-1])# checks of the string other than the last letter is a number


                        if "d" in i or "D" in i:# the day gap

                                stripped = int(i[:-1])# slices the last part of the string which will only leave an int part
                                                      # as the input will only consist <number of time><which level> and as level
                                                      # is only one letter it slices it off and leaves a number

                                timedays = datetime.timedelta(days=stripped)# sets the timedays to the no of days in the stripped
                                timedelta = timedelta + timedays# adds the time gap in timedays to the main time gap "timedelta"


                        elif "h" in i or "H" in i:# the hour gap

                                stripped = int(i[:-1])# slices the last part of the string which will only leave an int part

                                timehours = datetime.timedelta(hours=stripped)# sets the timehours to the no of hours in the stripped
                                timedelta = timedelta + timehours# adds the time gap in timehours to the main time gap "timedelta"


                        elif "m" in i or "M" in i:

                                stripped = int(i[:-1])# slices the last part of the string which will only leave an int part

                                timeminutes = datetime.timedelta(minutes=stripped)# sets the timeminutes to the no of minutes in the stripped
                                timedelta = timedelta + timeminutes# adds the time gap in timeminutes to the main time gap "timedelta"


                        elif "s" in i or "S" in i:

                                stripped = int(i[:-1])# slices the last part of the string which will only leave an int part

                                timeseconds = datetime.timedelta(seconds=stripped)# sets the timeseconds to the no of seconds in the stripped
                                timedelta = timedelta + timeseconds# adds the time gap in timeseconds to the main time gap "timedelta"

                except:# if the message doesn't has a number in the front except the last index
                        reminder_message = i# sets the reminder message to the message entered by user


        # for endcase of user entering None time
        if timedelta == datetime.timedelta():
                await ctx.send("If you want me to remind you add some time you numbnuts")
                return None



        time_reminder = time_of_message + timedelta# adds the main timegap to the time message was sent to create the time at which user is to be reminded

        #information to be printed in the terminal for the tests
        print(f"message type = {message_type}")

        print(f"timedelta = {timedelta}")
        print(f"time of the message = {time_of_message}")
        print(f"time to be reminded at = {time_reminder}")

        print(f"reminder message = {reminder_message}")

        # quality of life additions
        if reminder_message:
                reminder_message_true = f" about \"{reminder_message}\""
                reminder_message_dm = f", it's time for \"{reminder_message}\""


        await ctx.send(f"icy thy remind you {ctx.author.name}, in {timedelta}{reminder_message_true}")# the message confirming the reminder

        time.sleep(timedelta.total_seconds())


        await ctx.author.create_dm()# creates an personal dm channel with the author
        await ctx.author.dm_channel.send(f"IT'S TIMEEEEEEE <@!{ctx.author.id}>{reminder_message_dm}")# sends the reminder message as a dm







#make the bot send a message to the mentioned user unless they are in the server
@bot.command(name="message", help="sends a message to the mentioned user")
async def on_message(ctx, *args):

        rest = list(args)# sets the rest as the rest of the message
        mentioned = rest[0]# take out the part that's supposed to contain the mentioned user

        rest.pop(0)# pops out the mentioned

        message_content = " "
        for i in rest:
                message_content = message_content + " " + i


        message_final = f"{mentioned}{message_content}"


        print(f"command: \"message\" sent by:{ctx.author} time:{ctx.message.created_at}")

        await ctx.message.delete()# deletes the original message
        await ctx.send(message_final)# sends the final message







#in development
@bot.command(name="snipe", help="in development")
async def on_message(ctx):
        guild = discord.utils.get(bot.guilds, name=GUILD)# gets the guilds name

        await ctx.send("guild.auditlog")







#test function
@bot.command(name="welp", help="testing command")
async def on_message(ctx):

        global testvar
        global dataindexdict

        listroles = ctx.author.roles
        print(ctx.author.roles[1])
        print(type(ctx.author.roles[1]))
        listroles.pop(0)

        for i in listroles:

                await ctx.author.remove_roles(i)
        
        await ctx.send(ctx.author.roles)
        await ctx.send(type(ctx.author.roles[0]))
        #await ctx.send(listroles.remove(0))

        #with open("C:\\pythonWay\\PROJECTS\\DISCORD_BOT\\testbotdata.json", "r") as jsonfile:
        #        loaddata = json.load(jsonfile)
        #
        #        serverid = str(ctx.author.guild.id)
        #        server_in_file = False
        #        print(f"SERVER ID> {serverid}")
        #
        #        
        #
        #        for i in loaddata["guilddata"]:
        #                #loaddata["guilddata"]
        #                #try:
        #                print("ye")
        #                if i[serverid]:
        #                        print(i)
        #                        print("FUCK YEA")
        #                        server_in_file = True
        #
        #                        dataindex = loaddata["guilddata"].index(i)
        #         
        #                        try:
        #                                print("JUST GETTING THE VARRIABLE 0")
        #                                testvar = i.get(serverid).get("testvar")
        #                                print("JUST GETTING THE VARRIABLE")
        #                                break
        #
        #                        except:
        #                                print("THE VARIABLE ISN'T PRESENT 0")
        #                                var = {"testvar": "fuck ye THIS WORKS wasn't expecting really..."}
        #
        #                                i.get(serverid).update(var)
        #                                testvar = i[serverid].get("testvar")
        #
        #                                print("THE VARIABLE ISN'T PRESENT")
        #                                break
        #
        #                #except:
        #                #        pass
        #
        #        if server_in_file == False:
        #                print("THE SERVER ISN'T PRESENT IN THE LIST 0")
        #                loaddata["guilddata"].append({serverid: {}})
        #
        #                dataindex = -1
        #                loaddata["guilddata"][-1][serverid].update({"testvar": "fuck ye THIS WORKS wasn't expecting really..."})
        #                testvar = loaddata["guilddata"][-1][serverid].get("testvar")
        #                print("THE SERVER ISN'T PRESENT IN THE LIST")
        #
        #
        #        
        #        #print("MF")
        #        #pass


        #serverid = str(ctx.author.guild.id)
        #testvar2 = None#"welpwelpwelpwelp"
        #testvar = getjson(serverid, testvar, "testvar")
        #testvar2 = getjson(serverid, testvar2, "testvar2")
        #
        #await ctx.send(testvar)
        #
        #savejson(serverid, "sexy", "testvar")
        #savejson(serverid, None, "testvar2")
        #loaddatavar, dataindexdict = None, {}



        ##UPDATING THE VARIALE
        #loaddata["guilddata"][dataindex][serverid].update({"testvar": "welpwelp"})
        #
        ##DUMPS
        #with open("C:\\pythonWay\\PROJECTS\\DISCORD_BOT\\testbotdata.json", "w") as dumpfile:
        #        json.dump(loaddata, dumpfile)
        #
        #
        #        #loaddata["guilddata"][objectindex].get(serverid).update({"testvar": testvar})
        #        #["guilddata"][dataindex][serverid].update({"testvar": "welpwelp"})



        #with open("C:\\pythonWay\\PROJECTS\\DISCORD_BOT\\testbotdata.json", "w") as jsonfile:
        #        
        #        
        #        
        #        json.dump(loaddata, jsonfile)





        #welp = list(args)
        #userid = extract_user_and_role(welp[0])
        #
        #usermember = await commands.MemberConverter().convert(ctx, userid)
        #
        #await ctx.send(f"```name> {usermember.name}```")
        #await ctx.send(f"```id> {usermember.id}```")
        #await ctx.send(f"```time> {ctx.message.created_at}```")
        #
        #embeded = discord.Embed(title="embed fuck yeah", desc="description just so you know", color=0x45b798)
        #embeded.add_field(name="first field- hopefully", value="fuck yeaaaa this is exciting is this first line- hope so", inline=False)
        #embeded.add_field(name="second one- maybeeeee", value="so is this second hopefully it is- nicenice yeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", inline=True)
        #embeded.add_field(name="third one babyyyyyfggggnhgfhgfkgggggggggggy", value="A third- why not", inline=True)
        #
        #await ctx.send(embed=embeded)







#creates a new channel
@bot.command(name="createtextch", help="creates an channel for you.")
@commands.has_role('hot arse')# only admins can use this command
async def create_channel(ctx, name):

        guild = ctx.guild# gets the guild from ctx

        existingch = discord.utils.get(guild.channels, name=name)# checks if the given channel already exists
        if not existingch:
                print(f'Creating new channel: {name}')
                await guild.create_text_channel(name)# creates the channel
                await ctx.send('> done')









bot.run(TOKEN)# runs bot token in TOKEN
