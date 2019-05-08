import discord
import json
from discord.ext import commands
from cogs.Main import server_config

with open('configs/config.json') as json_data:
	response_json = json.load(json_data)
	success_string = response_json['response_string']['success']
	error_string = response_json['response_string']['error']
	del response_json

snipes = dict()

def snipe_embed(context_channel, message, user):
	if message.author not in message.guild.members or message.author.color == discord.Colour.default():
		embed = discord.Embed(description = message.content, timestamp = message.created_at)
	else:
		embed = discord.Embed(description = message.content, color = message.author.color, timestamp = message.created_at)
	embed.set_author(name = str(message.author), icon_url = message.author.avatar_url)
	if message.attachments:
		embed.add_field(name = 'Attachment(s)', value = '\n'.join([attachment.filename for attachment in message.attachments]) + '\n\n__Attachment URLs are invalidated once the message is deleted.__')
	if message.channel != context_channel:
		embed.set_footer(text = 'Sniped by: ' + str(user) + ' | in channel: #' + message.channel.name)
	else:
		embed.set_footer(text = 'Sniped by: ' + str(user))
	return embed

class Snipe(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		try:
			del snipes[guild.id]
		except KeyError:
			pass

	@commands.Cog.listener()
	async def on_guild_channel_delete(self, channel):
		try:
			del snipes[channel.guild.id][channel.id]
		except KeyError:
			pass

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		if message.guild and not message.author.bot:
			try:
				snipes[message.guild.id][message.channel.id] = message
			except KeyError:
				snipes[message.guild.id] = {message.channel.id: message}

	@commands.command()
	async def snipe(self, ctx, channel: discord.TextChannel = None):
		if not channel:
			channel = ctx.channel

		if not ctx.author.guild_permissions.manage_messages or not ctx.author.permissions_in(channel).read_messages or not ctx.author.permissions_in(channel).read_message_history:
			return

		if server_config[ctx.guild.id]['del_commands'] and ctx.guild.me.permissions_in(ctx.channel).manage_messages:
			await ctx.message.delete()

		try:
			sniped_message = snipes[ctx.guild.id][channel.id]
		except KeyError:
			await ctx.send(content = error_string + ' **No available messages.**')
		else:
			await ctx.send(embed = snipe_embed(ctx.channel, sniped_message, ctx.author))


def setup(bot):
	bot.add_cog(Snipe(bot))
