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

import discord, json, os, emoji
from discord.ext import commands

class role_selection (commands.Cog):
  def __init__ (self, bot):
    self.bot = bot

  @commands.command ()
  async def role_select (self, ctx, message_link, *roles_and_emojis):

    if (ctx.author != ctx.guild.owner):
      await ctx.send ("還想皮")
      return

    try:
      with open (f"./datas/role_select/role_select_{ctx.guild.id}.json") as msg_file:
        msgs = json.load (msg_file)
    except:
      with open (f"./datas/role_select/role_select_{ctx.guild.id}.json", "w") as msg_file:
        json.dump ({}, msg_file, indent = 2)
      with open (f"./datas/role_select/role_select_{ctx.guild.id}.json") as msg_file:
        msgs = json.load (msg_file)

    msgs[message_link] = {}

    try:
      for i in roles_and_emojis:
        if (((len (i) == 1) and (emoji.is_emoji (i))) or (i[1] == ":")):
          msgs[message_link][i] = []
          which_emoji = i
        elif ((i[0] == "<") and (i[1] == "@")):
          msgs[message_link][which_emoji].append (i)
        else:
          await ctx.send ("好像打錯什麼了")
          return
    except:
      await ctx.send ("好像打錯什麼了")
      return

    with open (f"./datas/role_select/role_select_{ctx.guild.id}.json", "w") as msg_file:
      json.dump (msgs, msg_file, indent = 2)

    try:
      gcm = message_link.split ("/")[-3:]
    except:
      pass
    msg_id = int (gcm[-1])

    msg = await ctx.fetch_message (msg_id)

    for i in msgs[message_link].keys ():
      await msg.add_reaction (i)

    await ctx.message.delete ()

def setup (bot):
  bot.add_cog (role_selection (bot))
