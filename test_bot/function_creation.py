
def welcome_show(member):

        global welcome_channel
        global welcome_title
        global custom_welcome_message
        global send_welcome_gif
        global custom_welcome_gif
        global send_welcome_message
        global welcome_member_count_show
        global send_welcome_emote
        global custom_welcome_thumbnail
        global send_welcome_thumbnail
        global dataindexdict

        serverid = str(member.guild.id)

        if True:                

                welcome_channel           = getjson(serverid, welcome_channel, "welcome_channel")
                welcome_title             = getjson(serverid, welcome_title, "welcome_title")
                custom_welcome_message    = getjson(serverid, custom_welcome_message, "custom_welcome_message")
                send_welcome_gif          = getjson(serverid, send_welcome_gif, "send_welcome_gif")
                custom_welcome_gif        = getjson(serverid, custom_welcome_gif, "custom_welcome_gif")
                send_welcome_message      = getjson(serverid, send_welcome_message, "send_welcome_message")
                welcome_member_count_show = getjson(serverid, welcome_member_count_show, "welcome_member_count_show")
                send_welcome_emote        = getjson(serverid, send_welcome_emote, "send_welcome_emote")
                custom_welcome_thumbnail  = getjson(serverid, custom_welcome_thumbnail, "custom_welcome_thumbnail")
                send_welcome_thumbnail    = getjson(serverid, send_welcome_thumbnail, "send_welcome_thumbnail")

                dataindexdict = None

        server = member.guild
        member_number = len(server.members)# gets the number of members in the server

        if welcome_title:
                title = welcome_title

        if not send_welcome_message:
                # if the welcome message is turned off by the admin
                welcome_message_text = None
        else:
                if custom_welcome_message:
                        welcome_message_text = custom_welcome_message
                else:
                        welcome_message_text = dedent(f"""**Welcome {member}**
                        WELCOMEEEE to {server.name}, glad to have you here and hope you enjoy your stay
                        **server now has {member_number} members!!!**
                        (>̃ ㅅ<̃)
                        """)

        welcome_gifs = (
                "https://media1.tenor.com/images/6830c5f9430da0b5bd9f3e55f66a4fca/tenor.gif?itemid=19063102",
                "https://media1.tenor.com/images/08c2c8535404c39f2fb3cb5de85c97d7/tenor.gif?itemid=16281444",
                "https://media1.tenor.com/images/c5fad21f9828d19044a58f8b84a6e14b/tenor.gif?itemid=6013419",
                "https://media1.tenor.com/images/5210b05939cdafd508346f8e714c1595/tenor.gif?itemid=17715386",
        )

        title = f"WELCOME TO {server.name}"# the main title for welcome message

        embeded = discord.Embed(title=title, description=welcome_message_text, color=0x8871bf)# sets the title

        if send_welcome_thumbnail:
                if custom_welcome_thumbnail:
                        thumbnail = custom_welcome_thumbnail
                else:
                        thumbnail = member.avatar_url# gets the user avatar
                embeded.set_thumbnail(url=thumbnail)# sets the thumbnail(shows the user avatar or the custom thumbnail in the side)

        if send_welcome_gif:
                if custom_welcome_gif:
                        welcome_gif = custom_welcome_gif
                else:
                        welcome_gif = random.choice(welcome_gifs)
                embeded.set_image(url=welcome_gif)# sets the gif as the main image in embed

        return embeded

def heatup():
        heat_up_message = "Please make sure that the input is either \"True\" or \"False\""
        embeded = discord.Embed(title="Icy's heating up..", description=heat_up_message, color=0x5fb79d)
        
        return embeded