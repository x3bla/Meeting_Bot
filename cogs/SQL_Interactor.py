import discord
from discord.ext import commands
import asyncio

class SessionTracker(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("SQL Interactor is loaded")

def setup(bot):
    bot.add_cog(SessionTracker(bot))
