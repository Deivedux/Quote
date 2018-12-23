import discord
from discord.ext import commands
from cogs.OwnerOnly import blacklist_ids

def quote_embed(message, user):
	if message.author not in message.guild.members or message.author.color == discord.Colour.default():
		embed = discord.Embed(description = message.content, timestamp = message.created_at)
	else:
		embed = discord.Embed(description = message.content, color = message.author.color, timestamp = message.created_at)
	embed.set_author(name = str(message.author), icon_url = message.author.avatar_url, url = 'https://discordapp.com/channels/' + str(message.guild.id) + '/' + str(message.channel.id) + '/' + str(message.id))
	if message.attachments:
		if len(message.attachments) == 1 and message.attachments[0].url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.gifv', '.webp', '.bmp')):
			embed.set_image(url = message.attachments[0].url)
		else:
			embed.add_field(name = 'Attachment(s)', value = '\n'.join(['[' + str(attachment.filename) + '](' + str(attachment.url) + ')' for attachment in message.attachments]))
	embed.set_footer(text = 'Linked by: ' + str(user))
	return embed

class MessageURL:
	def __init__(self, bot):
		self.bot = bot

	async def on_message(self, message):
		perms = message.guild.me.permissions_in(message.channel)
		if not perms.send_messages or not perms.embed_links or message.author.bot or message.author.id in blacklist_ids:
			return

		for i in message.content.split():
			word = i.lower().strip('<>')
			if word.startswith('https://canary.discordapp.com/channels/'):
				word = word.strip('https://canary.discordapp.com/channels/')
			elif word.startswith('https://discordapp.com/channels/'):
				word = word.strip('https://discordapp.com/channels/')
			else:
				continue

			list_ids = word.split('/')
			if len(list_ids) == 3:
				del list_ids[0]

				try:
					channel = self.bot.get_channel(int(list_ids[0]))
				except:
					continue

				if channel and isinstance(channel, discord.TextChannel):
					try:
						msg_id = int(list_ids[1])
					except:
						continue
					
					try:
						msg_found = await channel.get_message(msg_id)
					except discord.NotFound:
						continue
					except discord.Forbidden:
						continue
					else:
						await message.channel.send(embed = quote_embed(msg_found, message.author))


def setup(bot):
	bot.add_cog(MessageURL(bot))
