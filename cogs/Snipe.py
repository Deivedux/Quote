import discord
import json
from discord.ext import commands

with open('configs/config.json') as json_data:
	response_json = json.load(json_data)

success_string = response_json['response_string']['success']
error_string = response_json['response_string']['error']
del response_json

snipes = {}

def snipe_embed(context_channel, message, user):
	if message.author not in message.guild.members or message.author.color == discord.Colour.default():
		embed = discord.Embed(description = message.content, timestamp = message.created_at)
	else:
		embed = discord.Embed(description = message.content, color = message.author.color, timestamp = message.created_at)
	embed.set_author(name = str(message.author), icon_url = message.author.avatar_url)
	if message.channel != context_channel:
		embed.set_footer(text = 'Snipped by ' + str(user) + ' | in channel: #' + message.channel.name)
	else:
		embed.set_footer(text = 'Snipped by ' + str(user))
	return embed

class Snipe:
	def __init__(self, bot):
		self.bot = bot

	async def on_guild_remove(self, guild):
		try:
			del snipes[guild.id]
		except KeyError:
			pass

	async def on_guild_channel_delete(self, channel):
		try:
			del snipes[channel.guild.id][channel.id]
		except KeyError:
			pass

	async def on_message_delete(self, message):
		if message.guild.me.permissions_in(message.channel).send_messages:
			try:
				snipes[message.guild.id][message.channel.id] = message
			except KeyError:
				snipes[message.guild.id] = {message.channel.id: message}

	@commands.command()
	async def snipe(self, ctx, channel: discord.TextChannel = None):
		if not channel:
			channel = ctx.channel

		if not ctx.author.guild_permissions.manage_messages or not ctx.author.permissions_in(channel).read_messages:
			return

		try:
			sniped_message = snipes[ctx.guild.id][channel.id]
		except KeyError:
			return await ctx.send(content = error_string + ' **No available messages.**')

		await ctx.send(embed = snipe_embed(ctx.channel, sniped_message, ctx.author))


def setup(bot):
	bot.add_cog(Snipe(bot))
