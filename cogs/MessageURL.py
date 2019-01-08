import discord
from discord.ext import commands
from cogs.OwnerOnly import blacklist_ids

def quote_embed(context_channel, message, user):
	if not message.content and message.embeds and message.author.bot:
		message_embed = message.embeds[0]
		embed = discord.Embed(title = message_embed.title, description = message_embed.description, url = message_embed.url, color = message_embed.color, timestamp = message.created_at)
		if message_embed.image:
			if message.channel.is_nsfw() and not context_channel.is_nsfw():
				pass
			else:
				embed.set_image(url = message_embed.image.url)
		if message_embed.thumbnail:
			if message.channel.is_nsfw() and not context_channel.is_nsfw():
				pass
			else:
				embed.set_thumbnail(url = message_embed.image.url)
		if message_embed.fields:
			for field in message_embed.fields:
				embed.add_field(name = field.name, value = field.value, inline = field.inline)
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
					except:
						continue
					else:
						await message.channel.send(embed = quote_embed(message.channel, msg_found, message.author))


def setup(bot):
	bot.add_cog(MessageURL(bot))
