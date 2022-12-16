from interactions import Option, OptionType, get, Channel, Message, Embed
from os import listdir
import config
from interactions.ext.tasks import IntervalTrigger, create_task
from datetime import datetime
from asyncio import sleep
from aiohttp import ClientSession
from bs4 import BeautifulSoup

client = config.bot
url = 'http://www.jftna.org/jft/'

for filename in listdir('./cogs'):
	if filename.endswith('.py'):
		client.load(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
#	current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S").split()
#	t1 = datetime.strptime(current_time[1], "%H:%M:%S")
#	t2 = datetime.strptime("10:00:00", "%H:%M:%S")
#	seconds = abs((t2-t1).total_seconds())
    print('------')

async def _my_task():
	async with ClientSession() as session:
		async with session.get(url) as response:
			try:
				r = await response.text()
			except UnicodeDecodeError:
				r = await response.text('ISO-8859-1')
			s = BeautifulSoup(r, 'html.parser')
			text = "```"
			for tag in s.find_all('tr'):
				text += tag.text
				text += '\n'
			text += "```"
			channel = await get(config.bot, Channel, object_id='770777229000572959')
			await channel.send(text)
	get_channel = await get(client, Channel, object_id=770816409197608993)
	post_channel = await get(client, Channel, object_id=1051887328324489317)
	while True:
		message = await get_channel.purge(amount=1)
		await sleep(1)
		if len(message) == 0:
			break
		message = message[0]
		embed=Embed(title='Black hole screams', description=message.content,color = 0xf00a0a)
		if message.attachments:
			attachments = message.attachments
			attachment_names = ''
			for i in range (0,len(attachments)):
				attachment_names += attachments[i].filename + '\n'
			embed.add_field(name='Attachments', value=attachment_names, inline=False)
		embed.set_author(name=message.author.username+'#'+message.author.discriminator,icon_url=message.author.avatar_url)
		embed.timestamp = message.timestamp
		embed.set_footer(text='Message ID: '+str(message.id))
		await post_channel.send(embeds=embed)

@client.event
async def on_start():
	current_time = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S").split()
	t1 = datetime.strptime(current_time[1], "%H:%M:%S")
	#t1 = datetime.strptime("10:00:00", "%H:%M:%S")
	t2 = datetime.strptime("10:00:00", "%H:%M:%S")
	seconds = t1-t2
	if seconds.total_seconds() >= 0.0:
		x = datetime.strptime("23:59:59", "%H:%M:%S")
		hrs = str(seconds.seconds // 3600)
		mins = str(seconds.seconds % 3600 // 60)
		secs = str(seconds.seconds % 60)
		t3 = datetime.strptime(hrs+":"+mins+":"+secs, "%H:%M:%S")
		seconds = x - t3
		seconds_left = int(seconds.total_seconds())
	if seconds.total_seconds() < 0.0:
		seconds_left = int(abs((t2-t1).total_seconds()))
	await sleep(seconds_left)
	await _my_task()
	task = create_task(IntervalTrigger(86400))(_my_task)
	task.start()

@client.command(
	name='load_ext',
    options = [
        Option(
            name="package",
            description="What you want to say",
            type=OptionType.STRING,
            required=True,
        ),
    ],
)
async def load(ctx, package: str):
	client.load(f'cogs.{package}')
	await ctx.send('Extension loaded')

@client.command(
	name='unload_ext',
    options = [
        Option(
            name="package",
            description="What you want to say",
            type=OptionType.STRING,
            required=True,
        ),
    ],
)
async def unload(ctx, package: str):
	client.remove(f'cogs.{package}')
	await ctx.send("Extension unloaded")

@client.command(
    name="stop_fish",
    description="close the bot",
)
async def stop_fish(ctx):
    await ctx.send("closing")
    await client._stop()
	
client.start()