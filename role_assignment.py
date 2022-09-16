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


# Note that the requested Permissions number was created with: 399163731024
requested_intents = discord.Intents.default()
# Requires turning on Message Content Intent on the bot page. of discord.com/developers
requested_intents.message_content = True
bot=discord.ext.commands.Bot(command_prefix=PREFIX, intents=requested_intents)

@bot.command(name="create")
async def create_room(ctx, *args):
  print("creating")
  print(args)
  if not args:
    print("Need room name.")
  Rooms[args[0]]=Room(moderator=ctx.author.id)

@bot.command(name="join")
async def join_room(ctx, args):
  Rooms[args[0]].add_player(ctx.author.id)

@bot.command(name="leave")
async def leave_room(ctx, args):
  Rooms[args[0]].remove_player(ctx.author.id)

@bot.command(name="remove")
async def remove_player(ctx, args):
  Rooms[args[0]].remove_player(args[1])

@bot.command(name="invite")
async def invite_player(ctx, args):
  Rooms[args[0]].add_player(args[1])

@bot.command(name="add")
async def add_role(ctx, args):
  Rooms[args[0]].add_role(args[1])

@bot.command(name="subtract")
async def subtract_role(ctx, args):
  Rooms[args[0]].remove_role(args[1])

@bot.command(name="start")
async def assign_roles(ctx, args):
  game=Rooms[args[0]].start_game()
  members=ctx.guild.members()
  members_map = {x.id : x for x in members}
  members[Rooms[args[0]].moderator].send(game)
  for player,role in game.items:
    members[player].send("Game: %s, Role: %s" % (args[0], role))

@bot.command(name="list")
async def list_room_info(ctx, args):
  ctx.send("Room %s Info:\n%s" % (args[0], str(Rooms[args[0]].get_roles())))

@bot.command(name="delete")
async def delete_room(ctx, args):
  if args[0] in Rooms:
    del Rooms[args[0]]
    ctx.send("Deleted Room %s" % args[0])

bot.run(Token)
