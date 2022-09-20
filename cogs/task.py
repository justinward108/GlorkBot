from interactions import Extension
from interactions.ext.tasks import IntervalTrigger, create_task
import interactions
import config
import requests
from bs4 import BeautifulSoup

url = 'https://www.jftna.org/jft/'


class Cog(Extension):
	def __init__(self, client):
		self.method = create_task(IntervalTrigger(86400))(self.method)
		self.method.start()

	async def method(self):
		r = requests.get(url)
		s = BeautifulSoup(r.text, 'html.parser')
		text = "```"
		for tag in s.find_all('tr'):
			text += tag.text
			text += '\n'
		text += "```"
		channel = await interactions.get(config.bot, interactions.Channel, object_id='770777229000572959')
		await channel.send(text)
def setup(client):
	Cog(client)