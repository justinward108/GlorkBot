import interactions
from datetime import datetime
import config

class info(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="info",
        description="General bot info",
    )
    async def ext_command(self, ctx: interactions.CommandContext):
        reply = "Current server time- "+str(datetime.utcnow())+" UTC\nConnection speed- "+str(round(config.bot.latency))+ " ms\nBot created by ^ReBeLLi0n^D#2343. Notify me if you find something broken I may or may not fix it lol"
        await ctx.send(reply)
def setup(client):
    info(client)