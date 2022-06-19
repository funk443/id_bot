"""
Copyright (C) 2022  CToID

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
    return pf["default"]["prefix"][1:-1]
  else:
    return pf[str (ctx.guild.id)]["prefix"]

bot = commands.Bot (command_prefix = get_prefix, intents = intents, activity = activity, help_command = None)

print ("id_bot  Copyright (C) 2022  CToID")
print ("This program comes with ABSOLUTELY NO WARRANTY.")
print ("This is free software, and you are welcome to redistribute it under certain conditions.")
print ("Check version 3 (or any later version) of GNU Affero General Public License for details.")

@bot.event
async def on_ready ():
  print ("UP")

@bot.command ()
async def change_prefix (ctx, npf = None):
  if (npf != None):
    pf[str (ctx.guild.id)]["prefix"] = npf
    await ctx.send (f"Prefix changed to {npf}")
  else:
    pf[str (ctx.guild.id)]["prefix"] = pf["default"]["prefix"][1:-1]
    await ctx.send ("沒給我東西那我就把他改回預設的了")

  with open ("prefix.ini", "w") as prefixfile:
    pf.write (prefixfile)

try:
  os.mkdir ("./datas")
except:
  pass

for fn in os.listdir ("./cogs"):
  if (fn.endswith (".py")):
    bot.load_extension (f"cogs.{fn[:-3]}")

if (__name__ == "__main__"):
  bot.run (str (config["tokens"]["discord_token"]))
