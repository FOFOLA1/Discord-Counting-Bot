
from discord import Intents,  Interaction, channel, Status, app_commands
import inspect
from discord.ext import commands
from json import load, dump, JSONDecodeError
import datetime
import requests

try:
    with open('.json', 'r') as file:
        data = load(file)
except (FileNotFoundError, JSONDecodeError):
    while True:
        inp = input("Please enter your bot token:\n> ")
        
        try:
            data = requests.get("https://discord.com/api/v10/users/@me", headers={
                "Authorization": f"Bot {inp}"
            }).json()
        except requests.exceptions.RequestException as e:
            if e.__class__ == requests.exceptions.ConnectionError:
                exit(f"ConnectionError: Discord is commonly blocked on public networks, please make sure discord.com is reachable!")

            elif e.__class__ == requests.exceptions.Timeout:
                exit(f"Timeout: Connection to Discord's API has timed out (possibly being rate limited?)")

            exit(f"Unknown error has occurred! Additional info:\n{e}")
        if data.get("id", None):
            break
        print("Invalid token, please try again.")
        
    data = {
        "token": inp,
        "channels": []
    }
    with open('.json', 'w') as file:
        dump(data, file)
    

TOKEN = data["token"]


intents = Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

def is_owner(interaction: Interaction):

    print(interaction.user.id)
    print(interaction.guild.owner_id)
    return interaction.user.id == interaction.guild.owner_id


def is_bot_owner(interaction: Interaction):
    return interaction.user.id == 709818829965885491

def save_data(data):
    with open('.json', 'w') as file:
        dump(data, file)



@bot.tree.command(name="setup",description="Setup counting bot")
@app_commands.check(is_owner)
@app_commands.describe(channel='Choose the channel for counting', style='Styles of counting: Hexadecimal: `hex`, Decimal: `dec`, Binary: `bin`')
async def setup_command(interaction:Interaction, channel: channel.TextChannel, style: str = "dec"):
    style = style.lower()
    if style not in ["hex", "dec", "bin"]:
        await interaction.response.send_message("Invalid type! Valid types are:\n\tBinary: `bin`\n\tDecimal: `dec`\n\tHexadecimal: `hex`.", ephemeral=True)
        return
    if channel.id in (data['channels'][_]["id"] for _ in range(len(data['channels']))):
        await interaction.response.send_message("Bot is already set in this channel.", ephemeral=True)
        return
        
    await channel.send("0")
    
    new_channel = {
        "id": channel.id,
        "last_user": bot.user.id,
        "count": 0,
        "type": style
    }
    data['channels'].append(new_channel)
    save_data(data)

    await interaction.response.send_message(f"Bot has been successfully set in {channel.jump_url}", ephemeral=True)  
'''@setup_command.error
async def setup_command_error(interaction: Interaction, error):
    await interaction.response.send_message(f"You must be an owner to do that!", ephemeral=True)'''
    
    
@bot.tree.command(name="shutdown", description="Shutdown the bot (for bot owner only)")
@app_commands.check(is_bot_owner)
async def shutdown_command(interaction: Interaction):
    await interaction.response.send_message("Shutting down the bot...", ephemeral=True)
    await bot.change_presence(status=Status.offline)
    await bot.close()
@shutdown_command.error
async def shutdown_command_error(interaction: Interaction, error):
    await interaction.response.send_message("You must be a bot owner to do that!", ephemeral=True)

    
@bot.tree.command(name="reset_count", description="Reset the bot's count")
@app_commands.describe(channel='Choose the channel for resetting')
@app_commands.check(is_owner)
async def reset_command(interaction:Interaction, channel: channel.TextChannel):
    for index, channel_data in enumerate(data['channels']):
        if channel.id == channel_data["id"]:
            await channel.send("How about start counting again?\n\n0")
            data["channels"][index]["count"] = 0
            data["channels"][index]["last_user"] = bot.user.id
            save_data(data)
            await interaction.response.send_message("Successfully started from 0 again!", ephemeral=True)
            return

    await interaction.response.send_message("This channel is not registered!", ephemeral=True)
@reset_command.error
async def reset_command_error(interaction: Interaction, error):
    await interaction.response.send_message("You must be an owner to do that!", ephemeral=True)
    

@bot.tree.command(name="remove",description="Remove counting in the channel")
@app_commands.check(is_owner)
@app_commands.describe(channel='Choose the channel for removing counting')
async def remove_command(interaction: Interaction, channel: channel.TextChannel):
    for index, channel_data in enumerate(data['channels']):
        if channel.id == channel_data["id"]:
            await channel.send("Counting stopped in this channel.")
            del data["channels"][index]
            save_data(data)
            await interaction.response.send_message(f"Successfully closed counting in {channel.jump_url}!", ephemeral=True)
            return

    await interaction.response.send_message("This channel is not registered!", ephemeral=True)
@remove_command.error
async def remove_command_error(interaction: Interaction, error):
    await interaction.response.send_message("You must be an owner to do that!", ephemeral=True)
    
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(inspect.cleandoc(f"""
            Logged in as {bot.user} (ID: {bot.user.id})

            Use this URL to invite {bot.user} to your server:
            https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&scope=applications.commands%20bot
        """), end="\n")

@bot.event
async def on_message(message):
    print(f'\033[31m{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} \033[34mINFO    \033[0m{message.author} in {message.channel}: {message.content}')
    for index, channel_data in enumerate(data['channels']):
        if message.channel.id == channel_data["id"]:
            if message.author == bot.user:
                return
            
            if message.author.id == channel_data["last_user"]:
                await message.channel.send(f"Give a chance to others, {message.author.mention}!", delete_after=5)
                await message.delete()
                return
            
            msg = message.content
            if channel_data["type"] == "hex":
                try:
                    num = int(msg, 16)
                except ValueError:
                    num = -1
            elif channel_data["type"] == "dec":
                try:
                    num = int(msg)
                except ValueError:
                    num = -1
            elif channel_data["type"] == "bin":
                try:
                    num = int(msg, 2)
                except ValueError:
                    num = -1
                    
            if num == channel_data["count"]+1:
                await message.add_reaction("\U0001F44D")
                data["channels"][index]["count"] += 1
                data["channels"][index]["last_user"] = message.author.id
                save_data(data)
            else:
                await message.channel.send(f"Nice try, {message.author.mention}!", delete_after=5)
                await message.delete()
                    
                    
bot.run(TOKEN)



""" 
\033[0m
0: Reset
30: Black
31: Red
32: Green
33: Yellow
34: Blue
35: Magenta
36: Cyan
37: White 
"""