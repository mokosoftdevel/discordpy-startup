from discord.ext import commands
import os
import traceback
import random

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('わいや')


@bot.command()
async def ねむい(ctx):
    rand_int = random.randint(0,100)
    await ctx.send(f"{ctx.author.mention}"+' 眠気は '+str(rand_int)+' やで' )


@bot.command()
async def roll(ctx):
    rand_int = random.randint(0,100)
    await ctx.send(f"{ctx.author.mention}"+' うんこのかんじは '+str(rand_int)+' やな' )


@bot.command()
async def massa(ctx):
    await ctx.send('<:Massa:761401088540672010> <:uruse:760475866626785342>')





bot.run(token)
