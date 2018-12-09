import discord
import json
from discord.ext import commands
from cogs.Main import prefixes

with open('configs/config.json') as json_data:
	response_json = json.load(json_data)

default_prefix = response_json['default_prefix']
error_string = response_json['response_string']['error']
del response_json

class Help:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def help(self, ctx, command = None):
		try:
			guild_prefix = prefixes[ctx.guild.id]
		except KeyError:
			guild_prefix = default_prefix

		with open('commands.json') as json_data:
			commands_json = json.load(json_data)

		if not command:

			embed = discord.Embed(color = 0x08FF00)
			embed.add_field(name = 'Links', value = '[Support Server](https://discord.gg/sbySHxA)\n[Add Me](https://discordapp.com/oauth2/authorize?client_id=' + str(self.bot.user.id) + '&permissions=84992&scope=bot)\n[Documentation](https://quote.readthedocs.io/en/latest/)\n[Vote For Me](https://discordbots.org/bot/447176783704489985/vote)')
			embed.add_field(name = 'Commands', value = ', '.join(['`' + guild_prefix + i + '`' for i in commands_json.keys()]))
			embed.set_footer(text = guild_prefix + 'help [command_name] for more details.')
			await ctx.send(embed = embed)

		else:

			try:
				command_help = commands_json[command.lower()]
			except KeyError:
				return await ctx.send(content = error_string + ' **Command with that name does not exist.**')

			embed = discord.Embed(title = ' / '.join(['`' + guild_prefix + i + '`' for i in command_help['title']]), description = command_help['description'], color = 0x08FF00)
			embed.add_field(name = 'Example', value = ' or '.join(['`' + guild_prefix + i + '`' for i in command_help['examples']]))
			await ctx.send(embed = embed)


def setup(bot):
	bot.add_cog(Help(bot))
