import discord
from discord.ext import commands
import asyncio


async def convert(ctx, argument):
    amount = argument[:-1]
    unit = argument[-1]

    if amount.isdigit() and unit in ['s', 'm', 'h']:
        return int(amount), unit

    raise commands.BadArgument(message="Not a valid duration")


class SessionTracker(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Session Tracker is loaded")

def setup(bot):
    bot.add_cog(SessionTracker(bot))
