"""
Copyright (C) 2022 CToID

This file is part of id_bot

id_bot is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

id_bot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import discord, configparser, os
from discord.ext import commands

intents = discord.Intents.all ()

activity = discord.Game (name = "GNU Emacs")

config = configparser.ConfigParser ()
config.read ("config.ini")

pf = configparser.ConfigParser ()
pf.read ("prefix.ini")

async def get_prefix (bot, ctx):
  if (str (ctx.guild.id) not in pf):
    return pf["prefix"]["default"]
  else:
    return pf["prefix"][str (ctx.guild.id)]

bot = commands.Bot (command_prefix = get_prefix, intents = intents, activity = activity, help_command = None)

@bot.event
async def on_ready ():
  print ("UP")

@bot.command ()
async def change_prefix (ctx, npf = None):
  if (npf != None):
    pf["prefix"][str (ctx.guild.id)] = npf
    await ctx.send (f"Prefix changed to {npf}")
  else:
    pf["prefix"][str (ctx.guild.id)] = pf["prefix"]["default"]
    await ctx.send ("沒給我東西那我就把他改回預設的了")

  with open ("prefix.ini", "w") as prefixfile:
    pf.write (prefixfile)

for fn in os.listdir ("./cogs"):
  if (fn.endswith (".py")):
    bot.load_extension (f"cogs.{fn[:-3]}")

if (__name__ == "__main__"):
  bot.run (str (config["tokens"]["discord_token"]))
