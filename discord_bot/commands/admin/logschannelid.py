import discord 
import json 
from discord_bot.discordlogs import error 
from discord_bot.embeds.embeds import send_embed
from discord_bot.config import get_bot_config
from discord_bot.discordlogs.discord_log import discord_log

async def logschannelid(client, message, args):
    """
    Discord command to configure the id of the channel for admin logs
    """
    if len(args) != 1: # The channel ID is missing
        return await error(
            message.channel,
            "Invalid argument(s) number. Use:\n"
            "logchannel <channelid>")
    
    bot_config = get_bot_config()
    bot_config['logschannelid'] = args[0] # Add the channel ID to config dic
    with open('bot_config.json', 'w') as f:
        json.dump(bot_config, f, indent=4) # Write the new config with id added in json file
        
    await send_embed(
        message.channel,
        "📜Logs Channel ID",
        "Value has been edited: " + str(bot_config["logschannelid"]) ,
        discord.Color.green())
    
    return await discord_log(client, "📜Logs Channel ID", "Channel ID for logs edited by: " + message.author) 