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

import discord, json, os
from discord.ext import commands

class events (commands.Cog):
  def __init__ (self, bot):
    self.bot = bot

  @commands.Cog.listener ()
  async def on_message (self, message):

    if ((message.author == self.bot.user) or (message.author.bot)):
      return

    if (f"reply_{message.guild.id}.json" not in os.listdir ("./datas/reply")):
      return
    else:
      with open (f"./datas/reply/reply_{message.guild.id}.json", encoding = "utf8") as reply_file:
        rp = json.load (reply_file)

    if (message.content in rp):
      if (type (rp[message.content]) == list):
        for i in rp[message.content]:
          await message.channel.send (i)
      else:
        await message.channel.send (rp[message.content])

async def setup (bot):
  await bot.add_cog (events (bot))
