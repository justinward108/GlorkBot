import interactions
import os
import config
from interactions.ext.tasks import IntervalTrigger, create_task
from datetime import datetime
import asyncio
import requests
from bs4 import BeautifulSoup

client = config.bot
url = 'https://www.jftna.org/jft/'

for filename in os.listdir('./cogs'):
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
	r = requests.get(url)
	s = BeautifulSoup(r.text, 'html.parser')
	text = "```"
	for tag in s.find_all('tr'):
		text += tag.text
		text += '\n'
	text += "```"
	channel = await interactions.get(config.bot, interactions.Channel, object_id='770777229000572959')
	await channel.send(text)

@client.event
async def on_start():
	current_time = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S").split()
	t1 = datetime.strptime(current_time[1], "%H:%M:%S")
	#t1 = datetime.strptime("10:05:00", "%H:%M:%S")
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
	await asyncio.sleep(seconds_left)
	await _my_task()
	task = create_task(IntervalTrigger(86400))(_my_task)
	task.start()

client.start()
