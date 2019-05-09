import discord
import asyncio
import json
import DBService
from discord.ext import commands
from cogs.Main import server_config

with open('configs/config.json') as json_data:
	response_json = json.load(json_data)

default_prefix = response_json['default_prefix']
token = response_json['token']

async def get_prefix(bot, message):
	if message.guild:
		try:
			if server_config[message.guild.id]['prefix']:
				return commands.when_mentioned_or(server_config[message.guild.id]['prefix'])(bot, message)
			else:
				return commands.when_mentioned_or(default_prefix)(bot, message)
		except KeyError:
			return commands.when_mentioned_or(default_prefix)(bot, message)
	else:
		return commands.when_mentioned_or(default_prefix)(bot, message)

bot = commands.AutoShardedBot(command_prefix = get_prefix, case_insensitive = True, status = discord.Status.idle, activity = discord.Game('starting up...'), fetch_offline_members = False, max_messages = 1000)
bot.remove_command('help')
# A custom command is defined in Help.py

startup_extensions = ['cogs.Main', 'cogs.Help', 'cogs.OwnerOnly', 'cogs.Pin', 'cogs.Snipe', 'cogs.PersonalQuotes', 'cogs.MessageURL', 'cogs.RandomQuotes']
for cog in startup_extensions:
	try:
		bot.load_extension(cog)
	except Exception as e:
		print(e)

if len(response_json['botlog_webhook_url']) > 0 and response_json['botlog_webhook_url'].startswith('https://discordapp.com/api/webhooks/'):
	try:
		bot.load_extension('cogs.BotLog')
	except Exception as e:
		print(e)

if response_json['anti_bot_farm']['enabled'] == True:
	try:
		bot.load_extension('cogs.AntiFarm')
	except Exception as e:
		print(e)

del response_json

@bot.event
async def on_ready():
	print('Logged in as:')
	print(bot.user.name)
	print('------------')

	while True:
		if len(bot.guilds) > 1:
			await bot.change_presence(status = discord.Status.online, activity = discord.Activity(name = 'messages in ' + str(len(bot.guilds)) + ' servers', type = 3))
		else:
			await bot.change_presence(status = discord.Status.online, activity = discord.Activity(name = default_prefix + 'help', type = 1))

		await asyncio.sleep(120)

from cogs.OwnerOnly import blacklist_ids

@bot.event
async def on_guild_join(guild):
	if guild.id in blacklist_ids:
		await guild.leave()

@bot.event
async def on_message(message):
	if message.author.bot or message.author.id in blacklist_ids:
		return
	elif message.guild and message.guild.id in blacklist_ids:
		return await message.guild.leave()

	await bot.process_commands(message)


bot.run(token)
