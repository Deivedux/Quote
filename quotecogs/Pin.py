import discord
import sqlite3
from discord.ext import commands

conn = sqlite3.connect('/config/QuoteBot.db')
c = conn.cursor()

server_config_raw = c.execute("SELECT * FROM ServerConfig").fetchall()
pin_channels = {}
for i in server_config_raw:
	if i[3] != None:
		pin_channels[int(i[0])] = int(i[3])
del server_config_raw

class Pin:
	def __init__(self, bot):
		self.bot = bot

	async def on_raw_reaction_add(self, payload):
		if str(payload.emoji) == '📌':
			try:
				channel = self.bot.get_channel(pin_channels[payload.guild_id])
			except KeyError:
				return
			except discord.NotFound:
				c.execute("UPDATE ServerConfig SET PinChannel = NULL WHERE Guild = " + str(payload.guild_id))
				conn.commit()
				del pin_channels[payload.guild_id]
				return

			guild = self.bot.get_guild(payload.guild_id)
			user = guild.get_member(payload.user_id)
			pin_channel = self.bot.get_channel(payload.channel_id)
			if not user.permissions_in(pin_channel).manage_messages:
				return

			message = None
			async for msg in self.bot.get_channel(payload.channel_id).history(limit = 10000):
				if msg.channel.id == pin_channels[payload.guild_id]:
					break
				if msg.id == payload.message_id and (msg.content or msg.attachments):
					message = msg
					break

			if message:
				async for msg in channel.history(limit = 50):
					if msg.content.startswith('📌 **Message ID:** ' + str(payload.message_id)):
						return

				embed = discord.Embed(description = message.content, color = 0xD4AC0D, timestamp = message.created_at)
				embed.set_author(name = str(message.author), icon_url = message.author.avatar_url, url = 'https://discordapp.com/channels/' + str(payload.guild_id) + '/' + str(payload.channel_id) + '/' + str(payload.message_id))
				if message.attachments:
					if len(message.attachments) == 1 and message.attachments[0].url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.gifv', '.webp')):
						embed.set_image(url = message.attachments[0].url)
					else:
						attachments = []
						for attachment in message.attachments:
							attachments.append('[' + str(attachment.filename) + '](' + str(attachment.url) + ')')
						embed.add_field(name = 'Attachment(s)', value = '\n'.join(attachments))

				await channel.send(content = '📌 **Message ID:** ' + str(payload.message_id) + ' | ' + pin_channel.mention, embed = embed)

	@commands.command(aliases = ['pinc'])
	async def pinchannel(self, ctx, channel: discord.TextChannel = None):
		if not ctx.guild or not ctx.author.guild_permissions.manage_guild:
			return

		if channel:

			perms = ctx.guild.me.permissions_in(channel)
			if not perms.read_messages or not perms.read_message_history or not perms.send_messages or not perms.embed_links:
				return await ctx.send(content = '<:xmark:314349398824058880> **Make sure I have all of the following permissions in that channel before enabling pins:\n• Read Messages\n• Read Message History\n• Send Messages\n• Embed Links**')

			try:
				c.execute("INSERT INTO ServerConfig (Guild, PinChannel) VALUES ('" + str(ctx.guild.id) + "', '" + str(channel.id) + "')")
				conn.commit()
			except sqlite3.IntegrityError:
				c.execute("UPDATE ServerConfig SET PinChannel = '" + str(channel.id) + "' WHERE Guild = " + str(ctx.guild.id))
				conn.commit()
			pin_channels[ctx.guild.id] = channel.id

			await ctx.send(content = '<:check:314349398811475968> **Pin channel set to ' + channel.mention + '.**')

		else:

			c.execute("UPDATE ServerConfig SET PinChannel = NULL WHERE Guild = " + str(ctx.guild.id))
			conn.commit()
			del pin_channels[ctx.guild.id]

			await ctx.send(content = '<:check:314349398811475968> **Pin channel disabled.**')


def setup(bot):
	bot.add_cog(Pin(bot))
