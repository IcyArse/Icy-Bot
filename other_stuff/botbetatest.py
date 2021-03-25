import os
import random
import discord

import pytz
import datetime

from dotenv import load_dotenv

from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(command_prefix="icy ", intents=intents)

@bot.event
async def on_ready():
        print(f'{bot.user.name} has connected to Discord!')
        guild = discord.utils.get(bot.guilds, name=GUILD)
        memberss = [member.name for member in guild.members]
        print(f'server members are: {memberss}')


@bot.command(name="remindin", help="reminds you in the given time [<hours>h <minutes>m <seconds>s]")
async def on_message(ctx, *args):
        time_of_message = ctx.message.created_at
        message_type = ctx.message.type

        delay = list(args)
        print(f"input = {delay}")

        reminder_message = ""
        reminder_message_true = ""
        reminder_message_dm = ""
        
        timedelta = datetime.timedelta()
        for i in delay:
                try :
                        stripped = int(i[:-1])

                        if "d" in i or "D" in i:

                                stripped = int(i[:-1])

                                timedays = datetime.timedelta(days=stripped)
                                await ctx.send(f"```> time delay of {stripped} days created```")
                                timedelta = timedelta + timedays
                                print(timedays)



                        elif "h" in i or "H" in i:

                                stripped = int(i[:-1])

                                timehours = datetime.timedelta(hours=stripped)
                                await ctx.send(f"```> time delay of {stripped} hours created```")
                                timedelta = timedelta + timehours
                                print(timehours)


                        elif "m" in i or "M" in i:

                                stripped = int(i[:-1])

                                timeminutes = datetime.timedelta(minutes=stripped)
                                await ctx.send(f"```> time delay of {stripped} minutes created```")
                                timedelta = timedelta + timeminutes
                                print(timeminutes)

                                
                                


                        elif "s" in i or "S" in i:

                                stripped = int(i[:-1])

                                timeseconds = datetime.timedelta(seconds=stripped)
                                await ctx.send(f"```> time delay of {stripped} seconds created```")
                                timedelta = timedelta + timeseconds
                                print(timeseconds)

                except :
                        reminder_message = i

                                


        if timedelta == datetime.timedelta():
                await ctx.send("If you want me to remind you add some time you numbnuts")
                return None


        time_reminder = time_of_message + timedelta

        print(f"message type = {message_type}")

        print(f"timedelta = {timedelta}")
        print(f"time of the message = {time_of_message}")
        print(f"time to be reminded at = {time_reminder}")

        print(f"reminder message = {reminder_message}")


        if reminder_message:
                reminder_message_true = f" about \"{reminder_message}\""
                reminder_message_dm = f", it's time for \"{reminder_message}\""


        await ctx.send(f"```> time right now: {time_of_message}```")
        await ctx.send(f"```> time to be reminded at {time_reminder}```")

        await ctx.send(f"icy thy remind you {ctx.author.name}, in {timedelta}{reminder_message_true}")



        while time_of_message.hour != time_reminder.hour or time_of_message.minute != time_reminder.minute or time_of_message.second != time_reminder.second or time_of_message.day != time_reminder.day:
                now = datetime.datetime.now().astimezone(pytz.timezone('UTC'))

                if now.hour == time_reminder.hour and now.minute == time_reminder.minute and now.second == time_reminder.second and now.day == time_reminder.day:
                        await ctx.author.create_dm()
                        await ctx.author.dm_channel.send(f"IT'S TIMEEEEEEE <@!{ctx.author.id}>{reminder_message_dm}")

                        await ctx.send("```> dm'ed the author the reminder```")

                        break


        await ctx.send("```> test complete```")

bot.run(TOKEN)
