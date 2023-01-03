from interactions import Embed, Member, Modal, TextInput, TextStyleType, Button, extension_command, extension_modal, extension_component, Extension, Option, OptionType, get, Channel, Message, LibraryException
from datetime import date


class report(Extension):
    def __init__(self, client):
        self.client = client


    @extension_command(name='report', description='Log a punk for strikes and bad behavior')
    async def send_button(self, ctx):
        button = Button(style=1, custom_id='button', label='click to open')
        await ctx.send("Click the button below to open popup for logging", components=button)

    @extension_component('button')
    async def button(self, ctx):
        modal = Modal(
            custom_id = "send",
            title = "log the punk",
            components = [
                TextInput(
                    style = TextStyleType.SHORT,
                    custom_id = "name",
                    label = "Punk's name",
                    min_length = 1,
                    max_length = 20,
                    required = True,
                ),
                TextInput(
                    style = TextStyleType.SHORT,
                    custom_id = "discord-id",
                    label = "Punk's discord-id",
                    placeholder = 'Make sure the id is correct!',
                    required = True,
                ),
                TextInput(
                    style = TextStyleType.PARAGRAPH,
                    custom_id = 'description',
                    label = "Punk's description",
                    min_length = 1,
                    max_length = 1000,
                    required = True,
                ),
            ],
        )
        await ctx.popup(modal)
        message = await get(self.client,Message,object_id=ctx.message.id)
        button = ctx.message.components[0].components[0]
        button.disabled = True
        await message.edit("Click the button below to open popup for logging", components=ctx.message.components)
        

    @extension_modal("send")
    async def modal(self, ctx, name: str, disc_id: str, info: str):
        channel = await get(self.client, Channel, object_id=1048094275482693662)
        embed = Embed(color = 0x0a66f0)
        embed.add_field(name='Name', value=name, inline=True)
        embed.add_field(name='Discord-id', value=disc_id, inline=True)
        embed.add_field(name='Description', value=info, inline=False)
        embed.set_author(name=ctx.author.username+'#'+ctx.author.discriminator,icon_url=ctx.author.avatar_url)
        try:            
            punk = await get(self.client, Member, object_id=disc_id, parent_id=770770772460568587)
        except LibraryException as e:
            if e.message == 'Unknown User' or e.message == 'Unknown Member':
                await channel.send(embeds=embed)
                await ctx.send(f"""
{name}
{disc_id}
{info}
""")
                return
            else:
                await ctx.send("Failed")
                return
        else:
            embed.set_thumbnail(url=punk.avatar_url)
            await channel.send(embeds=embed)
            await ctx.send(f"""
{name}
{disc_id}
{info}
""")


def setup(client):
    report(client)
