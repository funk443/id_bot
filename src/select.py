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

import discord, random
from discord.ext import commands

class select (commands.Cog):
  def __init__ (self, bot):
    self.bot = bot

  @commands.command ()
  async def sel (self, ctx, *items):
    item = random.choice (items)
    await ctx.reply (f"我選 {item}")

async def setup (bot):
  await bot.add_cog (select (bot))
