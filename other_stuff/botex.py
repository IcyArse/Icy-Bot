import os
import discord
import random

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')# gets the token of the bot from the .env file so they confidentional token won't be shared in the terminal
GUILD = os.getenv('DISCORD_GUILD')# gets the name of the guild from .env file about which you want the info

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)# makes and discord client

@client.event #client on the following event:
async def on_ready():
        print(f'{client.user} has connected to Discord!')# tells us if the bot is connected and client.user gives the name of the bot from the token
        #guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds) # a better way than this is :
        guild = discord.utils.get(client.guilds, name=GUILD)# gets the server with name same as GUILD from the client.guilds       

        print(f'{client.user} is connected to {guild.name}')# tells us that it is connected to the required guild
        #print(f'{guild.name} id = {guild.id}')# returns the guild id and it's name
        #print(f'{guild.members}')
        #memberss = []
        memberss = [member.name for member in guild.members]# searches for members in guild.members
        print(f'server members are: {memberss}')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hiiiiiiiiiii {member.name}, welcomeeeeeeeee icyyyyyy\'s serverrr'
    )

@client.event
async def on_message(message):
    #if message.author == client.user:
    #    return

    greets = [
                f'heyyyy <@!{client.user.id}>',
                "https://cdn.discordapp.com/attachments/785174324264828958/785521976134598677/2020_12_06_0aw_Kleki.png",
                'sup bitch',
                'heyo',
                '*fuck am too nervous*',
                'OwO',
                'uwu',
                'shakie shakie',
                'welpwelpwelp',
                'lol',
                'you know, you\'re a waste of hair',
                'dont talk to me peasant',
                'st-step bro/sis/sibling-',
                'dont talk to me peasant',
                'umm',
                'flIpPiN moThEr DipIn',
                'bonk',
                'flippity dippity you fuckity lickity dickity shitity',
                'what?',
                'hello. <@!{ctx.author.id}>.',
                'no.',
                'ew',
                'schwepite innt mate',
                "https://tenor.com/view/strawberry-fraise-funny-twerk-twerking-gif-13568371",
    ]

    if message.content == "icy hey":
        response = random.choice(greets)
        await message.channel.send(response)
        await message.channel.send("icy hey")
    elif message.content == "raise-exception":
        raise discord.DiscordException

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise 'idk man'


    

client.run(TOKEN)# runs client for the bot token in TOKEN