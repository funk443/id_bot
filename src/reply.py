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

import discord, json, os, asyncio, math
from discord import ui
from discord.ext import commands

class reply (commands.Cog):
  def __init__ (self, bot):
    self.bot = bot

  async def reply_pages (self, ctx, list_rp):
    list_rp = list (list_rp.items ())
    per_page = 10
    pages = math.ceil (len (list_rp) / per_page)
    cur_page = 1
    pages_index = {}
    pages_embeds = {}

    for i in range (pages):
      pages_index[f"page_{i + 1}"] = list_rp[i * 10:(i + 1) * 10]

    pages_index = list (pages_index.items ())

    for i in range (pages):
      pages_embeds[f"page_{i + 1}"] = discord.Embed (title = f"Page {i + 1} / {pages}")
      for j in range (len (pages_index[i][1])):
        name = pages_index[i][1][j][0]
        value = pages_index[i][1][j][1]
        pages_embeds[f"page_{i + 1}"].add_field (name = name, value = f"╰ {value}", inline = False)

    def create_view (n_but, p_but):
      view = ui.View ()
      n_button = ui.Button (label = "Next Page", disabled = n_but)
      p_button = ui.Button (label = "Previous Page", disabled = p_but)
      n_button.callback = next_page 
      p_button.callback = previous_page 
      view.add_item (p_button)
      view.add_item (n_button)
      return view

    async def next_page (interactive):
      await interactive.response.defer ()
      nonlocal cur_page
      if (cur_page != pages):
        cur_page += 1
        await msg.edit (embed = pages_embeds[f"page_{cur_page}"], view = create_view (False, False))
        if (cur_page == pages):
          await msg.edit (embed = pages_embeds[f"page_{cur_page}"], view = create_view (True, False))

    async def previous_page (interactive):
      await interactive.response.defer ()
      nonlocal cur_page
      if (cur_page > 1):
        cur_page -= 1
        await msg.edit (embed = pages_embeds[f"page_{cur_page}"], view = create_view (False, False))
        if (cur_page == 1):
          await msg.edit (embed = pages_embeds[f"page_{cur_page}"], view = create_view (False, True))

    view = create_view (False, True)
    msg = await ctx.send (embed = pages_embeds[f"page_{cur_page}"], view = view)

    while True:
      try:
        user = await self.bot.wait_for ("interaction", timeout = 10.0,
                                        check = lambda interaction: interaction.user == ctx.author)
      except asyncio.TimeoutError:
        await msg.edit (embed = pages_embeds[f"page_{cur_page}"], view = create_view (True, True))
        break

  @commands.command ()
  async def reply (self, ctx, key, content_1 = None, content_2 = None):
    try:
      with open (f"./datas/reply/reply_{ctx.guild.id}.json", encoding = "utf8") as reply_file:
        rp = json.load (reply_file)
    except:
      with open (f"./datas/reply/reply_{ctx.guild.id}.json", "w", encoding = "utf8") as reply_file:
        json.dump ({}, reply_file, ensure_ascii = False)

    if (key == "add"):
      try:
        if ((content_1 == None)
            or ((content_2 == None) and (len (ctx.message.attachments) == 0))):
          await ctx.send ("你什麼都沒有給我是要加什麼啦")
          return
        elif (len (ctx.message.attachments) != 0):
          urls = []
          for i in ctx.message.attachments:
            urls.append (i.url)
          rp[content_1] = urls
        else:
          rp[content_1] = content_2
        await ctx.reply (f"以後有人說 {content_1}，我會回他 {content_2}")
      except:
        return

    elif (key == "del"):
      if (content_1 == None):
        await ctx.send ("你什麼都沒有給我是要刪空氣喔")
        return
      else:
        try:
          rp.pop (content_1)
          await ctx.send (f"刪除了 {content_1}")
        except:
          await ctx.send ("本來就沒有的東西我要怎麼刪")
          return

    elif (key == "list_f"):
      await ctx.send (file = discord.File (f"./datas/reply/reply_{ctx.guild.id}.json"))
      return

    elif (key == "list"):
      list_rp = rp.copy ()
      for i in list_rp:
        if ((type (list_rp[i]) == list) or (list_rp[i].startswith ("http"))):
          list_rp[i] = "<This is an image or video>"
      for i in list_rp:
        words = "\n".join ([i, f"└ {list_rp[i]}\n"])
      await reply.reply_pages (self, ctx, list_rp)

    else:
      return

    with open (f"./datas/reply/reply_{ctx.guild.id}.json", "w", encoding = "utf8") as reply_file:
      json.dump (rp, reply_file, indent = 2, ensure_ascii = False)

async def setup (bot):
  await bot.add_cog (reply (bot))
