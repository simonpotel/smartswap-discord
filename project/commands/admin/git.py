import discord
from ...misc.logs import *
from discord import Activity, ActivityType
import subprocess

async def process_submodule_result(message_channel, submodule_result):
    command_status_embed = discord.Embed(title="subprocess command ✅" if submodule_result.returncode == 0 else "subprocess command ❌", 
                                         color=discord.Color.green() if submodule_result.returncode == 0 else discord.Color.red())
    command_status_embed.add_field(name="Command", value=" ".join(submodule_result.args), inline=True)
    command_status_embed.add_field(name="Return Code", value=submodule_result.returncode, inline=True)
    
    if submodule_result.stdout:
        command_status_embed.add_field(name="Standard Output", value=submodule_result.stdout, inline=False)
    
    if submodule_result.stderr:
        command_status_embed.add_field(name="Standard Error", value=submodule_result.stderr, inline=False)

    await message_channel.send(embed=command_status_embed)


async def git(client, message, args):
    usage = """Invalid argument(s) number. Use:
    git projects
    git update <project_name>
    """
    config = get_json_content("update_config.json")
    if config == -1:
        write_json("update_config.json", {"projectname":"c://dir"})
        await error(message.channel, "update_config.json has been created.")
        return 

    if len(args) < 1:
        return await error(message.channel, usage)
    
    if args[0] == "projects":
        embed = discord.Embed(title="Projects", color=discord.Color.pink())
        for project, path in config.items():
            embed.add_field(name=project, value=path, inline=False)
        await message.channel.send(embed=embed)
        return
    
    if args[0] == "update":
        if len(args) != 2:
            return await error(message.channel, "Invalid argument. Use `git update <project>`")
        
        project_name = args[1]
        if project_name not in config:
            return await error(message.channel, f"Project '{project_name}' is not configured.")
        
        project_path = config[project_name]
        try:
            # Git pull the main project
            pull_result = subprocess.run(['git', '-C', project_path, 'pull'], capture_output=True, text=True)

            await process_submodule_result(message.channel, pull_result)


            # Git submodule update --remote
            submodule_result = subprocess.run(['git', '-C', project_path, 'submodule', 'update', '--remote'], capture_output=True, text=True)

            await process_submodule_result(message.channel, submodule_result)


        except Exception as e:
            await error(message.channel, f"An unexpected error occurred: {e}")

        return
    
    await error(message.channel, "Invalid argument. Use `git <project>` or `git update`")