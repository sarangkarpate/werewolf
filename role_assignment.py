#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Werewolf Role Assignment Bot
Created on Thu Sep 15 17:00:51 2022

@author: ian
"""

import os
import discord
from discord.ext.commands import Bot
import json
from server.backend import Room,Role

PREFIX='!'

with open("config.json") as config_file:
  config=json.load(config_file)
Token = config['Token']

Rooms = {}


# Note that the requested Permissions number should be: 399163731024
requested_intents = discord.Intents.default()
requested_intents.message_content = True
bot=discord.ext.commands.Bot(command_prefix=PREFIX, intents=requested_intents)

@bot.command(name="create")
async def create_room(ctx, *args):
  print("creating")
  print(args)
  if not args:
    print("Need room name.")
  Rooms[args[0]]=Room(moderator=ctx)

@bot.command(name="join")
async def join_room(ctx, *args):
  print("joining")

@bot.command(name="leave")
async def leave_room(ctx, *args):
  print("leaving")

@bot.command(name="remove")
async def remove_player(ctx, *args):
  print()

@bot.command(name="invite")
async def invite_player(ctx, *args):
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

bot.run(Token)
