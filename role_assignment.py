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
  if not args:
    await ctx.author.send("<room name> is a required argument to the !create command.")
    return
  if args[0] in Rooms:
    await ctx.author.send("A room with the name '%s' already exists." % args[0])
    return
  Rooms[args[0]]=Room(moderator=ctx.author.id)
  await get_moderator(ctx, args[0]).send("Room %s created." % args[0])

@bot.command(name="join")
async def join_room(ctx, *args):
  if not args:
    await ctx.author.send("<room name> is a required argument to the !join command.")
    return
  if not args[0] in Rooms:
    await ctx.author.send("A room with the name '%s' doesn't exist." % args[0])
    return
  if ctx.author.id in Rooms[args[0]].players:
    await ctx.author.send("You are already in room %s" % args[0])
    return
  Rooms[args[0]].add_player(ctx.author.id)
  await ctx.author.send("You have joined room %s" % args[0])

@bot.command(name="leave")
async def leave_room(ctx, *args):
  if not args:
    await ctx.author.send("<room name> is a required argument to the !leave command.")
    return
  if not args[0] in Rooms:
    await ctx.author.send("A room with the name '%s' doesn't exist." % args[0])
    return
  if not ctx.author.id in Rooms[args[0]].players:
    await ctx.author.send("You are not in room %s" % args[0])
  Rooms[args[0]].remove_player(ctx.author.id)
  await ctx.author.send("You have left room %s" % args[0])

@bot.command(name="remove")
async def remove_player(ctx, *args):
  if not args:
    await ctx.author.send("<room name> is a required argument to the !remove command.")
    return
  if not args[0] in Rooms:
    await ctx.author.send("A room with the name '%s' doesn't exist." % args[0])
    return
  if not ctx.message.mentions:
    await ctx.author.send("Remove People by mentioning them with @ mentions.")
    return
  if not ctx.message.author.id == Rooms[args[0]].moderator:
    await ctx.author.send("You must be the moderator for the room to remove players.")
    return
  Rooms[args[0]].remove_players([p.id for p in ctx.message.mentions])
  await get_moderator(ctx, args[0]).send("Removed Players %s from room %s" % (str([x.display_name for x in ctx.message.mentions]), args[0]))
  for p in ctx.message.mentions:
    p.send("You have been removed from room: %s" % args[0])

@bot.command(name="invite")
async def invite_player(ctx, *args):
  if not args:
    await ctx.author.send("<room name> is a required argument to the !invite command.")
    return
  if not args[0] in Rooms:
    await ctx.author.send("A room with the name '%s' doesn't exist." % args[0])
    return
  if not ctx.message.mentions:
    await ctx.author.send("Invite People by mentioning them with @ mentions.")
    return
  Rooms[args[0]].add_players([p.id for p in ctx.message.mentions])
  await get_moderator(ctx, args[0]).send("Added Players %s to room %s" % (str([x.display_name for x in ctx.message.mentions]), args[0]))
  for p in ctx.message.mentions:
    p.send("You have been added to room: %s" % args[0])

@bot.command(name="add")
async def add_role(ctx, *args):
  if not args:
    await ctx.author.send("<room name> is a required argument to the !add command.")
    return
  if not args[0] in Rooms:
    await ctx.author.send("A room with the name '%s' doesn't exist." % args[0])
    return
  if len(args) ==1:
    await ctx.author.send("<role name> is a required argument to the !add command.")
    return
  if not ctx.message.author.id == Rooms[args[0]].moderator:
    await ctx.author.send("You must be the moderator for the room to add roles.")
    return
  if len(args) >=3:
    Rooms[args[0]].add_role(args[1], int(args[2]))
    await get_moderator(ctx, args[0]).send("Added %i Roles %s to room %s" % (int(args[2]), args[1], args[0]))
  else:
    Rooms[args[0]].add_role(args[1])
    await get_moderator(ctx, args[0]).send("Added 1 Role %s to room %s" % (args[1], args[0]))

@bot.command(name="subtract")
async def subtract_role(ctx, *args):
  if not args:
    await ctx.author.send("<room name> is a required argument to the !subtract command.")
    return
  if not args[0] in Rooms:
    await ctx.author.send("A room with the name '%s' doesn't exist." % args[0])
    return
  if len(args) ==1:
    await ctx.author.send("<role name> is a required argument to the !subtract command.")
    return
  if not ctx.message.author.id == Rooms[args[0]].moderator:
    await ctx.author.send("You must be the moderator for the room to subtract roles.")
    return
  if len(args) >=3:
    Rooms[args[0]].remove_role(args[1], int(args[2]))
    await get_moderator(ctx, args[0]).send("Subtracted %i Roles %s to room %s" % (int(args[2]), args[1], args[0]))
  else:
    Rooms[args[0]].remove_role(args[1])
    await get_moderator(ctx, args[0]).send("Subtracted All Roles %s to room %s" % (args[1], args[0]))

@bot.command(name="start")
async def assign_roles(ctx, *args):
  if not args:
    await ctx.author.send("<room name> is a required argument to the !start command.")
    return
  if not args[0] in Rooms:
    await ctx.author.send("A room with the name '%s' doesn't exist." % args[0])
    return
  if not ctx.message.author.id == Rooms[args[0]].moderator:
    await ctx.author.send("You must be the moderator for the room to start the room.")
    return
  game=Rooms[args[0]].start_game()
  game_description = str({get_user(ctx,player).display_name : role for player, role in game.items()})
  await get_user(ctx,Rooms[args[0]].moderator).send(game_description)
  for player,role in game.items():
    await get_user(ctx,player).send("Game: %s, Role: %s" % (args[0], role))

@bot.command(name="list")
async def list_room_info(ctx, *args):
  if not args:
    await ctx.author.send("<room name> is a required argument to the !list command.")
    return
  if not args[0] in Rooms:
    await ctx.author.send("A room with the name '%s' doesn't exist." % args[0])
    return
  room=args[0]
  await ctx.send("Room: %s\nModerator: %s\nPlayers: %s\nRoles:\n%s" % (room, get_user(ctx, int(Rooms[room].moderator)).display_name, str([get_user(ctx, x).display_name for x in Rooms[room].players]), str(Rooms[room].get_roles())))

@bot.command(name="delete")
async def delete_room(ctx, *args):
  if not args:
    await ctx.author.send("<room name> is a required argument to the !delete command.")
    return
  if not args[0] in Rooms:
    await ctx.author.send("A room with the name '%s' doesn't exist. It may have been deleted already" % args[0])
    return
  if not ctx.message.author.id == Rooms[args[0]].moderator:
    await ctx.author.send("You must be the moderator for the room to delete rooms.")
    return
  if args[0] in Rooms:
    del Rooms[args[0]]
    await ctx.send("Deleted Room %s" % args[0])

bot.run(Token)
