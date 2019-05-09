import discord
import asyncio
import json
import aiohttp
import datetime
from DBService import DBService
from discord.ext import commands
from cogs.OwnerOnly import blacklist_ids

server_config_raw = DBService.exec("SELECT * FROM ServerConfig").fetchall()
server_config = dict()

def cache_guild(db_response):
	server_config[db_response[0]] = {'prefix': db_response[1], 'del_commands': True if db_response[2] else False, 'on_reaction': True if db_response[3] else False}

for i in server_config_raw:
	cache_guild(i)

del server_config_raw

with open('configs/config.json') as json_data:
	response_json = json.load(json_data)
	default_prefix = response_json['default_prefix']
	success_string = response_json['response_string']['success']
	error_string = response_json['response_string']['error']
	del response_json

def quote_embed(context_channel, message, user):
	if not message.content and message.embeds and message.author.bot:
		embed = message.embeds[0]
	else:
		if message.author not in message.guild.members or message.author.color == discord.Colour.default():
			embed = discord.Embed(description = message.content, timestamp = message.created_at)
		else:
			embed = discord.Embed(description = message.content, color = message.author.color, timestamp = message.created_at)
		if message.attachments:
			if message.channel.is_nsfw() and not context_channel.is_nsfw():
				embed.add_field(name = 'Attachments', value = ':underage: **Quoted message belongs in NSFW channel.**')
			elif len(message.attachments) == 1 and message.attachments[0].url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.gifv', '.webp', '.bmp')):
				embed.set_image(url = message.attachments[0].url)
			else:
				for attachment in message.attachments:
					embed.add_field(name = 'Attachment', value = '[' + attachment.filename + '](' + attachment.url + ')', inline = False)
		embed.set_author(name = str(message.author), icon_url = message.author.avatar_url, url = 'https://discordapp.com/channels/' + str(message.guild.id) + '/' + str(message.channel.id) + '/' + str(message.id))
		if message.channel != context_channel:
			embed.set_footer(text = 'Quoted by: ' + str(user) + ' | in channel: #' + message.channel.name)
		else:
			embed.set_footer(text = 'Quoted by: ' + str(user))
	return embed

class Main(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		for guild in self.bot.guilds:
			try:
				DBService.exec("INSERT INTO ServerConfig (Guild) VALUES (" + str(guild.id) + ")")
			except Exception:
				continue

		server_config_raw = DBService.exec("SELECT * FROM ServerConfig").fetchall()
		for i in server_config_raw:
			cache_guild(i)

		guild_ids = [guild.id for guild in self.bot.guilds]
		cached_guilds = [i for i in server_config.keys()]

		for i in cached_guilds:
			if i not in guild_ids:
				del cached_guilds[i]

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		try:
			del server_config[guild.id]
		except KeyError:
			pass

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		try:
			DBService.exec("INSERT INTO ServerConfig (Guild) VALUES (" + str(guild.id) + ")")
		except Exception:
			pass

		db_response = DBService.exec("SELECT * FROM ServerConfig WHERE Guild = " + str(guild.id)).fetchone()
		cache_guild(db_response)

	'''@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(content = error_string + ' **Please wait ' + str(round(error.retry_after, 1)) + ' seconds before invoking this again.**', delete_after = 5)
'''
	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if str(payload.emoji) == '💬' and payload.user_id not in blacklist_ids and not self.bot.get_guild(payload.guild_id).get_member(payload.user_id).bot and server_config[payload.guild_id]['on_reaction']:
			guild = self.bot.get_guild(payload.guild_id)
			channel = guild.get_channel(payload.channel_id)
			user = guild.get_member(payload.user_id)

			if user.permissions_in(channel).send_messages:
				try:
					message = await channel.fetch_message(payload.message_id)
				except discord.NotFound:
					return
				except discord.Forbidden:
					return
				else:
					if not message.content and message.embeds and message.author.bot:
						await channel.send(content = 'Raw embed from `' + str(message.author).strip('`') + '` in ' + message.channel.mention, embed = quote_embed(channel, message, user))
					else:
						await channel.send(embed = quote_embed(channel, message, user))

	@commands.command(aliases = ['q'])
	@commands.cooldown(rate = 2, per = 5, type = commands.BucketType.channel)
	async def quote(self, ctx, msg_arg = None, *, reply = None):
		if not msg_arg:
			return await ctx.send(content = error_string + ' **Please provide a valid message argument.**')

		if ctx.guild and server_config[ctx.guild.id]['del_commands'] and ctx.guild.me.permissions_in(ctx.channel).manage_messages:
			await ctx.message.delete()

		message = None
		try:
			msg_arg = int(msg_arg)
		except ValueError:
			perms = ctx.guild.me.permissions_in(ctx.channel)
			if perms.read_messages and perms.read_message_history:
				async for msg in ctx.channel.history(limit = 100, before = ctx.message):
					if msg_arg.lower() in msg.content.lower():
						message = msg
						break
		else:
			try:
				message = await ctx.channel.fetch_message(msg_arg)
			except:
				for channel in ctx.guild.text_channels:
					perms = ctx.guild.me.permissions_in(channel)
					if channel == ctx.channel or not perms.read_messages or not perms.read_message_history:
						continue

					try:
						message = await channel.fetch_message(msg_arg)
					except:
						continue
					else:
						break

		if message:
			if not message.content and message.embeds and message.author.bot:
				await ctx.send(content = 'Raw embed from `' + str(message.author).strip('`') + '` in ' + message.channel.mention, embed = quote_embed(ctx.channel, message, ctx.author))
			else:
				await ctx.send(embed = quote_embed(ctx.channel, message, ctx.author))
			if reply:
				await ctx.send(content = '**' + ctx.author.display_name + '\'s reply:**\n' + reply.replace('@everyone', '@еveryone').replace('@here', '@hеre'))
		else:
			await ctx.send(content = error_string + ' **Could not find the specified message.**')

	@commands.command()
	async def prefix(self, ctx, *, prefix = None):
		if not ctx.guild:
			return

		if not prefix:

			guild_prefix = server_config[ctx.guild.id]['prefix'] if server_config[ctx.guild.id]['prefix'] is not None else default_prefix
			await ctx.send(content = '**My prefix here is** `' + guild_prefix + '`')

		else:

			if not ctx.author.guild_permissions.administrator:
				return

			if len(prefix) > 5 or '\n' in prefix:
				return await ctx.send(content = error_string + ' **Invalid prefix format. Make sure of the following:\n• Prefix is not over 5 characters long.\n• Prefix does not contain new lines.**')

			try:
				DBService.exec("INSERT INTO ServerConfig (Guild, Prefix) VALUES (" + str(ctx.guild.id) + ", '" + str(prefix).replace('\'', '\'\'') + "')")
			except Exception:
				DBService.exec("UPDATE ServerConfig SET Prefix = '" + str(prefix).replace('\'', '\'\'') + "' WHERE Guild = " + str(ctx.guild.id))
			server_config[ctx.guild.id]['prefix'] = prefix

			await ctx.send(content = success_string + ' **Prefix changed to** `' + prefix + '`')

	@commands.command(aliases = ['delcmds'])
	@commands.has_permissions(manage_guild = True)
	async def delcommands(self, ctx):
		if not server_config[ctx.guild.id]['del_commands']:

			try:
				DBService.exec("INSERT INTO ServerConfig (Guild, DelCommands) VALUES (" + str(ctx.guild.id) + ", '1')")
			except Exception:
				DBService.exec("UPDATE ServerConfig SET DelCommands = '1' WHERE Guild = " + str(ctx.guild.id))
			server_config[ctx.guild.id]['del_commands'] = True

			await ctx.send(content = success_string + ' **Auto-delete of quote commands enabled.**')

		else:

			DBService.exec("UPDATE ServerConfig SET DelCommands = NULL WHERE Guild = " + str(ctx.guild.id))
			server_config[ctx.guild.id]['del_commands'] = False

			await ctx.send(content = success_string + ' **Auto-delete of quote commands disabled.**')

	@commands.command()
	@commands.has_permissions(manage_guild = True)
	async def reactions(self, ctx):
		if not server_config[ctx.guild.id]['on_reaction']:

			try:
				DBService.exec("INSERT INTO ServerConfig (Guild, OnReaction) VALUES (" + str(ctx.guild.id) + ", '1')")
			except Exception:
				DBService.exec("UPDATE ServerConfig SET OnReaction = '1' WHERE Guild = " + str(ctx.guild.id))
			server_config[ctx.guild.id]['on_reaction'] = True

			await ctx.send(content = success_string + ' **Quoting messages on reaction enabled.**')

		else:

			DBService.exec("UPDATE ServerConfig SET OnReaction = NULL WHERE Guild = " + str(ctx.guild.id))
			server_config[ctx.guild.id]['on_reaction'] = False

			await ctx.send(content = success_string + ' **Quoting messages on reaction disabled.**')

	@commands.command(aliases = ['dupe'])
	@commands.has_permissions(manage_guild = True)
	@commands.cooldown(rate = 2, per = 30, type = commands.BucketType.guild)
	async def duplicate(self, ctx, msgs: int, from_channel: discord.TextChannel, to_channel: discord.TextChannel = None):
		if not to_channel:
			to_channel = ctx.channel

		if not ctx.author.permissions_in(from_channel).read_messages or not ctx.author.permissions_in(from_channel).read_message_history:

			return

		elif not ctx.guild.me.permissions_in(ctx.channel).manage_webhooks:

			await ctx.send(content = error_string + ' **Duplicating messages require me to have `Manage Webhooks` permission in the target channel.**')

		elif not ctx.guild.me.permissions_in(from_channel).read_messages or not ctx.guild.me.permissions_in(from_channel).read_message_history:

			await ctx.send(content = error_string + ' **I do not have enough permissions to fetch messages from** ' + from_channel.mention)

		else:

			if msgs > 100:
				msgs = 100

			messages = list()
			async for msg in from_channel.history(limit = msgs, before = ctx.message):
				messages.append(msg)

			webhook = await ctx.channel.create_webhook(name = 'Message Duplicator')

			for msg in reversed(messages):
				await asyncio.sleep(0.5)
				async with aiohttp.ClientSession() as session:
					webhook_channel = discord.Webhook.from_url(webhook.url, adapter = discord.AsyncWebhookAdapter(session))
					try:
						await webhook_channel.send(username = msg.author.display_name, avatar_url = msg.author.avatar_url, content = msg.content, embeds = msg.embeds, wait = True)
					except:
						continue

			await webhook.delete()

	@commands.command()
	@commands.cooldown(rate = 2, per = 5, type = commands.BucketType.user)
	async def lookup(self, ctx, arg):
		try:
			invite = await self.bot.fetch_invite(arg, with_counts = True)
		except discord.NotFound:
			await ctx.send(content = error_string + ' **Invalid invite, or I\'m banned from there.**')
		else:
			def chan_type(channel):
				if isinstance(channel, discord.PartialInviteChannel):
					if channel.type == discord.ChannelType.text:
						return '#'
					elif channel.type == discord.ChannelType.voice:
						return '\\🔊'
					else:
						return ''
				else:
					if isinstance(channel, discord.TextChannel):
						return '#'
					elif isinstance(channel, discord.VoiceChannel):
						return '\\🔊'
					else:
						return ''

			desc = '• Server: **' + str(invite.guild) + '** (' + str(invite.guild.id) + ')\n• Channel: **' + chan_type(invite.channel) + str(invite.channel) + '** (' + str(invite.channel.id) + ')\n' + ('• Inviter: **' + str(invite.inviter) + '** (' + str(invite.inviter.id) + ')\n' if invite.inviter else '') + ('• Features: ' + ', '.join(['**' + feature + '**' for feature in invite.guild.features]) + '\n' if invite.guild.features else '') + '\n• Active Members: **' + str(invite.approximate_presence_count) + '** / **' + str(invite.approximate_member_count) + '**'
			embed = discord.Embed(title = 'About Invite', description = desc, color = 0x08FF00)
			if invite.guild.icon:
				embed.set_thumbnail(url = invite.guild.icon_url_as(size = 128))
			if invite.guild.banner:
				embed.set_image(url = invite.guild.banner_url)
			await ctx.send(embed = embed)

	@commands.command()
	async def snowflake(self, ctx, snowflake: int):
		await ctx.send(content = '```fix\n' + discord.utils.snowflake_time(snowflake).strftime('%A %Y/%m/%d %H:%M:%S UTC') + '\n```')


def setup(bot):
	bot.add_cog(Main(bot))
