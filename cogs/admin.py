from discord.ext import commands
import datetime

class Admin(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        send_at = ctx.message.created_at
        now_at = datetime.datetime.now()
        ping = (now_at - send_at).microseconds / 1000
        await ctx.reply(f'ping: {ping}ms')

    

def setup(bot):
    return bot.add_cog(Admin(bot))