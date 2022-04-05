from discord.ext import commands
import datetime
import config

config = config.config()

def checks(ctx):
    return ctx.message.author.id == 895821363749732352

class Ticket(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    # ticket関連リアクション
    @commands.Cog.listener(name='on_raw_reaction_add')
    async def create_ticket(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        if payload.emoji.name == '📧':
            if payload.message_id == int(config.read('ticket', 'create_ticket_massage_id')):
                user = await self.bot.fetch_user(user_id=payload.user_id)
                ticket_id = str(int(config.read('ticket','last_ticket_id')) + 1)
                active_ticket_cat = await self.bot.fetch_channel(config.read('ticket', 'active_ticket_category_id'))
                today_str = datetime.date.today().strftime("%m-%d")
                ticket_ch = await active_ticket_cat.create_text_channel(name=f"ticket_{ticket_id}［{today_str}］")
                config.write("ticket", "last_ticket_id", ticket_id)
                await ticket_ch.set_permissions(user, read_messages=True, send_messages=True, read_message_history=True)
                created_msg = await ticket_ch.send(f'{user.mention}さんのチケットを作成しました。\nチケットを閉じる場合は、✖を押してください。')
                await created_msg.add_reaction('✖')
                return
    
        elif payload.emoji.name == '✖':
            on_reaction_ch = await self.bot.fetch_channel(payload.channel_id)
            if on_reaction_ch.category_id == int(config.read('ticket', 'active_ticket_category_id')):
                archived_ticket_cat = await self.bot.fetch_channel(config.read('ticket', 'archived_ticket_category_id'))
                await on_reaction_ch.edit(category=archived_ticket_cat, sync_permissions=True)
                msg = await on_reaction_ch.send("チケットを閉じました。\nチケットを削除する場合には、:x:を押してください。")
                await msg.add_reaction('❌')
            return
        
        elif payload.emoji.name == "❌":
            ch = await self.bot.fetch_channel(payload.channel_id)
            print(ch.category_id)
            if ch.category_id == int(config.read('ticket', 'archived_ticket_category_id')):
                await ch.delete()
                return
        return


    #手動でチケットを作成
    @commands.command()
    @commands.check(checks)
    async def ticket(self, ctx, user_id):
        ticket_id = int(config.read('ticket', 'last_ticket_id')) + 1
        config.write('ticket', 'last_ticket_id', str(ticket_id))
        today = datetime.date.today()
        u = await self.bot.fetch_user(user_id)
        cat = await self.bot.fetch_channel(config.read('ticket', 'active_ticket_category_id'))
        ticket_ch = await cat.create_text_channel(name=f"ticket_{ticket_id}［{today.month}-{today.day}］")
        await ticket_ch.set_permissions(u, read_messages=True, send_messages=True, read_message_history=True)
        m = await ticket_ch.send(f'{u.mention}さんのチケットを作成しました。\nチケットを閉じる場合は、✖を押してください。')
        await m.add_reaction('✖')

def setup(bot):
    return bot.add_cog(Ticket(bot))
