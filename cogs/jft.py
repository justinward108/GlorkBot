import interactions
import aiohttp
import asyncio
from bs4 import BeautifulSoup

url = 'https://www.jftna.org/jft/'

class jft(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client

    def scrape(self, r):
        s = BeautifulSoup(r, 'html.parser')
        text = "```"
        for tag in s.find_all('tr'):
            text += tag.text
            text += '\n'
        text += "```"
        return text

    @interactions.extension_command(
        name="jft",
        description="For daily readings",
    )

    
    async def ext_command(self, ctx: interactions.CommandContext):
        loop = asyncio.get_running_loop()
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                try:
                    r = await response.text()
                except UnicodeDecodeError:
                    r = await response.text('ISO-8859-1')
                text = await loop.run_in_executor(None, self.scrape, r)
                await ctx.send(text)


def setup(client):
    jft(client)
