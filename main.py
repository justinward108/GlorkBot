import interactions
import os
import config

client = config.bot

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    print('------')

client.start()