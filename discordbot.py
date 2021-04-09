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
    if 'くそ' in message.content or 'クソ' in message.content:
        await message.add_reaction('💩')
        await message.channel.send('なんや？')
    if 'くさい' in message.content or '臭い' in message.content:
        await message.channel.send('臭いのわいちゃうで？')


@bot.command()
async def ヘルプ(ctx):
    await ctx.send("""うんこって誰 : わいが返事するで

うんこねむい : 眠気をはかるで

うんこどう？ : うんこの状態を教えるで

うんこmassa : Massaを罵倒するで

うんこ何食べよ : 食べるものを提案するよ

うんこおはよう : 占い
""")

@bot.command(aliases=['だれ','だれ？','誰','誰？'])
async def com_dare(ctx):
    await ctx.send('わいや')


@bot.command(aliases=['ねむい','眠い'])
async def com_nemui(ctx):
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
    await ctx.send(f"{ctx.author.mention}"+' '+nemu_mes+' ('+str(rand_int)+')' )


@bot.command(aliases=['どう？','どう'])
async def ping(ctx):
    rand_int = random.randint(0,100)
    await ctx.send(f"{ctx.author.mention}"+' うんこのかんじは '+str(rand_int)+' やな' )


@bot.command(aliases=['massa','Massa','まっさ'])
async def com_massa(ctx):
    await ctx.send('<:Massa:761401088540672010> <:uruse:760475866626785342>')


@bot.command(aliases=['何食べよ','何食べよ？'])
async def com_tabeyo(ctx):
    rand_int = random.randint(1,10)
    mes = ''
    if rand_int == 1:
        mes = 'んーーそやな、パスタとかどう？'
    if rand_int == 2:
        mes = '今日はあれやで、中華やろ'
    if rand_int == 3:
        mes = 'ここは一発焼肉で！'
    if rand_int == 4:
        mes = 'なんちゅうか、パン食いたくない？'
    if rand_int == 5:
        mes = 'ピッツァ'
    if rand_int == 6:
        mes = 'やっぱ和食よねっ'
    if rand_int == 7:
        mes = 'ラーメンいっとこ！'
    if rand_int == 8:
        mes = '食べたらあかん'
    if rand_int == 9:
        mes = 'スープ　スープだけ'
    if rand_int == 10:
        mes = 'コンビニでええんちゃう'
    await ctx.send(f"{ctx.author.mention}"+' '+mes)


@bot.command(aliases=['おはよう'])
async def com_ohayo(ctx):
    rand_int = random.randint(1,5)
    mes = ''
    if rand_int == 1:
        mes = 'おはよー　あんさん今日は"うん"がありまっせ'
    if rand_int == 2:
        mes = 'おはようさん　今日はくっさい一日ですわ'
    if rand_int == 3:
        mes = '朝からなんや、ため息が"もれとる"で'
    if rand_int == 4:
        mes = 'すごい！うんこだけに"大"吉やっ！！！'
    if rand_int == 5:
        mes = 'お前は普通'
    await ctx.send(f"{ctx.author.mention}"+' '+mes)



bot.run(token)
