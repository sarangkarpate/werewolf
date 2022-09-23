"""
Model object for a running instance of the bot
"""
from discord.ext import commands
from entities import Role, Room

from util.utils import (
    fetch_bot_command_prefix,
    fetch_bot_token,
    get_moderator,
    get_user,
    pretty_print_dictionary,
)


class Werewolf(commands.Cog, name="Werewolf bot commands"):
    def __init__(self, bot):
        self.Rooms = {}
        self.bot = bot

    @commands.command(
        name="create",
        brief="<room> Creates a room (village)",
        description="Use this command to create a room." "Syntax: create <room_name>",
    )
    async def create_room(ctx: discord.ext.commands.Context, *args: str):
        if not args:
            await ctx.author.send(
                "<room name> is a required argument to the !create command."
            )
            return
        roomname = args[0]
        if room in self.Rooms:
            await ctx.author.send("A room with the name '%s' already exists." % room)
            return
        self.Rooms[room] = Room(moderator=ctx.author.id)
        await get_moderator(ctx, room).send("Room %s created." % room)

    @commands.command(
        name="join",
        brief="<room> Joins a room",
        description="Use this command to join a room." "Syntax: join <room_name>",
    )
    async def join_room(ctx: discord.ext.commands.Context, *args: str):
        if not args:
            await ctx.author.send(
                "<room name> is a required argument to the !join command."
            )
            return
        room = args[0]
        if not room in self.Rooms:
            await ctx.author.send("A room with the name '%s' doesn't exist." % room)
            return
        if ctx.author.id in self.Rooms[room].players:
            await ctx.author.send("You are already in room %s" % room)
            return
        self.Rooms[room].add_player(ctx.author.id)
        await ctx.author.send("You have joined room %s" % room)

    @commands.command(
        name="leave",
        brief="<room> Leaves a room",
        description="Use this command to leave a room." "Syntax: leave <room_name>",
    )
    async def leave_room(ctx: discord.ext.commands.Context, *args: str):
        if not args:
            await ctx.author.send(
                "<room name> is a required argument to the !leave command."
            )
            return
        room = args[0]
        if not room in self.Rooms:
            await ctx.author.send("A room with the name '%s' doesn't exist." % room)
            return
        if not ctx.author.id in self.Rooms[room].players:
            await ctx.author.send("You are not in room %s" % room)
        self.Rooms[room].remove_player(ctx.author.id)
        await ctx.author.send("You have left room %s" % room)

    @commands.command(
        name="remove",
        brief="<room> <player1> <player2> ... Removes players from the room",
        description="Use this command to remove players from a room."
        "Syntax: remove <room_name> <player1> <player2> ...",
    )
    async def remove_player(ctx: discord.ext.commands.Context, *args: str):
        if not args:
            await ctx.author.send(
                "<room name> is a required argument to the !remove command."
            )
            return
        room = args[0]
        if not room in self.Rooms:
            await ctx.author.send("A room with the name '%s' doesn't exist." % room)
            return
        if not ctx.message.mentions:
            await ctx.author.send("Remove People by mentioning them with @ mentions.")
            return
        if not ctx.message.author.id == self.Rooms[room].moderator:
            await ctx.author.send(
                "You must be the moderator for the room to remove players."
            )
            return
        self.Rooms[room].remove_players([p.id for p in ctx.message.mentions])
        await get_moderator(ctx, room).send(
            "Removed Players %s from room %s"
            % (str([x.display_name for x in ctx.message.mentions]), room)
        )
        for p in ctx.message.mentions:
            await p.send("You have been removed from room: %s" % room)

    @commands.command(
        name="invite",
        brief="<room> <player1> <player2> ... Invites players to the room",
        description="Use this command to invite players to a room."
        "Syntax: invite <room_name> <player1> <player2> ...",
    )
    async def invite_player(ctx: discord.ext.commands.Context, *args: str):
        if not args:
            await ctx.author.send(
                "<room name> is a required argument to the !invite command."
            )
            return
        room = args[0]
        if not room in self.Rooms:
            await ctx.author.send("A room with the name '%s' doesn't exist." % room)
            return
        if not ctx.message.mentions:
            await ctx.author.send("Invite People by mentioning them with @ mentions.")
            return
        self.Rooms[room].add_players([p.id for p in ctx.message.mentions if p.bot is False])
        await get_moderator(ctx, room).send(
            "Added Players %s to room %s"
            % (
                str([x.display_name for x in ctx.message.mentions if x.bot is False]),
                room,
            )
        )
        for p in ctx.message.mentions:
            await p.send("You have been added to room: %s" % room)

    @commands.command(
        name="add",
        brief="<room> <role> OR <room> <role> <count> Add roles to a room",
        description="Use this command to add roles to a room."
        "Syntax: add <room> <role> - This adds a role to a room "
        "OR add <room> <role> <count> - This adds <count> number of roles to a room",
    )
    async def add_role(ctx: discord.ext.commands.Context, *args: str):
        if not args:
            await ctx.author.send(
                "<room name> is a required argument to the !add command."
            )
            return
        room = args[0]
        if not room in self.Rooms:
            await ctx.author.send("A room with the name '%s' doesn't exist." % room)
            return
        if not ctx.message.author.id == self.Rooms[room].moderator:
            await ctx.author.send(
                "You must be the moderator for the room to add roles."
            )
            return
        if len(args) == 1:
            await ctx.author.send(
                "<role name> is a required argument to the !add command."
            )
            return
        role_name = args[1]
        if len(args) == 2:
            self.Rooms[room].add_role(role_name)
            await get_moderator(ctx, room).send(
                "Added 1 Role %s to room %s" % (role_name, room)
            )
        else:
            role_count = int(args[2])
            self.Rooms[room].add_role(role_name, role_count)
            await get_moderator(ctx, room).send(
                "Added %i Roles %s to room %s" % (role_count, role_name, room)
            )

    @commands.command(
        name="subtract",
        brief="<room> <role> OR <room> <role> <count> Removes roles from a room",
        description="Use this command to remove roles from a room."
        "Syntax: subtract <room> <role> - This removes one <role> from a room "
        "OR add <room> <role> <count> - This removes <count> number of roles from a room",
    )
    async def subtract_role(ctx: discord.ext.commands.Context, *args: str):
        if not args:
            await ctx.author.send(
                "<room name> is a required argument to the !subtract command."
            )
            return
        room = args[0]
        if not room in self.Rooms:
            await ctx.author.send("A room with the name '%s' doesn't exist." % room)
            return
        if not ctx.message.author.id == self.Rooms[room].moderator:
            await ctx.author.send(
                "You must be the moderator for the room to subtract roles."
            )
            return
        if len(args) == 1:
            await ctx.author.send(
                "<role name> is a required argument to the !subtract command."
            )
            return
        role_name = args[1]
        if len(args) == 2:
            self.Rooms[room].remove_role(role_name)
            await get_moderator(ctx, room).send(
                "Subtracted All Roles %s to room %s" % (role_name, room)
            )
        else:
            role_count = int(args[2])
            self.Rooms[room].remove_role(role_name, role_count)
            await get_moderator(ctx, room).send(
                "Subtracted %i Roles %s to room %s" % (role_count, role_name, room)
            )

    @commands.command(
        name="start",
        brief="<room> Starts a game; assigns roles",
        description="Use this command to start a game."
        "Syntax: start <room> - This assigns roles to all players (sends a DM as well); also sends moderator a list of all role - players mapping",
    )
    async def assign_roles(ctx: discord.ext.commands.Context, *args: str):
        if not args:
            await ctx.author.send(
                "<room name> is a required argument to the !start command."
            )
            return
        room = args[0]
        if room not in self.Rooms:
            await ctx.author.send("A room with the name '%s' doesn't exist." % room)
            return
        village = self.Rooms[room]
        if not ctx.message.author.id == village.moderator:
            await ctx.author.send(
                "You must be the moderator for the room to start the room."
            )
            return
        try:
            game = village.start_game()
            game_description = pretty_print_dictionary(
                {
                    get_user(ctx, player).display_name: role
                    for player, role in game.items()
                }
            )
            await get_user(ctx, village.moderator).send(game_description)
            for player, role in game.items():
                await get_user(ctx, player).send("Game: %s, Role: %s" % (room, role))
            village.started = True
        except Exception as msg:
            # Role count is not the same as Player count while starting the game
            error_message = str(msg) + " for room: " + str(room)
            print(error_message)
            await get_moderator(ctx, room).send(error_message)

    @commands.command(name="list", brief="<room> Lists all roles and players in a room")
    async def list_room_info(ctx: discord.ext.commands.Context, *args: str):
        if not args:
            await ctx.author.send(
                "<room name> is a required argument to the !list command."
            )
            return
        room = args[0]
        if room not in self.Rooms:
            await ctx.author.send("A room with the name '%s' doesn't exist." % room)
            return
        await ctx.send(
            "Room: %s\nModerator: %s\nPlayers: %s\nRoles\n-----------\n%s"
            % (
                room,
                get_user(ctx, int(self.Rooms[room].moderator)).display_name,
                str([get_user(ctx, x).display_name for x in self.Rooms[room].players]),
                str(self.Rooms[room].get_role_information()),
            )
        )

    @commands.command(
        name="listself.Rooms",
        brief="Lists all self.Rooms and associated moderators",
        description="List all self.Rooms and their moderators",
    )
    async def list_all_self.Rooms(ctx: discord.ext.commands.Context):
        response_msg = ""
        for room in self.Rooms:
            response_msg += (
                "Room: "
                + str(room)
                + ": Moderator: "
                + str(get_user(ctx, int(self.Rooms[room].moderator)).display_name)
                + "\n"
            )
        if not response_msg:
            # No self.Rooms available yet
            response_msg = "No self.Rooms have been created yet!"
        await ctx.send(response_msg)

    @commands.command(
        name="reveal",
        brief="<room> Reveals all players and roll mapping in a room",
        description=" Mod restricted. use reveal <room> to reveal true colors!",
    )
    async def reveal_room_info(ctx: discord.ext.commands.Context, *args: str):
        if not args:
            await ctx.author.send(
                "<room name> is a required argument to the reveal command"
            )
            return
        room = args[0]
        if room not in self.Rooms:
            await ctx.author.send("A room with the name '%s' doesn't exist." % room)
            return
        if not ctx.message.author.id == self.Rooms[room].moderator:
            await ctx.author.send(
                "You must be the moderator for the room to reveal roles."
            )
            return

        game_mapping = {
            get_user(ctx, player).display_name: role
            for player, role in self.Rooms[room].assigned_roles.items()
        }
        game_description = pretty_print_dictionary(game_mapping)
        await ctx.send(game_description)

    @commands.command(name="delete", brief="<room> Deletes a room")
    async def delete_room(ctx: discord.ext.commands.Context, *args: str):
        if not args:
            await ctx.author.send(
                "<room name> is a required argument to the !delete command."
            )
            return
        room = args[0]
        if not ctx.message.author.id == self.Rooms[room].moderator:
            await ctx.author.send(
                "You must be the moderator for the room to delete self.Rooms."
            )
            return
        if not room in self.Rooms:
            await ctx.author.send(
                "A room with the name '%s' doesn't exist. It may have been deleted already"
                % room
            )
            return
        del self.Rooms[room]
        await ctx.send("Deleted Room %s" % room)

    @commands.command(
        name="update_moderator",
        brief="<room> <new player> updates moderator",
        description="Use this command for the current moderator to update to a new moderator for the given room"
        "Syntax: update_moderator <room_name> <new_moderator>",
    )
    async def update_moderator(ctx: discord.ext.commands.Context, *args: str):
        if len(args) != 2:
            await ctx.author.send(
                "<room name> and <new_moderator> are the required argument to the !update_moderator command."
            )
            return
        room = args[0]
        new_moderator = ctx.message.mentions[0]
        if not ctx.message.author.id == self.Rooms[room].moderator:
            await ctx.author.send(
                "You must be the current moderator to update or change moderators"
            )
            return
        if new_moderator.id == self.Rooms[room].moderator:
            await ctx.author.send(
                "'%s' is already the moderator of this room." % new_moderator
            )
            return
        if new_moderator.id in self.Rooms[room].players:
            self.Rooms[room].remove_player(new_moderator.id)
            await ctx.author.send(
                "'%s' has been removed from the players list" % new_moderator
            )
        self.Rooms[room].moderator = new_moderator.id
        await new_moderator.send("Congratulations! You are the moderator of %s." % room)
        if self.Rooms[room].started == True:
            game_description = pretty_print_dictionary(
                {
                    get_user(ctx, player).display_name: role
                    for player, role in self.Rooms[room].assigned_roles.items()
                }
            )
            await get_user(ctx, self.Rooms[room].moderator).send(game_description)
