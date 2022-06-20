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

import discord, json, os, configparser
from discord.ext import commands

class reply (commands.Cog):
  def __init__ (self, bot):
    self.bot = bot

  @commands.command ()
  async def reply (self, ctx, key, content_1 = None, content_2 = None):

    try:
      with open (f"./datas/reply/reply_{ctx.guild.id}.json") as reply_file:
        rp = json.load (reply_file)
    except:
      with open (f"./datas/reply/reply_{ctx.guild.id}.json", "w") as reply_file:
        json.dump ({}, reply_file)

    if (key == "add"):
      if ((content_1 == None)
          or ((content_2 == None) and (len (ctx.message.attachments) == 0))):
        await ctx.send ("你什麼都沒有給我是要加什麼啦")
      elif (len (ctx.message.attachments) != 0):
        rp[content_1] = ctx.message.attachments
      else:
        rp[content_1] = content_2

    elif (key == "del"):
      if (content_1 == None):
        await ctx.send ("你什麼都沒有給我是要刪空氣喔")
      else:
        try:
          rp.pop (content_1)
        except:
          await ctx.send ("本來就沒有的東西我要怎麼刪")

    elif (key == "list"):
      await ctx.send (file = discord.File (f"./datas/reply/reply_{ctx.guild.id}.json"))

    else:
      return

    with open (f"./datas/reply/reply_{ctx.guild.id}.json", "w") as reply_file:
      json.dump (rp, reply_file, indent = 2)

def setup (bot):
  bot.add_cog (reply (bot))
