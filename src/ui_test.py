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

import discord
from discord import ui, SelectOption
from discord.ext import commands

class ui_test (commands.Cog):
  def __init__ (self, bot):
    self.bot = bot

  @commands.command ()
  async def button_test (self, ctx):
    async def test_button_callback (interaction):
      await interaction.response.defer ()

    view = ui.View ()
    test_button = ui.Button (label = "test")
    test_button.callback = test_button_callback
    view.add_item (test_button)
    await ctx.send (view = view)


  @commands.command ()
  async def select_test (self, ctx):
    async def test_select_callback (interaction):
      await interaction.response.defer ()
      await ctx.send (test_select.values[0])
      print (test_select.values)

    view = ui.View ()
    test_select = ui.Select (placeholder = "Test",
                             options = [SelectOption (label = "a"),
                                        SelectOption (label = "b"),
                                        SelectOption (label = "c")])
    test_select.callback = test_select_callback
    view.add_item (test_select)
    await ctx.send (view = view)

  @commands.command ()
  async def modal_test (self, ctx):
    class modal1 (ui.Modal, title = "modal test"):
      usr_input = ui.TextInput (label = "Input Below")

      async def on_submit (self, interaction):
        await interaction.response.defer ()
        print (self.usr_input.value)

    async def calbak (interaction):
      await interaction.response.send_modal (modal1 ())

    view = ui.View ()
    button = ui.Button (label = "go")
    view.add_item (button)
    button.callback = calbak

    await ctx.send (view = view)

async def setup (bot):
  await bot.add_cog (ui_test (bot))
