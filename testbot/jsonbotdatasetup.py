import json

botdata = {}


#with open('testbotdata.json', 'w') as jsonfile:
#        json.dump(botdata, jsonfile)
#
with open('testbotdata.json', 'r+') as jsonfile:
        loaddata = json.load(jsonfile)

        
        #loaddata["guilddata"] = {}
        
        loaddata["guilddata"].remove(1)

#with open('testbotdata.json', 'r+') as jsonfile:
#        loaddata = json.load(jsonfile)
#
#        loaddata.guild_data.update({"setuptest": True})