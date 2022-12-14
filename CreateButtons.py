import random

import discord

style = {'bear': ['๐ป', discord.ButtonStyle.primary], 'Ammar-bear': ['๐งธ', discord.ButtonStyle.primary],
         'seer': ['๐ค', discord.ButtonStyle.primary], 'confused seer': ['๐ฅด', discord.ButtonStyle.primary],
         'one-eyed seer': ['๐ง', discord.ButtonStyle.primary], 'innocent child': ['๐ง', discord.ButtonStyle.green],
         'grenadier': ['๐ฃ', discord.ButtonStyle.green], 'gunsmith': ['๐ซ', discord.ButtonStyle.green],
         'trickster gunsmith': ['๐ซ', discord.ButtonStyle.green], 'mortician': ['๐ฅผ', discord.ButtonStyle.green],
         'Dr.Boom': ['๐งจ', discord.ButtonStyle.green], 'cut throat': ['๐ช', discord.ButtonStyle.green],
         'PI': ['๐ค', discord.ButtonStyle.green], 'hunter': ['๐น', discord.ButtonStyle.green],
         'prince': ['๐', discord.ButtonStyle.green], 'beholder': ['๐', discord.ButtonStyle.green],
         'masons': ['๐ฅ', discord.ButtonStyle.green], 'thing': ['โ', discord.ButtonStyle.green],
         'chupacabra': ['๐', discord.ButtonStyle.green], 'tough guy': ['๐ช', discord.ButtonStyle.green],
         'wheelsmith': ['๐', discord.ButtonStyle.green], "doctor": ['๐ฉบ', discord.ButtonStyle.green],
         'body guard': ['๐๏ธโโ๏ธ', discord.ButtonStyle.green], 'witch': ['๐ง', discord.ButtonStyle.green],
         'tanner': ['๐ญ', discord.ButtonStyle.grey], 'serial killer': ['โฐ', discord.ButtonStyle.grey],
         'hoodlum': ['๐คฅ', discord.ButtonStyle.grey], 'cruel tanner': ['๐', discord.ButtonStyle.grey],
         'jester': ['๐คก', discord.ButtonStyle.grey], 'wolf': ['๐บ', discord.ButtonStyle.red],
         'wolf man': ['๐บ', discord.ButtonStyle.red], 'dire wolf': ['๐บ', discord.ButtonStyle.red],
         'pet wolf': ['๐ถ', discord.ButtonStyle.red], 'armored wolf': ['๐ฆบ', discord.ButtonStyle.red],
         'grandma wolf': ['๐ต', discord.ButtonStyle.red], 'slasher wolf': ['๐ช', discord.ButtonStyle.red],
         'alpha wolf': ['๐ฅ', discord.ButtonStyle.red], 'wolf cub': ['๐ฆ', discord.ButtonStyle.red],
         'slightly mad bomber': ['๐งช', discord.ButtonStyle.red], 'sorceress': ['๐', discord.ButtonStyle.red],
         'mason-sorceress': ['๐ฅ', discord.ButtonStyle.red], 'minion': ['๐ฉ', discord.ButtonStyle.red],
         'villager': ['๐ค?', discord.ButtonStyle.green]}


seer_roles = ['bear', 'Ammar-bear', 'seer', 'confused seer', 'one-eyed seer']
deadly_roles = ['innocent child', 'grenadier', 'gunsmith', 'trickster gunsmith', 'mortician', 'Dr.Boom',
                'cut throat', 'PI', 'hunter']
other_roles = ['prince', 'beholder', 'masons', 'thing', 'chupacabra', 'tough guy', 'wheelsmith', 'villager']
protective_roles = ["doctor", 'body guard', 'witch']
third_party_roles = ['tanner', 'serial killer', 'hoodlum', 'cruel tanner', 'jester']
wolf_roles = ['wolf', 'wolf man', 'dire wolf', 'pet wolf', 'armored wolf', 'grandma wolf', 'slasher wolf',
              'alpha wolf', 'wolf cub']
wolf_friends = ['slightly mad bomber', 'sorceress', 'mason-sorceress','minion']

catagoies = {'WOLVES': wolf_roles, 'SEER': seer_roles, 'BLOOD THIRSTY VILLAGERS': deadly_roles,
             'LESS ANGRY VILLAGERES': other_roles, 'PROTECTIVE VILLAGERS': protective_roles,
             'THIRD PARTY': third_party_roles, 'WOLF FRIENDS': wolf_friends}

async def add_buttons(ctx, type, roles, Rooms, room,style):
    view = discord.ui.View()
    count = 0
    roles = roles.copy()
    while len(roles) > 0 and count < 5:
        if type == 'LESS ANGRY VILLAGERES' and count == 0:
            role = 'villager'
        elif type == 'WOLVES' and count == 0:
            role = 'wolf'
        else:
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
        count += 1
    await ctx.author.send(
        "Add %s roles to the %s village by clicking here!" % (type, room), view=view
    )


async def button_galore(ctx, Rooms, room):
    for catagory in catagoies.keys():
        await add_buttons(ctx, catagory, catagoies[catagory], Rooms, room, style)
