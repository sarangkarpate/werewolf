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
    if ctx.guild:
        return get_user(ctx, Rooms[room_name].moderator)
    else:
        # For DM scenarios
        return ctx.author


@bot.command(name="create", brief="<room> Creates a room (village)", description="Use this command to create a room."
                                                                                 "Syntax: create <room_name>")
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


@bot.command(name="join", brief="<room> Joins a room", description="Use this command to join a room."
                                                                   "Syntax: join <room_name>")
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


@bot.command(name="leave", brief="<room> Leaves a room", description="Use this command to leave a room."
                                                                     "Syntax: leave <room_name>")
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


@bot.command(name="remove", brief="<room> <player1> <player2> ... Removes players from the room",
             description="Use this command to remove players from a room."
                         "Syntax: remove <room_name> <player1> <player2> ...")
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


@bot.command(name="invite", brief="<room> <player1> <player2> ... Invites players to the room",
             description="Use this command to invite players to a room."
                         "Syntax: invite <room_name> <player1> <player2> ...")
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


@bot.command(name="add", brief="<room> <role> OR <room> <role> <count> Add roles to a room",
             description="Use this command to add roles to a room."
                         "Syntax: add <room> <role> - This adds a role to a room "
                         "OR add <room> <role> <count> - This adds <count> number of roles to a room")
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


@bot.command(name="subtract", brief="<room> <role> OR <room> <role> <count> Removes roles from a room",
             description="Use this command to remove roles from a room."
                         "Syntax: subtract <room> <role> - This removes one <role> from a room "
                         "OR add <room> <role> <count> - This removes <count> number of roles from a room")
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


@bot.command(name="start", brief="<room> Starts a game; assigns roles",
             description="Use this command to start a game."
                         "Syntax: start <room> - This assigns roles to all players (sends a DM as well); also sends moderator a list of all role - players mapping")
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
    except Exception as msg:
        # Role count is not the same as Player count while starting the game
        error_message = str(msg) + " for room: " + str(room)
        print(error_message)
        await get_moderator(ctx, room).send(error_message)


@bot.command(name="list", brief="<room> Lists all roles and players in a room")
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


@bot.command(name="lists", brief="Lists all rooms and associated moderators",
             description="List all Rooms and their moderators")
async def list_all_rooms(ctx):
    response_msg = ""
    for room in Rooms:
        response_msg += "Room: " + str(room) + ": Moderator: " + str(
            get_user(ctx, int(Rooms[room].moderator)).display_name) + "\n"
    if not response_msg:
        # No Rooms available yet
        response_msg =  "No rooms have been created yet!"
    await ctx.send(response_msg)


@bot.command(name="reveal", brief="<room> Reveals all players and roll mapping in a room",
             description=" Mod restricted. use reveal <room> to reveal true colors!")
async def reveal_room_info(ctx, *args):
    if not args:
        await ctx.author.send("<room name> is a required argument to the reveal command")
        return
    room = args[0]
    if room not in Rooms:
        await ctx.author.send("A room with the name '%s' doesn't exist." % room)
        return
    if not ctx.message.author.id == Rooms[room].moderator:
        await ctx.author.send("You must be the moderator for the room to reveal roles.")
        return

    game_description = str({get_user(ctx, player).display_name: role for player, role in Rooms[room].assigned_roles.items()})
    await ctx.send(game_description)


@bot.command(name="delete", brief="<room> Deletes a room")
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
