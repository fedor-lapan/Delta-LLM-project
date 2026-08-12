import discord                          # import requered library's for the discord bot
import os                               # for key browse
import time                             # for 429 handling
from dotenv import load_dotenv          # for key browse
from LLM import invoke_agent            # imports the main agent core
load_dotenv()                           # loads .env file data
TOKEN = os.getenv("DISCORD_TOKEN")      # saves discord token as TOKEN
import sys                              # for system exit
import random                           # made for smiley choise
import asyncio                          # for asyncronised functions
intents = discord.Intents.default()    
intents.message_content = True
client = discord.Client(intents=intents)
# discord bot settings


@client.event                           # defines a async function which will be called when the bot is logged in
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

    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return

    # Only respond when the bot is mentioned
    if client.user not in message.mentions:
        return
    reaction = ["👍", "❤️", "😂", "😄", "🔥", "💯", "👏", "🎉", "🥳", "⭐", "🚀"]   # the smileys the bot cann reply with to your messadge
    await message.add_reaction(random.choice(reaction)) # chosing them 
    print("Input received") # debug logg

    user_id = str(message.author.id)

    # Run the synchronous LLM call outside Discord's event loop
    thread_id = f"{user_id}:{message.guild.id}"
    async with message.channel.typing():
        response = await asyncio.to_thread(
            invoke_agent,
            message.content,
            thread_id
        )

    # Retry the LLM call if it returned False
    while calls != 0:
        if response is not False:
            break

        calls -= 1

        if calls == 0:
            break       # stops after 3 tries

        await asyncio.sleep(30)

        async with message.channel.typing():
            response = await asyncio.to_thread(
            invoke_agent,
            message.content,
            thread_id
    )

    # Retry sending the Discord message if Discord returns an HTTP error
    calls = 3

    try:# test if the response didnt crash
        if response is not False:
            await message.channel.send(response)
        else:
            await message.channel.send("sorry, something went wrong")

    except discord.HTTPException:
        while calls != 0:
            await asyncio.sleep(30)
            calls -= 1
            
            # repeats 3 times, if it doesnt help it returns an print log
            if calls == 0:
                print(f"Failed to send message to {message.channel.id} after 3 retries")
                return 

            try:
                await message.channel.send(response)
                break

            except discord.HTTPException:
                pass

    print("working")


client.run(TOKEN)
