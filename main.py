import discord
from discord.ext import commands
from discord import app_commands
import re
# Importing essentials

def setup():
    try:
        x = open("data.log", "rt")
        x = x.read()
        y = []
        z = ""
        for i in range(0, len(x) - 1):
            if x.read()[i] == "\n":
                y.append(z)
            else:
                z = z + x[i]
        return y
    except Exception as e:
        print(e)
        x = open("data.log", "wt")
        x.write("")
        setup()
    
    
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
global channels
channels = setup()
# Setting the bot up

@bot.event
async def on_ready():
    try:
        print(f"Logged in as user {bot.user}")
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)!")
    
    except Exception as e:
        print(e)
# Testing the bot        

@bot.tree.command(name="about")
async def about(ctx: discord.Interaction):
    await ctx.response.send_message("# Link deleter [BOT]\n# About\n**Invite link**: https://discord.com/oauth2/authorize?client_id=1278686272390434946&permissions=1099511639040&integration_type=0&scope=bot\n**Developer**: PaintCraft53\n# Commands\n**'/applyrule [channel_id]'**: If applyed, every link sent on this channel will deleted.\n**'/removerule [channel_id]'**: Removes the rule from the channel.\n**'/about'**: Shows instructions for the bot.")

@bot.tree.command(name="save")
async def save(ctx: discord.Interaction):
    x = ""
    for c in channels:
        x = x + c + "\n"
    y = open("data.log", "wt")
    y.write(x)
    print(x)
    y.close()
    await ctx.response.send_message("Data saved.")

@bot.tree.command(name="applyrule")
@app_commands.describe(channel="Channel ID")
async def applyrule(ctx: discord.Interaction, channel: str):
    dont = False
    for c in channels:
        if c == channel:
            dont = True
    
    if dont:
        await ctx.response.send_message("The rule is already applied for this channel!")
    else:
        channels.append(channel)
        await ctx.response.send_message(f"Applyed rule for channel {channel}")

@bot.tree.command(name="removerule")
@app_commands.describe(channel="for channel")
async def removerule(ctx: discord.Interaction, channel: str):
    try:
        channels.remove(channel)
        await ctx.response.send_message(f"Raemoved rule for channel {channel}")
    except:
        await ctx.response.send_message(f"Can't remove the rule for channel {channel}")

# Settung up the slash command    
    
@bot.event
async def on_message(ctx: discord.Interaction):
    url_pattern = re.compile(r'(https?://[^\s]+)')
    for c in channels:

        if int(c) == ctx.channel.id and url_pattern.findall(ctx.content):
            await ctx.channel.purge(limit=1)

bot.run("MTI3ODY4NjI3MjM5MDQzNDk0Ng.Gr-YPo.5hpvEWbQjteQ11m7jHIUB5MvsgqSDKyUn2D1Qc")
# Running the bot