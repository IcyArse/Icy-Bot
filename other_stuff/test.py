
import pytz
import datetime


time = datetime.datetime.now()
print(time)

utctime = time.astimezone(pytz.timezone('UTC'))
print(utctime)

timedelta = datetime.timedelta(seconds=10)
timebeta = datetime.timedelta(minutes=1)
print(f"interesting: {timebeta + timedelta}")
print(time + timedelta)

updated_time = (time + timedelta)


#while time.hour != updated_time.hour or time.minute != updated_time.minute or time.second != updated_time.second or time.day != updated_time.day:
#        now = datetime.datetime.now()
#
#        if now.hour == updated_time.hour and now.minute == updated_time.minute and now.second == updated_time.second and now.day == updated_time.day:
#                print("hello")
#                break

time_of_message = time
time_reminder = updated_time

while time_of_message.hour != time_reminder.hour or time_of_message.minute != time_reminder.minute or time_of_message.second != time_reminder.second or time_of_message.day != time_reminder.day:
        now = datetime.datetime.now()

        if now.hour == time_reminder.hour and now.minute == time_reminder.minute and now.second == time_reminder.second and now.day == time_reminder.day:
                print("welpwelp")#await ctx.send(f"IT'S TIMEEEEEEE <@!{ctx.author.id}>")
                break


print("hello it's been 10 seconds")
print(datetime.datetime.now())

