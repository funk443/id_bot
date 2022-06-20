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

import discord, configparser, os, json
from discord.ext import commands

intents = discord.Intents.all ()

activity = discord.Game (name = "GNU Emacs")

config = configparser.ConfigParser ()
config.read ("config.ini")

if ("prefix.json" not in os.listdir ()):
  with open ("./prefix.json", "w") as json_file:
    json.dump ({"default": "id "}, json_file, indent = 2)

with open ("./prefix.json", "r") as json_file:
  prefix = json.load (json_file)

async def get_prefix (bot, ctx):
  with open ("./prefix.json", "r") as json_file:
    prefix = json.load (json_file)
  try:
    return prefix[str (ctx.guild.id)]
  except:
    return prefix["default"]

bot = commands.Bot (command_prefix = get_prefix, intents = intents, activity = activity, help_command = None)

print ("id_bot  Copyright (C) 2022  CToID")
print ("This program comes with ABSOLUTELY NO WARRANTY.")
print ("This program is free software, and you are welcome to redistribute it under certain conditions.")
print ("Check version 3 (or any later version) of GNU Affero General Public License for details.")

@bot.event
async def on_ready ():
  print ("UP")

@bot.command ()
async def change_prefix (ctx, npf = None):
  if (npf != None):
    prefix[str (ctx.guild.id)] = npf
    await ctx.send (f"改成 `{npf}`")
  else:
    prefix[str (ctx.guild.id)] = prefix["default"]
    await ctx.send ("改回預設引導詞")

  with open ("./prefix.json", "w") as json_file:
    json.dump (prefix, json_file, indent = 2)

try:
  os.mkdir ("./datas")
except:
  pass

try:
  os.mkdir ("./datas/reply")
except:
  pass

try:
  os.mkdir ("./datas/role_select")
except:
  pass

for fn in os.listdir ("./src"):
  if (fn.endswith (".py")):
    bot.load_extension (f"src.{fn[:-3]}")

if (__name__ == "__main__"):
  bot.run (str (config["tokens"]["discord_token"]))
