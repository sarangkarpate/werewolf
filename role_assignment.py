#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Werewolf Role Assignment Bot
Created on Thu Sep 15 17:00:51 2022

@author: ian
"""

# Permissions number: 399163731024

import os
import discord
from discord.ext.commands import Bot
import json
from server.backend import Room,Role

PREFIX='$'

Token = os.getenv('DISCORD_TOKEN')
if Token is None:
  Token=""
Rooms = {}
bot=discord.ext.commands.Bot(command_prefix=PREFIX, intents=discord.Intents.default())

@bot.command()
async def a_command(ctx, args):
  print("finally")

@bot.event
async def on_message(message):
  print("read message")
  await bot.process_commands(message)
'''
@bot.command(name="create")
async def create_room(ctx, *args):
  Rooms[args[1]]=Room(moderator=ctx.sender)

@bot.command(name="join")
async def join_room(ctx, *args):
  print()

@bot.command(name="leave")
async def leave_room(ctx, *args):
  print()

@bot.command(name="remove")
async def remove_player(ctx, *args):
  print()

@bot.command(name="invite")
async def remove_player(ctx, *args):
  print()

@bot.command(name="add")
async def add_role(ctx, *args):
  print()

@bot.command(name="subtract")
async def subtract_role(ctx, *args):
  print()

@bot.command(name="start")
async def assign_roles(ctx, *args):
  print()

@bot.command(name="list")
async def list_room_info(ctx, *args):
  print()

@bot.command(name="delete")
async def delete_room(ctx, *args):
  print()
'''
bot.run(Token)
