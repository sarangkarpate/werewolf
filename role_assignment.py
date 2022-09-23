#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Werewolf Role Assignment Bot
Created on Thu Sep 15 17:00:51 2022

@author: ian
"""

from typing import Optional
import discord
from utils import fetch_bot_command_prefix, fetch_bot_token
from models import Werewolf

# Note that the requested Permissions number was created with: 399163731024
requested_intents = discord.Intents.default()
# Requires turning on Message Content Intent on the bot page of discord.com/developers. This is required to read messages for command processing.
requested_intents.message_content = True
# Requires turning on Member Intent on the bot page of discord.com/developers. This is required to look up members by ID to message them.
requested_intents.members = True
bot = discord.ext.commands.Bot(
    command_prefix=fetch_bot_command_prefix(), intents=requested_intents
)
bot.add_cog(Werewolf(bot))
bot.run(fetch_bot_token())
