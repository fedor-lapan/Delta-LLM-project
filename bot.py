import discord                          # import requered library's for the discord bot
import os                               # for key browse
import time                             # for 429 handling
from dotenv import load_dotenv          # for key browse
from LLM import invoke_agent            # imports the main agent core
load_dotenv()                           # loads .env file data
TOKEN = os.getenv("DISCORD_TOKEN")      # saves discord token as TOKEN
import sys                              # for system excit
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
# discord bot settings

@client.event
async def on_ready():
    """
    Log in proces, starts the log in and tells if the LLM is ready to go 
    """
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    calls = 3
    """
    Main command, answers every question and replies every time
    """
    if message.author == client.user:
        return None # checks if the message was sent by himself
    print("Input recived")
    user_id = str(message.author.id) # saves the user id , basicly who wrote that

    response = invoke_agent(
        message.content,
        user_id
    )
    while calls != 0:
        if response is False:
            calls -= 1
        else:
            break 
        time.sleep(30)
        response = invoke_agent(
            message.content,
            user_id
        )
    calls = 3
    
    try:
        await message.channel.send(response)
    except discord.HTTPException as e:
        while calls != 0:
            time.sleep(30)
            calls -= 1
            if calls == 0:
                sys.exit()
            try:
                await message.channel.send(response)
            except:
                pass
    print("working")


client.run(TOKEN)
