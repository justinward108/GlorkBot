import interactions
import config
import json
from datetime import datetime

#todo: logic to save multiple guilds in json file. Only 1 server rn


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
		dictionary={'channel_id':str(channel.id)}
		with open ('channels.json','w') as outfile:
			json.dump(dictionary, outfile)
		await ctx.send("logged")

	@interactions.extension_listener	
	async def on_message_delete(self, message: interactions.Message):
		with open('channels.json','r') as openfile:
			channel_id = json.load(openfile)
		if not channel_id:
			return
		channel = await interactions.get(config.bot, interactions.Channel, object_id=channel_id['channel_id'])
		deleted_message_channel = await interactions.get(config.bot, interactions.Channel, object_id=str(message.channel_id))
		embed=interactions.Embed(title='Message sent by '+message.author.mention+ ' deleted in '+deleted_message_channel.mention, description=message.content, color = 0xf00a0a)
		embed.set_author(name=str(message.author),icon_url=message.author.avatar_url)
		embed.timestamp = datetime.utcnow()
		embed.set_footer(text='Message ID: '+str(message.id))
		await channel.send(embeds=embed)

	@interactions.extension_listener
	async def on_message_update(self, before, after):
		with open ('channels.json','r') as openfile:
			channel_id = json.load(openfile)
			if not channel_id:
				return
		channel = await interactions.get(config.bot, interactions.Channel, object_id='851128747746918480')
		edited_message_channel = await interactions.get(config.bot, interactions.Channel, object_id = str(before.channel_id))
		embed=interactions.Embed(title='Message sent by '+before.author.mention+ ' edited in '+edited_message_channel.mention, color = 0x0a66f0)
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
