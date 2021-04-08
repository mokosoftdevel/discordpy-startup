from discord.ext import commands
import os
import traceback
import random
import discord

bot = commands.Bot(command_prefix='うんこ')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    #await ctx.send(error_msg)

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.bot:
        return
    if message.content != 'うんこ' and message.content.startswith('うんこ'):
        return
    if message.content.endswith('うん'):
        await message.add_reaction('💩')
        await message.channel.send('こ')
        return
    if 'うんこ' in message.content:
        await message.add_reaction('💩')
        await message.channel.send('なに？')


@bot.command()
async def ヘルプ(ctx):
    await ctx.send("""うんこって誰 : わいが返事するで

うんこねむい : 眠気をはかるで

うんこどう : うんこの状態を教えるで

うんこmassa : Massaを罵倒するで
""")

@bot.command()
async def って誰(ctx):
    await ctx.send('わいや')


@bot.command()
async def ねむい(ctx):
    rand_int = random.randint(0,100)
    nemu_mes = ''
    if rand_int <= 5:
        nemu_mes = 'いやいや、きみめっちゃ目ぱっちりやん'
    if rand_int > 5 and rand_int <=15:
        nemu_mes = 'ねむそうには全然みえへんけど？'
    if rand_int > 15 and rand_int <= 30:
        nemu_mes = 'みんなねむいのは同じやから我慢し'
    if rand_int > 30 and rand_int <= 60:
        nemu_mes = 'この時間はねむなるよなぁ レッドブルきめよか！'
    if rand_int > 60 and rand_int <= 80:
        nemu_mes = '自分もう眠そうな顔してるで'
    if rand_int > 80 and rand_int <= 90:
        nemu_mes = 'いやもう寝たほうがいいでそろそろ'
    if rand_int > 90:
        nemu_mes = 'あかんあかん、もう寝ぇ！！！！'
    await ctx.send(f"{ctx.author.mention}"+' '+nemu_mes )


@bot.command()
async def どう(ctx):
    rand_int = random.randint(0,100)
    await ctx.send(f"{ctx.author.mention}"+' うんこのかんじは '+str(rand_int)+' やな' )


@bot.command()
async def massa(ctx):
    await ctx.send('<:Massa:761401088540672010> <:uruse:760475866626785342>')




bot.run(token)
