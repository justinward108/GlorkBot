import interactions
import config
import json
from datetime import datetime



class logging(interactions.Extension):
	def __init__(self,client: interactions.Client):
		self.client: interactions.Client = client
	@interactions.extension_command(
		name='msg_logging',
		description='set and enable message logging channel',
		options=[
			interactions.Option(
				name='channel',
				description='select channel to log',
				type=interactions.OptionType.CHANNEL,
				required=True,
			),
		],
	)
	async def ext_command(self, ctx: interactions.CommandContext, channel: str):
		with open ('channels.json','r') as file:
			data = json.load(file)
		data[str(ctx.guild_id)]=str(channel.id)
		with open ('channels.json','w') as outfile:
			json.dump(data, outfile)
		await ctx.send("logged")

	@interactions.extension_command(
		name='msg_logging_disable',
		description='disable message logging',
	)
	async def ext_command1(self, ctx: interactions.CommandContext):
		with open('channels.json','r') as file:
			data = json.load(file)
			if ctx.guild_id not in data.keys():
				await ctx.send("Logging was not enabled")
				return
			removed_value = data.pop(ctx.guild_id)
		with open('channels.json','w') as file:
			json.dump(data, file)	
		await ctx.send("Logging disabled")

	@interactions.extension_listener	
	async def on_message_delete(self, message: interactions.Message):
		if str(message.author.id) == '1018468492288217098':
			return
		with open('channels.json','r') as openfile:
			channel_id = json.load(openfile)
		if str(message.guild_id) not in channel_id.keys():
			return
		channel = await interactions.get(config.bot, interactions.Channel, object_id=channel_id[str(message.guild_id)])
		deleted_message_channel = await interactions.get(config.bot, interactions.Channel, object_id=str(message.channel_id))
		embed=interactions.Embed(title='Message deleted in '+'#'+str(deleted_message_channel), description=message.content, color = 0xf00a0a)
		embed.set_author(name=str(message.author)+'#'+str(message.author.discriminator),icon_url=message.author.avatar_url)
		embed.timestamp = datetime.utcnow()
		embed.set_footer(text='Message ID: '+str(message.id))
		await channel.send(embeds=embed)

	@interactions.extension_listener
	async def on_message_update(self, before, after):
		if str(before.author.id) == '1018468492288217098':
			return
		with open ('channels.json','r') as openfile:
			channel_id = json.load(openfile)
			if str(before.guild_id) not in channel_id.keys():
				return
		channel = await interactions.get(config.bot, interactions.Channel, object_id=channel_id[str(before.guild_id)])
		edited_message_channel = await interactions.get(config.bot, interactions.Channel, object_id = str(before.channel_id))
		embed=interactions.Embed(title='Message sent by '+str(before.author)+'#'+str(before.author.discriminator)+' edited in '+'#'+str(edited_message_channel), color = 0x0a66f0)
		if before == None:
			embed.add_field(name='Before:', value="Old meessage cant be fetched", inline=False)
		else:
			embed.add_field(name='Before:', value=before.content, inline=False)
		embed.add_field(name="After:", value=after.content, inline=False)
		embed.timestamp = datetime.utcnow()
		embed.set_footer(text='\u200b')
		await channel.send(embeds=embed)


def setup(client):
	logging(client)
