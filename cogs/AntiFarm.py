import discord
import json
from discord.ext import commands

with open('configs/config.json') as json_data:
	response_json = json.load(json_data)

farm_conditions = response_json['anti_bot_farm']['leave_guild_if']
del response_json

class AntiFarm(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		for guild in self.bot.guilds:
			if guild.member_count > farm_conditions['min_member_count']:
				bots = [member for member in guild.members if member.bot]
				result = (len(bots) / guild.member_count) * 100
				if result > farm_conditions['min_bot_rate']:
					await guild.leave()

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		if guild.member_count > farm_conditions['min_member_count']:
			bots = [member for member in guild.members if member.bot]
			result = (len(bots) / guild.member_count) * 100
			if result > farm_conditions['min_bot_rate']:
				await guild.leave()

	@commands.Cog.listener()
	async def on_member_join(self, member):
		if member.guild.member_count > farm_conditions['min_member_count']:
			bots = [member for member in member.guild.members if member.bot]
			result = (len(bots) / member.guild.member_count) * 100
			if result > farm_conditions['min_bot_rate']:
				await member.guild.leave()

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.guild.member_count > farm_conditions['min_member_count']:
			bots = [member for member in member.guild.members if member.bot]
			result = (len(bots) / member.guild.member_count) * 100
			if result > farm_conditions['min_bot_rate']:
				await member.guild.leave()


def setup(bot):
	bot.add_cog(AntiFarm(bot))
