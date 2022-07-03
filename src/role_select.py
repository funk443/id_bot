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

    if ((ctx.author != ctx.guild.owner)
        or (not ctx.author.permissions_in (ctx.channel).manage_roles)):
      await ctx.send ("還想皮")
      return

    try:
      with open (f"./datas/role_select/role_select_{ctx.guild.id}.json", encoding = "utf8") as msg_file:
        msgs = json.load (msg_file)
    except:
      with open (f"./datas/role_select/role_select_{ctx.guild.id}.json", "w", encoding = "utf8") as msg_file:
        json.dump ({}, msg_file, indent = 2)
      with open (f"./datas/role_select/role_select_{ctx.guild.id}.json", encoding = "utf8") as msg_file:
        msgs = json.load (msg_file)

    try:
      gcm = message_link.split ("/")[-3:]
    except:
      pass
    msg_id = int (gcm[-1])
    msgs[msg_id] = {}

    try:
      for i in roles_and_emojis:
        if (((len (i) == 1) and (emoji.is_emoji (i))) or (i[1] == ":")):
          msgs[msg_id][i] = []
          which_emoji = i
        elif ((i[0] == "<") and (i[1] == "@")):
          msgs[msg_id][which_emoji].append (i)
        else:
          await ctx.send ("好像打錯什麼了")
          return
    except:
      await ctx.send ("好像打錯什麼了")
      return

    with open (f"./datas/role_select/role_select_{ctx.guild.id}.json", "w", encoding = "utf8") as msg_file:
      json.dump (msgs, msg_file, indent = 2)

    msg = await ctx.fetch_message (msg_id)

    for i in msgs[msg_id].keys ():
      await msg.add_reaction (i)

    await ctx.message.delete ()

  @commands.Cog.listener ()
  async def on_raw_reaction_add (self, payload):

    if (payload.member.bot):
      return

    try:
      with open (f"./datas/role_select/role_select_{payload.guild_id}.json", encoding = "utf8") as role_select_file:
        data = json.load (role_select_file)
    except:
      return

    msg_id = str (payload.message_id)
    emoji = str (payload.emoji)

    if ((msg_id in data)
        and (emoji in data[msg_id])):
      guild = self.bot.get_guild (payload.guild_id)
      for i in data[msg_id][emoji]:
        role = guild.get_role (int (i[3:-1]))
        await payload.member.add_roles (role)

async def setup (bot):
  await bot.add_cog (role_selection (bot))
