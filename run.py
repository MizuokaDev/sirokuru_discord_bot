from sys import prefix
from discord.ext import commands
from config import config

config = config()
prefix = config.read('settings', 'prefix')
token = config.read('settings', 'token')
bot = commands.Bot(prefix)

bot.load_extension('cogs.ticket')
bot.load_extension('cogs.admin')
bot.load_extension('cogs.role')

bot.run(token)