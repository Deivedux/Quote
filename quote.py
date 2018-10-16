import discord
import asyncio
import sqlite3
import json
from io import StringIO
from discord.ext import commands

conn = sqlite3.connect('QuoteBot.db', detect_types = sqlite3.PARSE_DECLTYPES)
c = conn.cursor()
# Create necessary database tables, if they don't exist already, on it's own behalf.
c.execute("CREATE TABLE IF NOT EXISTS Prefixes (Guild TEXT unique, Prefix TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS ServerConfig (Guild TEXT unique, DelCommands TEXT, OnReaction TEXT, PinChannel TEXT)")
# P.S: I'm very used to storing everything as TEXT,
# so I'd appreciate if you don't change this syntax,
# especially since the public Quote bot already
# uses this syntax.

from quotecogs.Main import prefixes

with open('config.json') as json_data:
	response_json = json.load(json_data)
	default_prefix = response_json['default_prefix']
	token = response_json['token']
	owners = response_json['owner_ids']

async def get_prefix(bot, message):
	if message.guild:
		try:
			return commands.when_mentioned_or(prefixes[message.guild.id])(bot, message)
		except KeyError:
			return commands.when_mentioned_or(default_prefix)(bot, message)
	else:
		return commands.when_mentioned_or(default_prefix)(bot, message)

bot = commands.Bot(command_prefix = get_prefix, case_insensitive = True, status = discord.Status.idle, activity = discord.Game('starting up...'), max_messages = 100)
bot.remove_command('help')
# A custom command is defined in Help.py

startup_extensions = ['quotecogs.Main', 'quotecogs.OwnerOnly', 'quotecogs.Pin']
for cog in startup_extensions:
	try:
		bot.load_extension(cog)
	except Exception as e:
		print(e)

@bot.event
async def on_ready():
	print('Logged in as:')
	print(bot.user.name)
	print('------------')

	for guild in bot.guilds:
		if len(guild.members) > 20:
			bots = []
			for member in guild.members:
				if member.bot:
					bots.append(member)
			result = len(bots) / len(guild.members) * 100
			if float(result) > 70.0:
				await guild.leave()

	while True:
		await bot.change_presence(status = discord.Status.online, activity = discord.Activity(name = 'messages in ' + str(len(bot.guilds)) + ' servers', type = 3))
		await asyncio.sleep(120)

# The 3 events below are bot-farm checks.
# The bot leaves the server if BOTH conditions are met:
# • more than 20 total members
# • more than 70% of them are bots
@bot.event
async def on_guild_join(guild):
	if len(guild.members) > 20:
		bots = []
		for member in guild.members:
			if member.bot:
				bots.append(member)
		result = len(bots) / len(guild.members) * 100
		if float(result) > 70.0:
			await guild.leave()

@bot.event
async def on_member_join(member):
	if len(member.guild.members) > 20:
		bots = []
		for member in member.guild.members:
			if member.bot:
				bots.append(member)
		result = len(bots) / len(member.guild.members) * 100
		if float(result) > 70.0:
			await member.guild.leave()

@bot.event
async def on_member_remove(member):
	if len(member.guild.members) > 20:
		bots = []
		for member in member.guild.members:
			if member.bot:
				bots.append(member)
		result = len(bots) / len(member.guild.members) * 100
		if float(result) > 70.0:
			await member.guild.leave()

# END OF BOT-FARM CHECKS

# Bot owners are able to add 🗑 reaction to own bot
# messages to delete themselves.
# Only works with cached messages.
@bot.event
async def on_reaction_add(reaction, user):
	if reaction.emoji == '🗑' and user.id in owners and reaction.message.author == bot.user:
		await reaction.message.delete()

# Prevents from reading other bot messages.
@bot.event
async def on_message(message):
	if message.author.bot:
		return

	await bot.process_commands(message)


bot.run(token)
