from discord.ext import commands
import os
import traceback
import random
import discord
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials 
from datetime import datetime,timedelta,timezone
from discord.ext import tasks
import numpy as np

bot = commands.Bot(command_prefix='うんこ')
token = os.environ['DISCORD_BOT_TOKEN']


# うんこの受け答えlist
unko_messages = []

# ねむいlist
unko_nemui = []

# おはよう
unko_ohayo = []

# massa
unko_massa = []

# 食べよ
unko_tabeyo = []

# schedule
unko_schedule = []

# slot list
unko_slot = []



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
sheet_ohayou = wb.worksheet('ohayou')
sheet_massa = wb.worksheet('massa')
sheet_tabeyo = wb.worksheet('tabeyo')
sheet_schedule = wb.worksheet('schedule')
sheet_slot = wb.worksheet('slot')

bot_channel_id = 738973128645935104
JST = timezone(timedelta(hours=+9), 'JS')


@tasks.loop(seconds=60)
async def loop():
    now = datetime.now(JST).strftime('%H:%M')
    # print(now)
    for line in unko_schedule:
        if now == line[0]:
            channel = bot.get_channel(int(line[1]))
            await channel.send(line[2])
        if now == "00:00": 
            await func_all_reload()

loop.start()


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
    global unko_massa
    mes = random.choice(unko_massa)
    await ctx.send(mes)


@bot.command(aliases=['何食べよ','何食べよ？'])
async def com_tabeyo(ctx):
    global unko_tabeyo
    mes = random.choice(unko_tabeyo)
    await ctx.send(f"{ctx.author.mention}"+' '+mes)


@bot.command(aliases=['スロット','すろっと'])
async def com_slot(ctx):
    global unko_slot
    mes1 = random.choice(unko_slot)
    mes2 = random.choice(unko_slot)
    mes3 = random.choice(unko_slot)
    await ctx.send(mes1+mes2+mes3)

@bot.command(aliases=['スロット３連','すろっと３連'])
async def com_slot7(ctx):
    global unko_slot

    dice = list()
    for x in range(1,8):
        for y in range(1,8):
            for z in range(1,8):
                dice.append(100*x+10*y*z)
    print(dice)

    prob = list()
    for i in range(343):
        if dice[i] == 111:
            prob.append(0.00045)
        elif dice[i] == 222:
            prob.append(0.00045)
        elif dice[i] == 333:
            prob.append(0.00045)
        elif dice[i] == 444:
            prob.append(0.00045)
        elif dice[i] == 555:
            prob.append(0.00045)
        elif dice[i] == 666:
            prob.append(0.00045)
        elif dice[i] == 777:
            prob.append(0.00045)
        else:
            prob.append(0.99685/336)

    samples = np.random.choice(a=dice,size=3,p=prob)
    print(samples)

    for item in samples:
        num = []
        n = item
        while n != 0:
            num.append(n % 10)
            n /= 10
        num.reverse()
        print(num)
        mes = unko_slot[num[0]]+unko_slot[num[1]]+unko_slot[num[2]]
        await ctx.send(mes)


    #mes1 = random.choice(unko_slot)
    #mes2 = random.choice(unko_slot)
    #mes3 = random.choice(unko_slot)
    #await ctx.send(mes1+mes2+mes3)
    #mes1 = random.choice(unko_slot)
    #mes2 = random.choice(unko_slot)
    #mes3 = random.choice(unko_slot)
    #await ctx.send(mes1+mes2+mes3)
    #mes1 = random.choice(unko_slot)
    #mes2 = random.choice(unko_slot)
    #mes3 = random.choice(unko_slot)
    #await ctx.send(mes1+mes2+mes3)

    

@bot.command(aliases=['おはよう'])
async def com_ohayo(ctx):
    global unko_ohayo
    mes = random.choice(unko_ohayo)
    await ctx.send(f"{ctx.author.mention}"+' '+mes)


@bot.command(aliases=['お知らせ'])
async def com_osirase(ctx):
    await ctx.send('@everyone はいはいみんな '+f"{ctx.author.mention}"+' が言いたいことがあるらしいで、ちょっと静かにしたってな、はいどうぞ')


@bot.command(aliases=['りろーど','リロード'])
async def com_reload(ctx):
    await ctx.send('読み込むでー')
    await func_all_reload()
    await ctx.send('読み込みんだで！おおきに！')


async def func_all_reload():
    await func_get_unko_message_spreadsheet()
    await func_get_unko_nemui_spreadsheet()
    await func_get_unko_ohayo_spreadsheet()
    await func_get_unko_massa_spreadsheet()
    await func_get_unko_tabeyo_spreadsheet()
    await func_get_unko_schedule_spreadsheet()
    await func_get_unko_slot_spreadsheet()


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

async def func_get_unko_ohayo_spreadsheet():
    global unko_ohayo
    unko_ohayo.clear()
    last_line = int(sheet_ohayou.cell(1,2).value)
    ranges = sheet_ohayou.range(3,1,last_line,1)
    for vcell in ranges:
        unko_ohayo.append(vcell.value)

async def func_get_unko_massa_spreadsheet():
    global unko_massa
    unko_massa.clear()
    last_line = int(sheet_massa.cell(1,2).value)
    ranges = sheet_massa.range(3,1,last_line,1)
    for vcell in ranges:
        unko_massa.append(vcell.value)

async def func_get_unko_tabeyo_spreadsheet():
    global unko_tabeyo
    unko_tabeyo.clear()
    last_line = int(sheet_tabeyo.cell(1,2).value)
    ranges = sheet_tabeyo.range(3,1,last_line,1)
    for vcell in ranges:
        unko_tabeyo.append(vcell.value)

async def func_get_unko_schedule_spreadsheet():
    global unko_schedule
    unko_schedule.clear()
    last_line = int(sheet_schedule.cell(1,2).value)
    column_size = 3
    ranges = sheet_schedule.range(3,1,last_line,column_size)
    for start in range(0, len(ranges), column_size):
        values = []
        for vcell in ranges[start : start + column_size]:
            values.append(vcell.value)
        unko_schedule.append(values)

async def func_get_unko_slot_spreadsheet():
    global unko_slot
    unko_slot.clear()
    last_line = int(sheet_slot.cell(1,2).value)
    ranges = sheet_slot.range(3,1,last_line,1)
    for vcell in ranges:
        unko_slot.append(vcell.value)







# spreadsheet から設定を読み込む
bot.loop.create_task(func_get_unko_message_spreadsheet())
bot.loop.create_task(func_get_unko_nemui_spreadsheet())
bot.loop.create_task(func_get_unko_ohayo_spreadsheet())
bot.loop.create_task(func_get_unko_massa_spreadsheet())
bot.loop.create_task(func_get_unko_tabeyo_spreadsheet())
bot.loop.create_task(func_get_unko_schedule_spreadsheet())
bot.loop.create_task(func_get_unko_slot_spreadsheet())

bot.run(token)
