import random

import discord

style = {'bear': ['🐻', discord.ButtonStyle.primary], 'Ammar-bear': ['🧸', discord.ButtonStyle.primary],
         'seer': ['🤓', discord.ButtonStyle.primary], 'confused seer': ['🥴', discord.ButtonStyle.primary],
         'one-eyed seer': ['🧐', discord.ButtonStyle.primary], 'innocent child': ['👧', discord.ButtonStyle.green],
         'grenadier': ['💣', discord.ButtonStyle.green], 'gunsmith': ['🔫', discord.ButtonStyle.green],
         'trickster gunsmith': ['🔫', discord.ButtonStyle.green], 'mortician': ['🥼', discord.ButtonStyle.green],
         'Dr.Boom': ['🧨', discord.ButtonStyle.green], 'cut throat': ['🪒', discord.ButtonStyle.green],
         'PI': ['🤓', discord.ButtonStyle.green], 'hunter': ['🏹', discord.ButtonStyle.green],
         'prince': ['👑', discord.ButtonStyle.green], 'beholder': ['😎', discord.ButtonStyle.green],
         'mason': ['👥', discord.ButtonStyle.green], 'thing': ['☝', discord.ButtonStyle.green],
         'chupacabra': ['😈', discord.ButtonStyle.green], 'tough guy': ['💪', discord.ButtonStyle.green],
         'wheelsmith': ['📀', discord.ButtonStyle.green], "doctor": ['🩺', discord.ButtonStyle.green],
         'body guard': ['🏋️‍♀️', discord.ButtonStyle.green], 'witch': ['🧙', discord.ButtonStyle.green],
         'tanner': ['🎭', discord.ButtonStyle.grey], 'serial killer': ['⚰', discord.ButtonStyle.grey],
         'hoodlum': ['🤥', discord.ButtonStyle.grey], 'cruel tanner': ['🎆', discord.ButtonStyle.grey],
         'jester': ['🤡', discord.ButtonStyle.grey], 'wolf': ['🐺', discord.ButtonStyle.red],
         'wolf man': ['🐺', discord.ButtonStyle.red], 'dire wolf': ['🐺', discord.ButtonStyle.red],
         'pet wolf': ['🐶', discord.ButtonStyle.red], 'armored wolf': ['🦺', discord.ButtonStyle.red],
         'grandma wolf': ['👩‍🦳', discord.ButtonStyle.red], 'slasher wolf': ['🪒', discord.ButtonStyle.red],
         'alpha wolf': ['👥', discord.ButtonStyle.red], 'wolf cub': ['🦝', discord.ButtonStyle.red],
         'slightly mad bomber': ['🥽', discord.ButtonStyle.red], 'sorceress': [':🎆', discord.ButtonStyle.red],
         'mason-sorceress': ['👥', discord.ButtonStyle.red]}


seer_roles = ['bear', 'Ammar-bear', 'seer', 'confused seer', 'one-eyed seer']
deadly_roles = ['innocent child', 'grenidier', 'gunsmith', 'trickster gunsmith', 'mortician', 'Dr.Boom',
                'cut throat', 'PI', 'hunter']
other_roles = ['prince', 'beholder', 'masons', 'thing', 'chupacabra', 'tough guy', 'wheelsmith']
protective_roles = ["doctor", 'body guard', 'witch']
third_party_roles = ['tanner', 'serial killer', 'hoodlum', 'cruel tanner', 'jester']
wolf_roles = ['wolf', 'wolf man', 'dire wolf', 'pet wolf', 'armored wolf', 'grandma wolf', 'slasher wolf',
              'alpha wolf', 'wolf cub']
wolf_friends = ['mason', 'slightly mad bomber', 'sorceress', 'mason-sorceress']

catagoies = {'WOLVES': wolf_roles, 'SEER': seer_roles, 'BLOOD THIRSTY VILLAGERS': deadly_roles,
             'LESS ANGRY VILLAGERES': other_roles, 'PROTECTIVE VILLAGERS': protective_roles,
             'THIRD PARTY': third_party_roles, 'WOLF FRIENDS': wolf_friends}

async def add_buttons(ctx, type, roles, Rooms, room,style):
    view = discord.ui.View()
    for _x in range(5):
        if 0 == len(roles):
            break
        role = random.choice(roles)
        roles.remove(role)
        button = discord.ui.Button(label=role, custom_id=role, emoji=style[role][0], style=style[role][1])
        async def button_callback(interaction):
            Rooms[room].add_role(interaction.data['custom_id'])
            await interaction.response.edit_message(
                content="Add %s roles to the %s village by clicking here! You added %s"
                % (type, room, interaction.data["custom_id"])
            )

        button.callback = button_callback
        view.add_item(button)
    await ctx.author.send(
        "Add %s roles to the %s village by clicking here!" % (type, room), view=view
    )


async def button_galore(ctx, Rooms, room):
    for catagory in catagoies.keys():
        await add_buttons(ctx, catagory, catagoies[catagory], Rooms, room, style)
