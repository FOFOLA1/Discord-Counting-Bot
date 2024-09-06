from dotenv import load_dotenv, set_key
from discord import Intents, Client
import inspect
import os
from discord.ext import commands

load_dotenv()
TOKEN = str(os.getenv("TOKEN"))
CHANNEL_ID = str(os.getenv("CHANNEL_ID"))
last_user_id = str(os.getenv("LAST_USER_ID"))
last_num = int(os.getenv("COUNT"))

class MyClient(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        

    async def on_message(self, message):
        global last_num, last_user_id
        print(f'Message from {message.author} in {message.channel}: {message.content}')
        if str(message.channel.id) == CHANNEL_ID and str(message.author.id) != str(self.user.id):
            if str(message.author.id) == last_user_id:
                await message.channel.send(f"{message.author.mention} dej prostor taky ostatním!")
                await message.delete()
            else:
                msg = message.content
                try:
                    num = int(msg, 16)
                except ValueError:
                    num = -1
                if num == last_num+1:
                    await message.add_reaction("\U0001F44D")
                    last_num += 1
                    last_user_id = str(message.author.id)
                    set_key(".env", "LAST_USER_ID", last_user_id)
                    set_key(".env", "COUNT", str(last_num))
                else: 
                    await message.channel.send(f"Ajéje, {message.author.mention} to pokazil! Poslední bylo **{hex(last_num).split('x')[-1]}**, zvaž svoji odpověď.")
                    await message.delete()
    
    async def on_ready():
        print(inspect.cleandoc(f"""
            Logged in as {client.user} (ID: {client.user.id})

            Use this URL to invite {client.user} to your server:
            https://discord.com/api/oauth2/authorize?client_id={client.user.id}&scope=applications.commands%20bot
        """), end="\n")
        
    
    
        
        
        
            
intents = Intents.default()
intents.message_content = True

client = MyClient(intents=intents, command_prefix="/")




client.run(TOKEN)