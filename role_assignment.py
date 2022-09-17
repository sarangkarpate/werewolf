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
# Requires turning on Message Content Intent on the bot page of discord.com/developers. This is required to read messages for command processing.
requested_intents.message_content = True
# Requires turning on Member Intent on the bot page of discord.com/developers. This is required to look up members by ID to message them.
requested_intents.members = True
bot=discord.ext.commands.Bot(command_prefix=PREFIX, intents=requested_intents)

def get_user(ctx, identifier):
  return ctx.guild.get_member(int(identifier))

def get_moderator(ctx,room_name):
  return get_user(ctx, Rooms[room_name].moderator)

@bot.command(name="create")
async def create_room(ctx, *args):
  room = args[0]
  if not args:
    await ctx.author.send("<room name> is a required argument to the !create command.")
    return
  if room in Rooms:
    await ctx.author.send("A room with the name '%s' already exists." % room)
    return
  Rooms[room]=Room(moderator=ctx.author.id)
  await get_moderator(ctx, room).send("Room %s created." % room)

@bot.command(name="join")
async def join_room(ctx, *args):
  room = args[0]
  if not args:
    await ctx.author.send("<room name> is a required argument to the !join command.")
    return
  if not room in Rooms:
    await ctx.author.send("A room with the name '%s' doesn't exist." % room)
    return
  if ctx.author.id in Rooms[room].players:
    await ctx.author.send("You are already in room %s" % room)
    return
  Rooms[room].add_player(ctx.author.id)
  await ctx.author.send("You have joined room %s" % room)

@bot.command(name="leave")
async def leave_room(ctx, *args):
  room = args[0]
  if not args:
    await ctx.author.send("<room name> is a required argument to the !leave command.")
    return
  if not room in Rooms:
    await ctx.author.send("A room with the name '%s' doesn't exist." % room)
    return
  if not ctx.author.id in Rooms[room].players:
    await ctx.author.send("You are not in room %s" % room)
  Rooms[room].remove_player(ctx.author.id)
  await ctx.author.send("You have left room %s" % room)

@bot.command(name="remove")
async def remove_player(ctx, *args):
  room = args[0]
  if not args:
    await ctx.author.send("<room name> is a required argument to the !remove command.")
    return
  if not room in Rooms:
    await ctx.author.send("A room with the name '%s' doesn't exist." % room)
    return
  if not ctx.message.mentions:
    await ctx.author.send("Remove People by mentioning them with @ mentions.")
    return
  if not ctx.message.author.id == Rooms[room].moderator:
    await ctx.author.send("You must be the moderator for the room to remove players.")
    return
  Rooms[room].remove_players([p.id for p in ctx.message.mentions])
  await get_moderator(ctx, room).send("Removed Players %s from room %s" % (str([x.display_name for x in ctx.message.mentions]), room))
  for p in ctx.message.mentions:
    p.send("You have been removed from room: %s" % room)

@bot.command(name="invite")
async def invite_player(ctx, *args):
  room = args[0]
  if not args:
    await ctx.author.send("<room name> is a required argument to the !invite command.")
    return
  if not room in Rooms:
    await ctx.author.send("A room with the name '%s' doesn't exist." % room)
    return
  if not ctx.message.mentions:
    await ctx.author.send("Invite People by mentioning them with @ mentions.")
    return
  Rooms[room].add_players([p.id for p in ctx.message.mentions])
  await get_moderator(ctx, room).send("Added Players %s to room %s" % (str([x.display_name for x in ctx.message.mentions]), room))
  for p in ctx.message.mentions:
    p.send("You have been added to room: %s" % room)

@bot.command(name="add")
async def add_role(ctx, *args):
  room = args[0]
  if not args:
    await ctx.author.send("<room name> is a required argument to the !add command.")
    return
  if not room in Rooms:
    await ctx.author.send("A room with the name '%s' doesn't exist." % room)
    return
  if not ctx.message.author.id == Rooms[room].moderator:
    await ctx.author.send("You must be the moderator for the room to add roles.")
    return
  if len(args) == 1:
    await ctx.author.send("<role name> is a required argument to the !add command.")
    return
  if len(args) == 2:
    Rooms[room].add_role(args[1])
    await get_moderator(ctx, room).send("Added 1 Role %s to room %s" % (args[1], room))
  if len(args) >= 3:
    Rooms[room].add_role(args[1], int(args[2]))
    await get_moderator(ctx, room).send("Added %i Roles %s to room %s" % (int(args[2]), args[1], room))

@bot.command(name="subtract")
async def subtract_role(ctx, *args):
  room = args[0]
  if not args:
    await ctx.author.send("<room name> is a required argument to the !subtract command.")
    return
  if not room in Rooms:
    await ctx.author.send("A room with the name '%s' doesn't exist." % room)
    return
  if not ctx.message.author.id == Rooms[room].moderator:
    await ctx.author.send("You must be the moderator for the room to subtract roles.")
    return
  if len(args) == 1:
    await ctx.author.send("<role name> is a required argument to the !subtract command.")
    return
  if len(args) == 2:
    Rooms[room].remove_role(args[1])
    await get_moderator(ctx, room).send("Subtracted All Roles %s to room %s" % (args[1], room))
  if len(args) >= 3:
    Rooms[room].remove_role(args[1], int(args[2]))
    await get_moderator(ctx, room).send("Subtracted %i Roles %s to room %s" % (int(args[2]), args[1], room))

@bot.command(name="start")
async def assign_roles(ctx, *args):
  room = args[0]
  if not args:
    await ctx.author.send("<room name> is a required argument to the !start command.")
    return
  if not room in Rooms:
    await ctx.author.send("A room with the name '%s' doesn't exist." % room)
    return
  if not ctx.message.author.id == Rooms[room].moderator:
    await ctx.author.send("You must be the moderator for the room to start the room.")
    return
  game = Rooms[room].start_game()
  game_description = str({get_user(ctx,player).display_name : role for player, role in game.items()})
  await get_user(ctx,Rooms[room].moderator).send(game_description)
  for player,role in game.items():
    await get_user(ctx,player).send("Game: %s, Role: %s" % (room, role))

@bot.command(name="list")
async def list_room_info(ctx, *args):
  room = args[0]
  if not args:
    await ctx.author.send("<room name> is a required argument to the !list command.")
    return
  if not room in Rooms:
    await ctx.author.send("A room with the name '%s' doesn't exist." % room)
    return
  await ctx.send("Room: %s\nModerator: %s\nPlayers: %s\nRoles:\n%s" % (room, get_user(ctx, int(Rooms[room].moderator)).display_name, str([get_user(ctx, x).display_name for x in Rooms[room].players]), str(Rooms[room].get_roles())))

@bot.command(name="delete")
async def delete_room(ctx, *args):
  room = args[0]
  if not args:
    await ctx.author.send("<room name> is a required argument to the !delete command.")
    return
  if not room in Rooms:
    await ctx.author.send("A room with the name '%s' doesn't exist. It may have been deleted already" % room)
    return
  if not ctx.message.author.id == Rooms[room].moderator:
    await ctx.author.send("You must be the moderator for the room to delete rooms.")
    return
  if room in Rooms:
    del Rooms[room]
    await ctx.send("Deleted Room %s" % room)

bot.run(Token)
