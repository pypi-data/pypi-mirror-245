import discord
from discord.ext import commands
from discord.utils import get

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
user_id = 797156297396453396


@bot.event
async def on_ready():
    user = bot.get_user(user_id)
    await user.send("Го в танки")
    # await bot.close()
    exit(f"Sent message to {user.name} with text 'Го в танки'")


def main(_user_id):
    global user_id
    user_id = _user_id
    bot.run("MTE4MjgyMzYwMDc2ODY4ODE4OA.GVO3aq.0PwnIVxVX0MeRSDI0X3SQLDlX6mGXQEb5V9Zws")
