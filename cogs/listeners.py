import disnake
from disnake.ext import commands

class Listeners(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot id: {self.bot.user.id}")



def setup(bot):
    bot.add_cog(Listeners(bot))
