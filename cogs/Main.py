import discord
import datetime
import asyncio
import sqlite3
import json
from discord.ext import commands
from cogs.OwnerOnly import blacklist_ids

conn = sqlite3.connect('configs/QuoteBot.db')
c = conn.cursor()

server_config_raw = c.execute("SELECT * FROM ServerConfig").fetchall()
prefixes = {}
del_commands = []
on_reaction = []
for i in server_config_raw:
	if i[1] != None:
		prefixes[int(i[0])] = str(i[1])
	if i[2] != None:
		del_commands.append(int(i[0]))
	if i[3] != None:
		on_reaction.append(int(i[0]))
del server_config_raw

with open('configs/config.json') as json_data:
	response_json = json.load(json_data)
	default_prefix = response_json['default_prefix']
	success_string = response_json['response_string']['success']
	error_string = response_json['response_string']['error']
	del response_json

def quote_embed(context_channel, message, user):
	if message.author not in message.guild.members or message.author.color == discord.Colour.default():
		embed = discord.Embed(description = message.content, timestamp = message.created_at)
	else:
		embed = discord.Embed(description = message.content, color = message.author.color, timestamp = message.created_at)
	embed.set_author(name = str(message.author), icon_url = message.author.avatar_url, url = 'https://discordapp.com/channels/' + str(message.guild.id) + '/' + str(message.channel.id) + '/' + str(message.id))
	if message.attachments:
		if len(message.attachments) == 1 and message.attachments[0].url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.gifv', '.webp', '.bmp')):
			embed.set_image(url = message.attachments[0].url)
		else:
			attachment_count = 0
			for attachment in message.attachments:
				attachment_count+=1
				embed.add_field(name = 'Attachment ' + str(attachment_count), value = '[' + attachment.filename + '](' + attachment.url + ')', inline = False)
	if message.channel != context_channel:
		embed.set_footer(text = 'Quoted by: ' + str(user) + ' | in channel: #' + message.channel.name)
	else:
		embed.set_footer(text = 'Quoted by: ' + str(user))
	return embed

class Main:
	def __init__(self, bot):
		self.bot = bot

	async def on_ready(self):
		c.execute("DELETE FROM ServerConfig WHERE Guild NOT IN (" + ', '.join([str(guild.id) for guild in self.bot.guilds]) + ")")
		conn.commit()

	async def on_guild_remove(self, guild):
		c.execute("DELETE FROM ServerConfig WHERE Guild = " + str(guild.id))
		conn.commit()

	async def on_raw_reaction_add(self, payload):
		if str(payload.emoji) == '💬' and payload.user_id not in blacklist_ids and not self.bot.get_guild(payload.guild_id).get_member(payload.user_id).bot and payload.guild_id in on_reaction:
			guild = self.bot.get_guild(payload.guild_id)
			channel = guild.get_channel(payload.channel_id)
			user = guild.get_member(payload.user_id)

			try:
				message = await channel.get_message(payload.message_id)
			except discord.NotFound:
				return
			except discord.Forbidden:
				return
			else:
				await channel.send(embed = quote_embed(channel, message, user))

	@commands.command(aliases = ['q'])
	async def quote(self, ctx, msg_id: int = None, *, reply = None):
		if not msg_id:
			return await ctx.send(content = error_string + ' **Please specify a message ID to quote.**')

		if ctx.guild.id in del_commands and ctx.guild.me.permissions_in(ctx.channel).manage_messages:
			await ctx.message.delete()

		try:
			message = await ctx.channel.get_message(msg_id)
		except discord.NotFound:
			await ctx.send(content = error_string + ' **Could not find the specified message.**')
		except discord.Forbidden:
			await ctx.send(content = error_string + ' **I do not have enough permissions to get the message.**')
		else:
			await ctx.send(embed = quote_embed(ctx.channel, message, ctx.author))
			if reply:
				await ctx.send(content = '**' + ctx.author.display_name + '\'s reply:**\n' + reply)

	@commands.command(aliases = ['quotechan', 'qchan', 'qc'])
	async def quotechannel(self, ctx, channel: discord.TextChannel, msg_id: int = None, *, reply = None):
		if not msg_id:
			return await ctx.send(content = error_string + ' **Please specify a message ID to quote, and if you did, make sure that the first argument is a channel to quote the message from.**')

		if ctx.guild.id in del_commands and ctx.guild.me.permissions_in(ctx.channel).manage_messages:
			await ctx.message.delete()

		try:
			message = await channel.get_message(msg_id)
		except discord.NotFound:
			await ctx.send(content = error_string + ' **Could not find the specified message.**')
		except discord.Forbidden:
			await ctx.send(content = error_string + ' **I do not have enough permissions to get the message.**')
		else:
			await ctx.send(embed = quote_embed(ctx.channel, message, ctx.author))
			if reply:
				await ctx.send(content = '**' + ctx.author.display_name + '\'s reply:**\n' + reply)

	@commands.command()
	async def prefix(self, ctx, *, prefix = None):
		if not ctx.guild:
			return

		if not prefix:

			try:
				guild_prefix = prefixes[ctx.guild.id]
			except KeyError:
				guild_prefix = default_prefix

			await ctx.send(content = '**My prefix here is** `' + guild_prefix + '`')

		else:

			if not ctx.author.guild_permissions.administrator:
				return

			if len(prefix) > 5 or '\n' in prefix:
				return await ctx.send(content = error_string + ' **Invalid prefix format. Make sure of the following:\n• Prefix is not over 5 characters long.\n• Prefix does not contain new lines.**')

			try:
				c.execute("INSERT INTO ServerConfig (Guild, Prefix) VALUES (" + str(ctx.guild.id) + ", '" + str(prefix).replace('\'', '\'\'') + "')")
				conn.commit()
			except sqlite3.IntegrityError:
				c.execute("UPDATE ServerConfig SET Prefix = '" + str(prefix).replace('\'', '\'\'') + "' WHERE Guild = " + str(ctx.guild.id))
				conn.commit()
			prefixes[ctx.guild.id] = prefix

			await ctx.send(content = success_string + ' **Prefix changed to** `' + prefix + '`')

	@commands.command(aliases = ['delcmds'])
	async def delcommands(self, ctx):
		if not ctx.guild or not ctx.author.guild_permissions.manage_guild:
			return

		if ctx.guild.id not in del_commands:

			try:
				c.execute("INSERT INTO ServerConfig (Guild, DelCommands) VALUES (" + str(ctx.guild.id) + ", '1')")
				conn.commit()
			except sqlite3.IntegrityError:
				c.execute("UPDATE ServerConfig SET DelCommands = '1' WHERE Guild = " + str(ctx.guild.id))
				conn.commit()
			del_commands.append(ctx.guild.id)

			await ctx.send(content = success_string + ' **Auto-delete of quote commands enabled.**')

		else:

			c.execute("UPDATE ServerConfig SET DelCommands = NULL WHERE Guild = " + str(ctx.guild.id))
			conn.commit()
			del_commands.remove(ctx.guild.id)

			await ctx.send(content = success_string + ' **Auto-delete of quote commands disabled.**')

	@commands.command()
	async def reactions(self, ctx):
		if not ctx.guild or not ctx.author.guild_permissions.manage_guild:
			return

		if ctx.guild.id not in on_reaction:

			try:
				c.execute("INSERT INTO ServerConfig (Guild, OnReaction) VALUES (" + str(ctx.guild.id) + ", '1')")
				conn.commit()
			except sqlite3.IntegrityError:
				c.execute("UPDATE ServerConfig SET OnReaction = '1' WHERE Guild = " + str(ctx.guild.id))
				conn.commit()
			on_reaction.append(ctx.guild.id)

			await ctx.send(content = success_string + ' **Quoting messages on reaction enabled.**')

		else:

			c.execute("UPDATE ServerConfig SET OnReaction = NULL WHERE Guild = " + str(ctx.guild.id))
			conn.commit()
			on_reaction.remove(ctx.guild.id)

			await ctx.send(content = success_string + ' **Quoting messages on reaction disabled.**')


def setup(bot):
	bot.add_cog(Main(bot))
