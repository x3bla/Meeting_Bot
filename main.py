import os
import discord
from discord.ext import commands, tasks
from itertools import cycle
import traceback
import sys

# variables
operator = [262505750922919937, 807215269403426848]

def operators(ctx):
    global operator
    if ctx.author.id in operator:
        return True
    else:
        print(f"{ctx.author} attempted to perform a load action\n")
        return False


# cycling through statuses
status = cycle(["Propaganda Campaign", "Nothing happened at tian men square", "Glory to the CCP"])

# setting prefix and making commands case insensitive
bot = commands.Bot(command_prefix='ccp!', case_insensitive=True)


# status changes
@tasks.loop(minutes=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


# basic commands
@bot.event
async def on_ready():
    change_status.start()
    print("Bot is ready.")

@bot.event
async def on_member_join(member):
    print(f'{member} has joined a server.')
    # TODO: add to MySQL

@bot.event
async def on_member_remove(member):
    print(f'{member} has left a server')
    # TODO: remove from MySQL

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        print(f"{ctx.author} tried to use a command without proper perms")
        pass
    else:
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! \n{bot.latency * 1000}ms")

# loading/unloading listeners
@bot.command()
@commands.check(operators)
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    print(f"{ctx.author} has performed an admin action\n")

@bot.command()
@commands.check(operators)
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    print(f"{ctx.author} has performed an admin action")
    print(f"{extension} has been unloaded\n")

@bot.command()
@commands.check(operators)
async def reload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    print(f"{ctx.author} has performed an admin action")
    print(f"{extension} has been reloaded\n")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run("")
