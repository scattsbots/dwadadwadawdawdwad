from discord.ext import commands
from lxml import html
from difflib import SequenceMatcher
import subprocess
import threading
import aiofiles
import discord
import asyncio
import aiohttp
import random
import ctypes
import re
import os

ctypes.windll.kernel32.SetConsoleTitleW('Scatts')
token = 'ODYxNjM1ODgyNjk2NDQxODU2.YOMq8g.a6CDowcFqN8eB4nuN2yhe-Fm3h4'
prefix = '/'

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=intents)
bot.remove_command('help')

administrators = []
chat_channel = 862536230678953984
bots_channel = 862536230678953984

queue = []

def followsv2():
    while True:
        try:
            task, arg1, arg2 = queue.pop(0).split('-')
            subprocess.run([f'{task}', f'{arg1}', f'{arg2}'])
        except:
            pass

threading.Thread(target=followsv2).start()

@bot.event
async def on_member_join(member):
    channel = await bot.fetch_channel(bots_channel)
    await channel.send(f'Welcome to **Twitch Followers v2**, {member.mention}.\nType `/help` to get started!')

@bot.event
async def on_command_error(ctx, error: Exception):
    if ctx.channel.id == bots_channel:
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(color=1376511, description=f'{error}')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(color=1376511, description='You are missing arguments required to run this command!')
            await ctx.send(embed=embed)
            ctx.command.reset_cooldown(ctx)
        elif 'You do not own this bot.' in str(error):
            embed = discord.Embed(color=1376511, description='You do not have permission to run this command!')
            await ctx.send(embed=embed)
        else:
            print(str(error))
    else:
        try:
            await ctx.message.delete()
        except:
            pass

@bot.command()
async def help(ctx):
    if ctx.channel.type != discord.ChannelType.private:
        embed = discord.Embed(color=1376511)
        
        embed.add_field(name='1 | Twitch Followers', value='`/tfollow (channel)`', inline=True)
        embed.add_field(name='2 | Twitch Spam', value='`/tspam (channel) (message)`', inline=True)
        embed.set_author(name=f'{ctx.guild.name} | Commands')
        await ctx.channel.send(embed=embed)

tfollow_cooldown = []

@bot.command()
@commands.cooldown(1, 120, type=commands.BucketType.user)
async def tfollow(ctx, channel, amount: int=None):
    if ctx.channel.type != discord.ChannelType.private:
        if ctx.channel.id == bots_channel or ctx.author.id in administrators:
            try:
                if '-' in str(channel):
                    raise Exception
                if str(channel).lower() in blacklisted and ctx.author.id not in administrators:
                    embed = discord.Embed(color=16379747, description=f"**{channel}** is blacklisted")
                    await ctx.channel.send(embed=embed)
                    return
                max_amount = 0
                if ctx.author.id in administrators:
                    tfollow.reset_cooldown(ctx)
                    max_amount += 10000
                premium = discord.utils.get(ctx.guild.roles, name='861637488522297365')
                if premium in ctx.author.roles:
                    max_amount += 10000
                default = discord.utils.get(ctx.guild.roles, name='861637619439632405')
                if default in ctx.author.roles:
                    max_amount += 50
                max_amount += 100
                if amount is None:
                    amount = max_amount
                elif amount > max_amount:
                    amount = max_amount
                if amount <= max_amount:
                    position = len(queue) + 1
                    embed = discord.Embed(color=1376511, description=f'Sending **{amount}** followers to **{channel}** 🔥')
                    await ctx.send(embed=embed)
                    queue.append(f'tfollow-{channel}-{amount}')
            except:
                embed = discord.Embed(color=1376511, description='An error has occured while attempting to run this command')
                await ctx.send(embed=embed)
                tfollow.reset_cooldown(ctx)
        else:
            await ctx.message.delete()
            tfollow.reset_cooldown(ctx)


_delay = 600

@bot.command()
async def delay(ctx, seconds):
    if ctx.channel.type != discord.ChannelType.private:
        if ctx.author.id in administrators:
            global _delay
            _delay = int(seconds)
            embed = discord.Embed(color=1376511, description=f'Set trivia delay to **{seconds}** seconds!')
            await ctx.send(embed=embed)
        else:
            await ctx.message.delete()

@bot.command()
@commands.cooldown(1, 600, type=commands.BucketType.user)
async def tspam(ctx, channel, *, msg):
    if ctx.channel.type != discord.ChannelType.private:
        if discord.utils.get(ctx.guild.roles, name='Premium') in ctx.author.roles or discord.utils.get(ctx.guild.roles, name='Premium +') in ctx.author.roles or ctx.author.id in administrators:
            if ctx.channel.id == bots_channel or ctx.author.id in administrators:
                try:
                    max_amount = 0
                    if ctx.author.id in administrators:
                        tspam.reset_cooldown(ctx)
                        max_amount += 48
                    max_amount += 5
                    amount = None
                    if amount is None:
                        amount = max_amount
                    if amount <= max_amount:
                        position = len(queue) + 1
                        embed = discord.Embed(color=1376511, description=f'Spamming **{channel}** with **{msg}** :zap:')
                        await ctx.send(embed=embed)
                        queue.insert(0, f'tspam-{channel}-{msg}')
                except:
                    embed = discord.Embed(color=16379747, description='An error has occured while attempting to run this command!')
                    await ctx.send(embed=embed)
                    tspam.reset_cooldown(ctx)
            else:
                await ctx.message.delete()
                tspam.reset_cooldown(ctx)
        else:
            embed = discord.Embed(color=1376511, description='Only **Premium** can use this!')
            await ctx.send(embed=embed)

bot.run("ODYxNjM1ODgyNjk2NDQxODU2.YOMq8g.a6CDowcFqN8eB4nuN2yhe-Fm3h4")
