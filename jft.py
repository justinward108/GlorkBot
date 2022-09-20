import discord
import requests
from bs4 import BeautifulSoup

intents = discord.Intents.default()
intents.message_content = True
url = 'https://www.jftna.org/jft/'
text = "```"

client = discord.Client(intents=intents)
r = requests.get(url)
s = BeautifulSoup(r.text, 'html.parser')
for tag in s.find_all('tr'):
	text += tag.text
	text += '\n' 
text += "```"
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        embed = discord.Embed(title='Just for Today Meditation', description=text)
        await message.channel.send(embed=embed)
        await message.channel.send(text)
        return


client.run('MTAxODQ2ODQ5MjI4ODIxNzA5OA.GgzRkY.qj4HYWll42cooIDKKPOpO8j1M9-9F07-cas15U')