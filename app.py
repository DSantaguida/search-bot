import os
import discord
import requests
import json
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("-search"):
        request = message.content.split(" ")
        search = ""
        max = 3
        for entry in request:
            if "-search" not in entry and "-c" not in entry:
                search += entry + "%20"
            if "-c" in entry:
                max = int(request[1][-1])

        r = requests.get("https://customsearch.googleapis.com/customsearch/v1?cx=" + os.getenv('SEARCH_ENGINE_ID') + "&q=" + search[:-3] + "&key=" + os.getenv('SEARCH_KEY'))

        result_dict = json.loads(r.text)

        result = ""
        i = 0
        for item in result_dict['items']:
            result += str(i + 1) + ". " + item['link'] + "\n"
            i+=1
            if (i==max):
                break

        await message.channel.send("Search Results:\n" + result)



client.run(TOKEN)