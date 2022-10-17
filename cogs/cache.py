from interactions import Extension,extension_command

class cache(Extension):
    def __init__(self, client):
        self.client = client

    @extension_command(
        name="cache",
    )
    async def ext_command(self, ctx):

        cache = self.client._http.cache
        y = ''
        for x, storage in cache.storages.items():
            y += x.__name__ +':'+str(len(storage.values))
            y += '\n'
        await ctx.send(y)
def setup(client):
    cache(client)