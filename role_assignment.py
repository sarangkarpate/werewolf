#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Werewolf Role Assignment Bot
Created on Thu Sep 15 17:00:51 2022

@author: ian
"""

import discord
from discord.ext.commands import Bot
from server.backend import Room, Role
from util.utils import fetch_bot_token, fetch_bot_command_prefix, get_user

Rooms = {}

# Note that the requested Permissions number was created with: 399163731024
requested_intents = discord.Intents.default()
# Requires turning on Message Content Intent on the bot page of discord.com/developers. This is required to read messages for command processing.
requested_intents.message_content = True
# Requires turning on Member Intent on the bot page of discord.com/developers. This is required to look up members by ID to message them.
requested_intents.members = True
bot = discord.ext.commands.Bot(command_prefix=fetch_bot_command_prefix(), intents=requested_intents)


def get_moderator(ctx, room_name):
    """
    Gets a moderator based on context.
    :param ctx:
    :param room_name:
    :return: Optional[Member]
    """
    return get_user(ctx, Rooms[room_name].moderator)


@bot.command(name="create")
async def create_room(ctx, *args):
    if not args:
        await ctx.author.send("<room name> is a required argument to the !create command.")
        return
    room = args[0]
    if room in Rooms:
        await ctx.author.send("A room with the name '%s' already exists." % room)
        return
    Rooms[room] = Room(moderator=ctx.author.id)
    await get_moderator(ctx, room).send("Room %s created." % room)


@bot.command(name="join")
async def join_room(ctx, *args):
    if not args:
        await ctx.author.send("<room name> is a required argument to the !join command.")
        return
    room = args[0]
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
    if not args:
        await ctx.author.send("<room name> is a required argument to the !leave command.")
        return
    room = args[0]
    if not room in Rooms:
        await ctx.author.send("A room with the name '%s' doesn't exist." % room)
        return
    if not ctx.author.id in Rooms[room].players:
        await ctx.author.send("You are not in room %s" % room)
    Rooms[room].remove_player(ctx.author.id)
    await ctx.author.send("You have left room %s" % room)


@bot.command(name="remove")
async def remove_player(ctx, *args):
    if not args:
        await ctx.author.send("<room name> is a required argument to the !remove command.")
        return
    room = args[0]
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
    await get_moderator(ctx, room).send(
        "Removed Players %s from room %s" % (str([x.display_name for x in ctx.message.mentions]), room))
    for p in ctx.message.mentions:
        await p.send("You have been removed from room: %s" % room)


@bot.command(name="invite")
async def invite_player(ctx, *args):
    if not args:
        await ctx.author.send("<room name> is a required argument to the !invite command.")
        return
    room = args[0]
    if not room in Rooms:
        await ctx.author.send("A room with the name '%s' doesn't exist." % room)
        return
    if not ctx.message.mentions:
        await ctx.author.send("Invite People by mentioning them with @ mentions.")
        return
    Rooms[room].add_players([p.id for p in ctx.message.mentions if p.bot is False])
    await get_moderator(ctx, room).send(
        "Added Players %s to room %s" % (
            str([x.display_name for x in ctx.message.mentions if x.bot is False]), room))
    for p in ctx.message.mentions:
        await p.send("You have been added to room: %s" % room)


@bot.command(name="add")
async def add_role(ctx, *args):
    if not args:
        await ctx.author.send("<room name> is a required argument to the !add command.")
        return
    room = args[0]
    if not room in Rooms:
        await ctx.author.send("A room with the name '%s' doesn't exist." % room)
        return
    if not ctx.message.author.id == Rooms[room].moderator:
        await ctx.author.send("You must be the moderator for the room to add roles.")
        return
    if len(args) == 1:
        await ctx.author.send("<role name> is a required argument to the !add command.")
        return
    role_name = args[1]
    if len(args) == 2:
        Rooms[room].add_role(role_name)
        await get_moderator(ctx, room).send("Added 1 Role %s to room %s" % (role_name, room))
    else:
        role_count = int(args[2])
        Rooms[room].add_role(role_name, role_count)
        await get_moderator(ctx, room).send("Added %i Roles %s to room %s" % (role_count, role_name, room))


@bot.command(name="subtract")
async def subtract_role(ctx, *args):
    if not args:
        await ctx.author.send("<room name> is a required argument to the !subtract command.")
        return
    room = args[0]
    if not room in Rooms:
        await ctx.author.send("A room with the name '%s' doesn't exist." % room)
        return
    if not ctx.message.author.id == Rooms[room].moderator:
        await ctx.author.send("You must be the moderator for the room to subtract roles.")
        return
    if len(args) == 1:
        await ctx.author.send("<role name> is a required argument to the !subtract command.")
        return
    role_name = args[1]
    if len(args) == 2:
        Rooms[room].remove_role(role_name)
        await get_moderator(ctx, room).send("Subtracted All Roles %s to room %s" % (role_name, room))
    else:
        role_count = int(args[2])
        Rooms[room].remove_role(role_name, role_count)
        await get_moderator(ctx, room).send("Subtracted %i Roles %s to room %s" % (role_count, role_name, room))


@bot.command(name="start")
async def assign_roles(ctx, *args):
    if not args:
        await ctx.author.send("<room name> is a required argument to the !start command.")
        return
    room = args[0]
    if room not in Rooms:
        await ctx.author.send("A room with the name '%s' doesn't exist." % room)
        return
    village = Rooms[room]
    if not ctx.message.author.id == village.moderator:
        await ctx.author.send("You must be the moderator for the room to start the room.")
        return
    try:
        game = village.start_game()
        game_description = str({get_user(ctx, player).display_name: role for player, role in game.items()})
        await get_user(ctx, village.moderator).send(game_description)
        for player, role in game.items():
            await get_user(ctx, player).send("Game: %s, Role: %s" % (room, role))
    except AssertionError as msg:
        # Role count is not the same as Player count while starting the game
        print(msg)
        await get_moderator(ctx, room).send(
            "Cannot start game for room: {} because Role count is {} and Player count is {}".format(room,
                                                                                                    village.fetch_role_count(),
                                                                                                    village.fetch_player_count()))


@bot.command(name="list")
async def list_room_info(ctx, *args):
    if not args:
        await ctx.author.send("<room name> is a required argument to the !list command.")
        return
    room = args[0]
    if room not in Rooms:
        await ctx.author.send("A room with the name '%s' doesn't exist." % room)
        return
    await ctx.send("Room: %s\nModerator: %s\nPlayers: %s\nRoles:\n%s" % (
        room, get_user(ctx, int(Rooms[room].moderator)).display_name,
        str([get_user(ctx, x).display_name for x in Rooms[room].players]), str(Rooms[room].get_roles())))


@bot.command(name="delete")
async def delete_room(ctx, *args):
    if not args:
        await ctx.author.send("<room name> is a required argument to the !delete command.")
        return
    room = args[0]
    if not ctx.message.author.id == Rooms[room].moderator:
        await ctx.author.send("You must be the moderator for the room to delete rooms.")
        return
    if not room in Rooms:
        await ctx.author.send("A room with the name '%s' doesn't exist. It may have been deleted already" % room)
        return
    del Rooms[room]
    await ctx.send("Deleted Room %s" % room)


bot.run(fetch_bot_token())
