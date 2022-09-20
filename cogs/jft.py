import interactions
import requests
from bs4 import BeautifulSoup

url = 'https://www.jftna.org/jft/'

class jft(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="jft",
        description="For daily readings",
    )
    async def ext_command(self, ctx: interactions.CommandContext):
        r = requests.get(url)
        s = BeautifulSoup(r.text, 'html.parser')
        text = "```"
        for tag in s.find_all('tr'):
        	text += tag.text
        	text += '\n'
        text += "```"
        await ctx.send(text)

def setup(client):
    jft(client)