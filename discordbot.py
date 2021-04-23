from discord.ext import commands
import os
import traceback
import random
import discord
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials 

bot = commands.Bot(command_prefix='うんこ')
token = os.environ['DISCORD_BOT_TOKEN']


# うんこの受け答えlist
unko_messages = []

# ねむいlist
unko_nemui = []





# google spread sheet api 
sheet = os.environ['SHEETKEY']
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']    
credential = {
                "type": "service_account",
                "project_id": os.environ['SHEET_PROJECT_ID'],
                "private_key_id": os.environ['SHEET_PRIVATE_KEY_ID'],
                "private_key": os.environ['SHEET_PRIVATE_KEY'].replace('\\n', '\n'),
                "client_email": os.environ['SHEET_CLIENT_EMAIL'],
                "client_id": os.environ['SHEET_CLIENT_ID'],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url":  os.environ['SHEET_CLIENT_X509_CERT_URL']
             }
# print(credential)
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credential, scope)
gc = gspread.authorize(credentials)
wb = gc.open_by_key(sheet)
sheet_messages = wb.worksheet('messages')
sheet_uranai = wb.worksheet('uranai')



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
    global unko_messages
    for line in unko_messages:
        if line[0] == 'end':
            if message.content.endswith(line[1]):
                if int(line[3]) == 1:
                    await message.add_reaction(line[4])
                if len(line[2]) > 0:
                    await message.channel.send(line[2])
                return
        elif line[0] == 'find':
            if line[1] in message.content:
                if int(line[3]) == 1:
                    await message.add_reaction(line[4])
                if len(line[2]) > 0:
                    await message.channel.send(line[2])
                return
        


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
    global unko_nemui
    for line in unko_nemui:
        if int(line[0]) <= rand_int and rand_int <= int(line[1]):
            nemu_mes = line[2]
            break
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


@bot.command(aliases=['お知らせ'])
async def com_osirase(ctx):
    await ctx.send('@everyone はいはいみんな '+f"{ctx.author.mention}"+' が言いたいことがあるらしいで、ちょっと静かにしたってな、はいどうぞ')


@bot.command(aliases=['りろーど','リロード'])
async def com_reload(ctx):
    await ctx.send('読み込みます')
    await func_get_unko_message_spreadsheet()
    await func_get_unko_nemui_spreadsheet()
    global unko_messages
    print(unko_messages)
    await ctx.send('読み込みました')



async def func_get_unko_message_localhost():
    global unko_messages
    unko_messages.clear()
    unko_messages.append(['end','うん','こ',1,'💩'])
    unko_messages.append(['find','うんこ','なに？',1,'💩'])
    unko_messages.append(['find','くそ','なんや？',1,'💢'])
    print(unko_messages)

async def func_get_unko_message_spreadsheet():
    global unko_messages
    unko_messages.clear()
    last_line = int(sheet_messages.cell(1,2).value)
    print(last_line)
    column_size = 5
    ranges = sheet_messages.range(3,1,last_line,column_size)
    for start in range(0, len(ranges), column_size):
        values = []
        for vcell in ranges[start : start + column_size]:
            values.append(vcell.value)
        unko_messages.append(values)

async def func_get_unko_nemui_spreadsheet():
    global unko_nemui
    unko_nemui.clear()
    last_line = int(sheet_uranai.cell(1,2).value)
    column_size = 3
    ranges = sheet_uranai.range(3,1,last_line,column_size)
    for start in range(0, len(ranges), column_size):
        values = []
        for vcell in ranges[start : start + column_size]:
            values.append(vcell.value)
        unko_nemui.append(values)
    

    








# spreadsheet から設定を読み込む
bot.loop.create_task(func_get_unko_message_spreadsheet())
bot.loop.create_task(func_get_unko_nemui_spreadsheet())

bot.run(token)
