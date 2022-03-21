from discord.ext import commands
import config

config = config.config()

class Role(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name='on_raw_reaction_add')
    async def add_vc_role(self, payload):
        if payload.emoji.name == "👍" and payload.message_id == int(config.read('role', 'vc_role_message_id')):
            guild = await self.bot.fetch_guild(payload.guild_id)
            member = await guild.fetch_member(payload.user_id)
            role = guild.get_role(int(config.read('role', 'vc_role_id')))
            print(type(role))
            await member.add_roles(role)
    

def setup(bot):
    return bot.add_cog(Role(bot))