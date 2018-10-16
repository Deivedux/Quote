import discord
import datetime
import asyncio
import sqlite3
from discord.ext import commands

conn = sqlite3.connect('QuoteBot.db', detect_types = sqlite3.PARSE_DECLTYPES)
c = conn.cursor()

prefixes_raw = c.execute("SELECT * FROM Prefixes").fetchall()
global prefixes
prefixes = {}
for i in prefixes_raw:
	prefixes[int(i[0])] = str(i[1])
del prefixes_raw

server_config_raw = c.execute("SELECT * FROM ServerConfig").fetchall()
del_commands = []
on_reaction = []
for i in server_config_raw:
	if i[1] != None:
		del_commands.append(int(i[0]))
	if i[2] != None:
		on_reaction.append(int(i[0]))
del server_config_raw

quoted_messages = []

class Main:
	def __init__(self, bot):
		self.bot = bot

	async def on_raw_reaction_add(self, payload):
		if str(payload.emoji) == '💬' and not self.bot.get_guild(payload.guild_id).get_member(payload.user_id).bot and payload.guild_id in on_reaction:
			guild = self.bot.get_guild(payload.guild_id)
			channel = guild.get_channel(payload.channel_id)
			user = guild.get_member(payload.user_id)

			if not user.permissions_in(channel).send_messages or payload.message_id in quoted_messages:
				return

			message = None
			async for msg in channel.history(limit = 10000):
				if msg.id == payload.message_id:
					message = msg
					break

			if message:
				if message.author not in guild.members or message.author.color == discord.Colour.default():
					embed = discord.Embed(description = message.content, timestamp = message.created_at)
				else:
					embed = discord.Embed(description = message.content, color = message.author.color, timestamp = message.created_at)
				embed.set_author(name = str(message.author), icon_url = message.author.avatar_url, url = 'https://discordapp.com/channels/' + str(payload.guild_id) + '/' + str(payload.channel_id) + '/' + str(payload.message_id))
				if message.attachments:
					if len(message.attachments) == 1 and message.attachments[0].url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.gifv', '.webp')):
						embed.set_image(url = message.attachments[0].url)
					else:
						attachments = []
						for attachment in message.attachments:
							attachments.append('[' + str(attachment.filename) + '](' + str(attachment.url) + ')')
						embed.add_field(name = 'Attachment(s)', value = '\n'.join(attachments))
				embed.set_footer(text = 'Requester: ' + str(user) + ' | in channel: #' + channel.name)
				await channel.send(embed = embed)

				quoted_messages.append(message.id)
				await asyncio.sleep(2)
				quoted_messages.remove(message.id)

	@commands.command()
	async def help(self, ctx, command = None):
		'''
		Before someone starts accusing this "terrible" help design
		initially the code was not meant to be open-source
		so I didn't care about how dirty or clean the code was
		and right now I'm too busy to make this look cleaner

		So if this really bothers someone
		you are free to remake this into a whatever version you want
		and even include external files if you want, I don't care
		'''
		if not command:
			embed = discord.Embed(title = 'Commands')
			embed.add_field(name = 'help', value = 'Show this message, or more details on a specific command.', inline = False)
			embed.add_field(name = 'quote', value = 'Quote a message using a message ID, and optionally leave your own reply to a quoted message.', inline = False)
			embed.add_field(name = 'quotechan', value = 'Quote a message using a message ID from a specific channel.', inline = False)
			embed.add_field(name = 'prefix', value = 'See currently set prefix, or change to a different prefix for this server.', inline = False)
			embed.add_field(name = 'delcommands', value = 'Toggle this to let Quote auto-delete the quote command.', inline = False)
			embed.add_field(name = 'reactions', value = 'Toggle this to let users quote messages by adding 💬 reaction to them.', inline = False)
			embed.add_field(name = 'pinchannel', value = 'Set a channel that will be used for pinning messages. Members with Manage Messages permission can react with 📌 to pin a message.', inline = False)
			await ctx.send(embed = embed)
		elif command.lower() == 'help':
			embed = discord.Embed()
			embed.add_field(name = '`help`', value = 'Show this message, or more details on a specific command.')
			embed.add_field(name = 'Requires Permissions', value = 'None', inline = False)
			embed.add_field(name = 'Example', value = '`help`')
			await ctx.send(embed = embed)
		elif command.lower() == 'quote':
			embed = discord.Embed()
			embed.add_field(name = '`quote` / `q`', value = 'Quote a message using a message ID, and optionally leave your own reply to a quoted message.')
			embed.add_field(name = 'Requires Permissions', value = 'None', inline = False)
			embed.add_field(name = 'Example', value = '`quote 492444904681897986` or `quote 492444904681897986 this is my reply`')
			await ctx.send(embed = embed)
		elif command.lower() == 'quotechannel':
			embed = discord.Embed()
			embed.add_field(name = '`quotechannel` / `quotechan` / `qchan` / `qc`', value = 'Quote a message using a message ID from a specific channel.')
			embed.add_field(name = 'Requires Permissions', value = 'None', inline = False)
			embed.add_field(name = 'Example', value = '`quotechan #channel 492444904681897986` or `qc #channel 492444904681897986 this is my reply`')
			await ctx.send(embed = embed)
		elif command.lower() == 'prefix':
			embed = discord.Embed()
			embed.add_field(name = '`prefix`', value = 'See currently set prefix, or change to a different prefix for this server.')
			embed.add_field(name = 'Requires Permissions', value = 'Administrator', inline = False)
			embed.add_field(name = 'Example', value = '`prefix` or `prefix >`')
			await ctx.send(embed = embed)
		elif command.lower() == 'delcommands':
			embed = discord.Embed()
			embed.add_field(name = '`delcommands`', value = 'Toggle this to let Quote auto-delete the quote command.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Server', inline = False)
			embed.add_field(name = 'Example', value = '`delcommands`')
			await ctx.send(embed = embed)
		elif command.lower() == 'reactions':
			embed = discord.Embed()
			embed.add_field(name = '`reactions`', value = 'Toggle this to let users quote messages by adding 💬 reaction to them.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Server', inline = False)
			embed.add_field(name = 'Example', value = '`reactions`')
			await ctx.send(embed = embed)
		elif command.lower() == 'pinchannel':
			embed = discord.Embed()
			embed.add_field(name = '`pinchannel` / `pinc`', value = 'Set a channel that will be used for pinning messages. Members with Manage Messages permission can react with 📌 to pin a message.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Server', inline = False)
			embed.add_field(name = 'Example', value = '`pinchannel #pinned-messages`')
			await ctx.send(embed = embed)

	@commands.command(aliases = ['q'])
	async def quote(self, ctx, msg_id: int, *, reply = None):
		if ctx.guild.id in del_commands:
			try:
				await ctx.message.delete()
			except discord.Forbidden:
				pass

		message = None
		async with ctx.channel.typing():
			async for msg in ctx.channel.history(limit = 1000, before = ctx.message):
				perms = ctx.guild.me.permissions_in(ctx.channel)
				if not perms.read_messages or not perms.read_message_history:
					break
				if msg.id == msg_id:
					message = msg
					break
			if not message:
				for channel in ctx.guild.text_channels:
					perms = ctx.guild.me.permissions_in(channel)
					if not perms.read_messages or not perms.read_message_history or channel == ctx.channel:
						continue
					async for msg in channel.history(limit = 1000):
						if msg.id == msg_id:
							message = msg
							break

		if not message:
			await ctx.send(content = '<:xmark:314349398824058880> **Could not find the specified message.**')
		else:
			if message.author not in ctx.guild.members or message.author.color == discord.Colour.default():
				embed = discord.Embed(description = message.content, timestamp = message.created_at)
			else:
				embed = discord.Embed(description = message.content, color = message.author.color,  timestamp = message.created_at)
			embed.set_author(name = str(message.author), icon_url = message.author.avatar_url, url = 'https://discordapp.com/channels/' + str(ctx.guild.id) + '/' + str(message.channel.id) + '/' + str(message.id))
			if message.attachments:
				if len(message.attachments) == 1 and message.attachments[0].url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.gifv', '.webp')):
					embed.set_image(url = message.attachments[0].url)
				else:
					attachments = []
					for attachment in message.attachments:
						attachments.append('[' + str(attachment.filename) + '](' + str(attachment.url) + ')')
					embed.add_field(name = 'Attachment(s)', value = '\n'.join(attachments))
			embed.set_footer(text = 'Requester: ' + str(ctx.author) + ' | in channel: #' + message.channel.name)
			await ctx.send(embed = embed)

			if reply:
				await ctx.send(content = '**' + ctx.author.display_name + '\'s reply:**\n' + reply)

	@commands.command(aliases = ['quotechan', 'qchan', 'qc'])
	async def quotechannel(self, ctx, channel: discord.TextChannel, msg_id: int, *, reply = None):
		if ctx.guild.id in del_commands:
			try:
				await ctx.message.delete()
			except discord.Forbidden:
				pass

		message = None
		async with ctx.channel.typing():
			async for msg in channel.history(limit = 10000, before = ctx.message):
				perms = ctx.guild.me.permissions_in(channel)
				if not perms.read_messages or not perms.read_message_history:
					break
				if msg.id == msg_id:
					message = msg
					break

		if not message:
			await ctx.send(content = '<:xmark:314349398824058880> **Could not find the specified message.**')
		else:
			if message.author not in ctx.guild.members or message.author.color == discord.Colour.default():
				embed = discord.Embed(description = message.content, timestamp = message.created_at)
			else:
				embed = discord.Embed(description = message.content, color = message.author.color,  timestamp = message.created_at)
			embed.set_author(name = str(message.author), icon_url = message.author.avatar_url, url = 'https://discordapp.com/channels/' + str(ctx.guild.id) + '/' + str(message.channel.id) + '/' + str(message.id))
			if message.attachments:
				if len(message.attachments) == 1 and message.attachments[0].url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.gifv', '.webp')):
					embed.set_image(url = message.attachments[0].url)
				else:
					attachments = []
					for attachment in message.attachments:
						attachments.append('[' + str(attachment.filename) + '](' + str(attachment.url) + ')')
					embed.add_field(name = 'Attachment(s)', value = '\n'.join(attachments))
			embed.set_footer(text = 'Requester: ' + str(ctx.author) + ' | in channel: #' + message.channel.name)
			await ctx.send(embed = embed)

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
				guild_prefix = '>'

			await ctx.send(content = '**My prefix here is `' + guild_prefix + '`.**')

		else:

			if not ctx.author.guild_permissions.administrator:
				return

			if len(prefix) > 5 or '\n' in prefix:
				return await ctx.send(content = '<:xmark:314349398824058880> **Invalid prefix format. Make sure of the following:\n• Prefix is not over 5 characters long.\n• Prefix does not contain new lines.**')

			try:
				c.execute("INSERT INTO Prefixes (Guild, Prefix) VALUES ('" + str(ctx.guild.id) + "', '" + str(prefix).replace('\'', '\'\'') + "')")
				conn.commit()
			except sqlite3.IntegrityError:
				c.execute("UPDATE Prefixes SET Prefix = '" + str(prefix).replace('\'', '\'\'') + "' WHERE Guild = " + str(ctx.guild.id))
				conn.commit()
			prefixes[ctx.guild.id] = prefix

			await ctx.send(content = '<:check:314349398811475968> **Prefix changed to `' + prefix + '`.**')

	@commands.command()
	async def delcommands(self, ctx):
		if not ctx.guild or not ctx.author.guild_permissions.manage_guild:
			return

		if ctx.guild.id not in del_commands:

			try:
				c.execute("INSERT INTO ServerConfig (Guild, DelCommands) VALUES ('" + str(ctx.guild.id) + "', '1')")
				conn.commit()
			except sqlite3.IntegrityError:
				c.execute("UPDATE ServerConfig SET DelCommands = '1' WHERE Guild = " + str(ctx.guild.id))
				conn.commit()
			del_commands.append(ctx.guild.id)

			await ctx.send(content = '<:check:314349398811475968> **Auto-delete of quote command enabled.**')

		else:

			c.execute("UPDATE ServerConfig SET DelCommands = NULL WHERE Guild = " + str(ctx.guild.id))
			conn.commit()
			del_commands.remove(ctx.guild.id)

			await ctx.send(content = '<:check:314349398811475968> **Auto-delete of quote command disabled.**')

	@commands.command()
	async def reactions(self, ctx):
		if not ctx.guild or not ctx.author.guild_permissions.manage_guild:
			return

		if ctx.guild.id not in on_reaction:

			try:
				c.execute("INSERT INTO ServerConfig (Guild, OnReaction) VALUES ('" + str(ctx.guild.id) + "', '1')")
				conn.commit()
			except sqlite3.IntegrityError:
				c.execute("UPDATE ServerConfig SET OnReaction = '1' WHERE Guild = " + str(ctx.guild.id))
				conn.commit()
			on_reaction.append(ctx.guild.id)

			await ctx.send(content = '<:check:314349398811475968> **Quoting messages on reaction enabled.**')

		else:

			c.execute("UPDATE ServerConfig SET OnReaction = NULL WHERE Guild = " + str(ctx.guild.id))
			conn.commit()
			on_reaction.remove(ctx.guild.id)

			await ctx.send(content = '<:check:314349398811475968> **Quoting messages on reaction disabled.**')


def setup(bot):
	bot.add_cog(Main(bot))
