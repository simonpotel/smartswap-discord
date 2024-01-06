from ..misc.config import *
from ..misc.logs import *
import json 

async def logschannelid(client, message, args):
    if len(args) != 1: # The channel ID is missing
        return await error(
            message.channel,
            "Invalid argument(s) number. Use:\n"
            "logchannel <channelid>")
    bot_config = get_bot_config()
    bot_config['logschannelid'] = args[0] # Add the channel ID to config dic
    with open('bot_config.json', 'w') as f:
        json.dump(bot_config, f, indent=4) # Write the new config with id added in json file
    return await send_embed(
        message.channel,
        "📜Logs Channel ID",
        "Value has been edited: " + str(bot_config["logschannelid"]) ,
        discord.Color.green())
        