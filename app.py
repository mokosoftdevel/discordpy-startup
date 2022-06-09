from flask import Flask
from discord.ext import commands
import discord
import os

bot = commands.Bot()
token = os.environ['DISCORD_BOT_TOKEN']
bot.run(token)


# web 
app = Flask(__name__)
@app.route('/')
async def web_main():
    channel = bot.get_channel(700201258929094778)
    await channel.send("uhihihi")
    return "hello world"

if __name__ == "__main__":
    app.run()


