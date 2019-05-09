import discord
import sqlite3
import json
from DBService import DBService
from discord.ext import commands
from cogs.OwnerOnly import blacklist_ids

server_config_raw = DBService.exec("SELECT * FROM ServerConfig").fetchall()
pin_channels = {}
for i in server_config_raw:
	if i[4] != None:
		pin_channels[int(i[0])] = int(i[4])
del server_config_raw

with open('configs/config.json') as json_data:
	response_json = json.load(json_data)
	success_string = response_json['response_string']['success']
	error_string = response_json['response_string']['error']
	del response_json

def pin_embed(message):
	embed = discord.Embed(description = message.content, color = 0xD4AC0D, timestamp = message.created_at)
	embed.set_author(name = str(message.author), icon_url = message.author.avatar_url, url = 'https://discordapp.com/channels/' + str(message.guild.id) + '/' + str(message.channel.id) + '/' + str(message.id))
	if message.attachments:
		if message.channel.is_nsfw() and not context_channel.is_nsfw():
			embed.add_field(name = 'Attachments', value = ':underage: **Quoted message belongs in NSFW channel.**')
		elif len(message.attachments) == 1 and message.attachments[0].url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.gifv', '.webp', '.bmp')):
			embed.set_image(url = message.attachments[0].url)
		else:
			attachment_count = 0
			for attachment in message.attachments:
				attachment_count+=1
				embed.add_field(name = 'Attachment ' + str(attachment_count), value = '[' + attachment.filename + '](' + attachment.url + ')', inline = False)

	return embed

class Pin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if str(payload.emoji) == '📌' and payload.user_id not in blacklist_ids and not self.bot.get_guild(payload.guild_id).get_member(payload.user_id).bot:
			guild = self.bot.get_guild(payload.guild_id)
			try:
				channel = guild.get_channel(pin_channels[payload.guild_id])
			except KeyError:
				return
			else:
				if not channel:
					DBService.exec("UPDATE ServerConfig SET PinChannel = NULL WHERE Guild = " + str(payload.guild_id))
					del pin_channels[payload.guild_id]
					return

			user = guild.get_member(payload.user_id)
			pin_channel = self.bot.get_channel(payload.channel_id)
			if not user.permissions_in(pin_channel).manage_messages or channel == pin_channel:
				return

			try:
				message = await pin_channel.fetch_message(payload.message_id)
			except discord.Forbidden:
				return
			else:
				async for msg in channel.history(limit = 100):
					if str(payload.message_id) in msg.content:
						return

				await channel.send(content = '📌 **Message ID:** ' + str(payload.message_id) + ' | ' + pin_channel.mention, embed = pin_embed(message))

	@commands.command(aliases = ['pinc'])
	async def pinchannel(self, ctx, channel: discord.TextChannel = None):
		if not ctx.guild or not ctx.author.guild_permissions.manage_guild:
			return

		if channel:

			perms = ctx.guild.me.permissions_in(channel)
			if not perms.read_messages or not perms.read_message_history or not perms.send_messages or not perms.embed_links:
				return await ctx.send(content = error_string + ' **Make sure I have all of the following permissions in that channel before enabling pins:\n• Read Messages\n• Read Message History\n• Send Messages\n• Embed Links**')

			try:
				DBService.exec("INSERT INTO ServerConfig (Guild, PinChannel) VALUES (" + str(ctx.guild.id) + ", " + str(channel.id) + ")")
			except Exception:
				DBService.exec("UPDATE ServerConfig SET PinChannel = " + str(channel.id) + " WHERE Guild = " + str(ctx.guild.id))
			pin_channels[ctx.guild.id] = channel.id

			await ctx.send(content = success_string + ' **Pin channel set to** ' + channel.mention)

		else:

			DBService.exec("UPDATE ServerConfig SET PinChannel = NULL WHERE Guild = " + str(ctx.guild.id))
			del pin_channels[ctx.guild.id]

			await ctx.send(content = success_string + ' **Pin channel disabled.**')


def setup(bot):
	bot.add_cog(Pin(bot))
