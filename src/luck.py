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

import discord, json, random, datetime
from discord.ext import commands

class daily_luck (commands.Cog):
  def __init__ (self, bot):
    self.bot = bot

  @commands.command ()
  async def 今日運勢 (self, ctx):
    lucks = ("大凶", "凶", "小凶", "平", "小吉", "吉", "大吉", "你命由你不由天，自己幸福自己拼", "在吉跟不吉之間")

    try:
      with open ("./datas/luck.json", encoding = "utf8") as luck_file:
        records = json.load (luck_file)
    except:
      with open ("./datas/luck.json", "w", encoding = "utf8") as luck_file:
        json.dump ({}, luck_file, indent = 2, ensure_ascii = False)
      with open ("./datas/luck.json", encoding = "utf8") as luck_file:
        records = json.load (luck_file)

    shift = datetime.timedelta (hours = 8)

    # if (str (ctx.author.id) not in records):
    #   today_luck = random.choice (lucks)
    #   await ctx.reply (today_luck)
    #   records[str (ctx.author.id)] = [(ctx.message.created_at + shift).date ().isoformat (), today_luck]
    #   with open ("./datas/luck.json", "w", encoding = "utf8") as luck_file:
    #     json.dump (records, luck_file, indent = 2, ensure_ascii = False)
    #   return

    if ((str (ctx.author.id) not in records)
        or (datetime.date.fromisoformat (records[str (ctx.author.id)][0]) < datetime.date.today ())):
      today_luck = random.choice (lucks)
      await ctx.reply (today_luck)
      records[str (ctx.author.id)] = [(ctx.message.created_at + shift).date ().isoformat (), today_luck]
      with open ("./datas/luck.json", "w", encoding = "utf8") as luck_file:
        json.dump (records, luck_file, indent = 2, ensure_ascii = False)
    else:
      await ctx.reply (f"啊不就跟你說今天是 {records[str (ctx.author.id)][1]} 了")

def setup (bot):
  bot.add_cog (daily_luck (bot))
