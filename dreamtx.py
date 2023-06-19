import discord
import sys
import os
import io
import asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions
import discord.ext
import random
import requests
import json
from random import randint
from bs4 import BeautifulSoup
import TenGiphPy

token =""
tenor_token = ''

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='c!',intents=intents)
bot.remove_command('help')


@bot.event
async def on_ready():
    print("Connected")
    await bot.change_presence(activity=discord.Activity(type=2, name='c!help'))

@bot.command()
async def userinfo(ctx, user: discord.Member = None):
    if user is None:
        randomColor = randint(0, 16777216)

        em = discord.Embed(color=randomColor,
                           title=f'User Info: {ctx.message.author.name}')
        em.add_field(
            name='Status', value=f'Current Status: {ctx.message.author.status}')
        em.add_field(name='Account Created',
                     value=ctx.message.author.created_at.__format__('%A, %B %d, %Y'))
        em.add_field(name='ID', value=f'{ctx.message.author.id}')
        em.set_thumbnail(url=ctx.message.author.avatar)
        await ctx.send(embed=em)
    else:
        randomColor = randint(0, 16777216)
        em = discord.Embed(color=randomColor, title=f'User Info: {user.name}')
        em.add_field(name='Status', value=f'{user.status}')
        em.add_field(name='Account Created',
                     value=user.created_at.__format__('%A, %B %d, %Y'))
        em.add_field(name='ID', value=f'{user.id}')
        em.set_thumbnail(url=user.avatar)
        await ctx.send(embed=em)


@bot.command()
async def servercount(ctx):
    await ctx.send(f"{len(bot.guilds)} Servers")


@bot.command()
@has_permissions(administrator=True)
async def warn(ctx, user: discord.Member, *, reason="No Reason Given"):
    randomColor = randint(0, 16777216)
    em = discord.Embed(color=randomColor,
                       title=f"You Are Warned :rage:", description=f"{reason}")
    em.set_footer(text=f"From : {ctx.author.guild.name}")
    await user.send(embed=em)
    await ctx.message.delete()
    await ctx.send("> ``User Has Been Warned`` :eyes:")


@warn.error
async def warn_error(ctx, error):
    randomColor = randint(0, 16777216)
    if isinstance(error, commands.MissingRequiredArgument):
        warn_embed = discord.Embed(
            title="Error : Missing Few Argument", color=randomColor)
        warn_embed.add_field(name="Usage :", value="c!warn @user", inline=True)
        warn_embed.add_field(
            name="Example : ", value="c!warn @KEE6#3362", inline=True)
        warn_embed.set_footer(text="Hope You Have Understood Now")
        await ctx.send(embed=warn_embed)

    if isinstance(error, commands.MissingPermissions):
        warn_error = discord.Embed(title=f"Error : Missing Permission",
                                   description="Looks Like You Don't Have Required Permission", color=0x00ff00)
        warn_error.add_field(
            name="Permission Requirements :", value="`administration`")

        await ctx.send(embed=warn_error)

    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("I Don't Have Enough Permissions")


@bot.command(aliases=['clear', 'delete', 'clean'])
@has_permissions(manage_messages=True)
async def purge(ctx, num: int):
    await ctx.channel.purge(limit=num+1)
    msg = await ctx.send(f"> ``{num} Messages Has Been Deleted`` :eyes:")
    await asyncio.sleep(3)
    await msg.delete()


@purge.error
async def purge_error(ctx, error):
    randomColor = randint(0, 16777216)
    if isinstance(error, commands.MissingRequiredArgument):
        purge_embed = discord.Embed(
            title="Error : Missing Few Argument", color=randomColor)
        purge_embed.add_field(
            name="Usage :", value="c!purge <no. of message>", inline=True)
        purge_embed.add_field(
            name="Example : ", value="c!purge 5", inline=True)
        purge_embed.set_footer(text="Hope You Have Understood Now")
        await ctx.send(embed=purge_embed)

    if isinstance(error, commands.MissingPermissions):
        purge_error = discord.Embed(title=f"Error : Missing Permission",
                                    description="Looks Like You Don't Have Required Permission", color=0x00ff00)
        purge_error.add_field(
            name="Permission Requirements :", value="`manage_messages`")

        await ctx.send(embed=purge_error)

    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("I Don't Have Enough Permissions")


@bot.command()
@has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member):
    try:
        await user.kick()
        await ctx.channel.send(f"> ``{user.name} Has Been Kicked`` :eyes:")
    except commands.MissingRequiredArgument:
        await ctx.send("Invalid Format")


@kick.error
async def kick_error(ctx, error):
    randomColor = randint(0, 16777216)
    if isinstance(error, commands.MissingRequiredArgument):
        kick_embed = discord.Embed(
            title="Error : Missing Few Argument", color=randomColor)
        kick_embed.add_field(name="Usage :", value="c!kick @user", inline=True)
        kick_embed.add_field(
            name="Example : ", value="c!kick @KEE6#3362", inline=True)
        kick_embed.set_footer(text="Hope You Have Understood Now")
        await ctx.send(embed=kick_embed)

    if isinstance(error, commands.MissingPermissions):
        error_mp = discord.Embed(title=f"Error : Missing Permission",
                                 description="Looks Like You Don't Have Required Permission", color=0x00ff00)
        error_mp.add_field(name="Permission Requirements :",
                           value="`kick_members`")

        await ctx.send(embed=error_mp)

    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("I Don't Have Permission To Kick Him Out")


@bot.command()
@has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member):
    await user.ban()
    await ctx.channel.send(f"> ``{user.name} Has Been Banned`` :eyes:")


@ban.error
async def ban_error(ctx, error):
    randomColor = randint(0, 16777216)
    if isinstance(error, commands.MissingRequiredArgument):
        ban_embed = discord.Embed(
            title="Error : Missing Few Argument", color=randomColor)
        ban_embed.add_field(name="Usage :", value="c!ban @user", inline=True)
        ban_embed.add_field(name="Example : ",
                            value="c!ban @KEE6#3362", inline=True)
        ban_embed.set_footer(text="Hope You Have Understood Now")
        await ctx.send(embed=ban_embed)

    if isinstance(error, commands.MissingPermissions):
        ban_error = discord.Embed(title=f"Error : Missing Permission",
                                  description="Looks Like You Don't Have Required Permission", color=0x00ff00)
        ban_error.add_field(name="Permission Requirements :",
                            value="`ban_members`")

        await ctx.send(embed=ban_error)

    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("I Don't Have Permissions.")


@bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"> ``Unbanned {user.name}#{user.discriminator}`` :dove:")


@unban.error
async def unban_error(ctx, error):
    randomColor = randint(0, 16777216)
    if isinstance(error, commands.MissingRequiredArgument):
        unban_embed = discord.Embed(
            title="Error : Missing Few Argument", color=randomColor)
        unban_embed.add_field(
            name="Usage :", value="c!unban username#discriminator", inline=True)
        unban_embed.add_field(
            name="Example : ", value="c!unban Byno#5571", inline=True)
        unban_embed.set_footer(text="Hope You Have Understood Now")
        await ctx.send(embed=unban_embed)

    if isinstance(error, commands.MissingPermissions):
        unban_error = discord.Embed(title=f"Error : Missing Permission",
                                    description="Looks Like You Don't Have Required Permission", color=0x00ff00)
        unban_error.add_field(
            name="Permission Requirements :", value="`ban_members`")

        await ctx.send(embed=unban_error)

    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("I Don't Have Permissions.")


@bot.command(pass_context=True)
@has_permissions(ban_members=True)
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    guild = ctx.guild
    if role not in guild.roles:
        await ctx.send("**Creating Muted Role ** <a:loading2:754893493599600642>")
        muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted, send_messages=False)
        role2 = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(role2)
        await ctx.send(f"> ``{member.name} is now muted.`` :eyes:")

    else:
        await member.add_roles(role)
        await ctx.send(f"> ``{member.name} was muted`` :eyes:")


@mute.error
async def mute_error(ctx, error):
    randomColor = randint(0, 16777216)
    if isinstance(error, commands.MissingRequiredArgument):
        mute_embed = discord.Embed(
            title="Error : Missing Few Argument", color=randomColor)
        mute_embed.add_field(name="Usage :", value="c!mute @user", inline=True)
        mute_embed.add_field(
            name="Example : ", value="c!mute @KEE6#3362", inline=True)

        mute_embed.set_footer(text="Hope You Have Understood Now ")
        await ctx.send(embed=mute_embed)

    if isinstance(error, commands.MissingPermissions):
        mute_error = discord.Embed(title=f"Error : Missing Permission",
                                   description="Looks Like You Don't Have Required Permission", color=0x00ff00)
        mute_error.add_field(
            name="Permission Requirements :", value="`ban_members`")

        await ctx.send(embed=mute_error)

    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("I Don't Have Enough Permissions.")


@bot.command(pass_context=True)
@has_permissions(ban_members=True)
async def unmute(ctx, user: discord.Member):
    '''Allows someone to un-shut up. Usage: *unmute [user]'''
    role = discord.utils.get(user.guild.roles, name='Muted')
    await user.remove_roles(role)
    await ctx.channel.send(f"> ``{user.name} can again talk now`` :eyes:")


@unmute.error
async def unmute_error(ctx, error):
    randomColor = randint(0, 16777216)
    if isinstance(error, commands.MissingRequiredArgument):
        unmute_embed = discord.Embed(
            title="Error : Missing Few Argument", color=randomColor)
        unmute_embed.add_field(
            name="Usage :", value="c!unmute @user", inline=True)
        unmute_embed.add_field(
            name="Example : ", value="c!unmute @KEE6#3362", inline=True)
        unmute_embed.set_footer(text="Hope You Have Understood Now")
        await ctx.send(embed=unmute_embed)

    if isinstance(error, commands.MissingPermissions):
        unmute_error = discord.Embed(title=f"Error : Missing Permission",
                                     description="Looks Like You Don't Have Required Permission", color=0x00ff00)
        unmute_error.add_field(
            name="Permission Requirements :", value="`ban_members`")

        await ctx.send(embed=unmute_error)

    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("I Don't Have Enough Permissions.")


@bot.command()
async def serverinfo(ctx):
    """Are you a nerd? Here's some server info."""
    randomColor = randint(0, 16777216)
    guild = ctx.guild
    roles = [x.name for x in guild.roles]
    role_length = len(roles)
    roles = ', '.join(roles)
    channels = len(guild.channels)
    time = str(guild.created_at.strftime("%b %m, %Y, %A, %I:%M %p"))
    em = discord.Embed(
        description="", title='Information About This Server', colour=randomColor)
    em.set_thumbnail(url=guild.icon_url)
    em.add_field(name='__Server __', value=str(guild.name))
    em.add_field(name='__Server ID__', value=str(guild.id))
    em.add_field(name='__Owner__', value=str(guild.owner))
    em.add_field(name='__Owner ID__', value=guild.owner_id)
    em.add_field(name='__Member Count__', value=str(guild.member_count))
    em.add_field(name='__Text/Voice Channels__', value=str(channels))
    em.add_field(name='__Server Region__', value='%s' % str(guild.region))
    em.add_field(name='__ Total Roles__', value='%s' % str(role_length))
    #em.add_field(name='__Roles__', value='%s' % str(roles))
    em.set_footer(text='Created - %s' % time)
    await ctx.send(embed=em)


@bot.command()
async def help(ctx):
    randomColor = randint(0, 16777216)
    eed = discord.Embed(title="List Of commands", color=randomColor)
    eed.add_field(name="# __Moderation__ :hammer_and_wrench: ",
                  value="c!kick, c!ban, c!unban, c!purge/c!clear/c!delete, c!warn, c!userinfo, c!mute, c!unmute", inline=False)
    eed.add_field(name="# __Fun__ :kissing_smiling_eyes: ",
                  value=" c!randomduck, c!randomcat, c!hug, c!kiss, c!spank, c!bite, c!gif", inline=False)
    eed.add_field(name="# __Channel Management__ :blue_heart:  ",
                  value="c!create_hook, c!create_channel, c!delete_channel, c!nuke", inline=False)
    eed.add_field(name="# __Info__ :newspaper: ",
                  value="c!serverinfo, c!userinfo, c!servercount, c!avatar", inline=False)
    eed.add_field(name="# __Other__ :zany_face: ",
                  value="c!google", inline=False)
    eed.add_field(name="# __Having Any Issues ? __", value="c!support")

    await ctx.send(embed=eed)


@bot.command()
async def randomduck(ctx):
    randomColor = randint(0, 16777216)
    request = requests.get("https://random-d.uk/api/random").text
    eedh = discord.Embed(title="Random Duck", color=randomColor)
    eedh.set_image(url=f'{json.loads(request)["url"]}')
    await ctx.send(embed=eedh)


# https://some-random-api.ml/img/cat
@bot.command()
async def randomcat(ctx):
    randomColor = randint(0, 16777216)
    request = requests.get("https://some-random-api.ml/img/cat").text

    eedh = discord.Embed(title="Random Cat", color=randomColor)
    eedh.set_image(url=f'{json.loads(request)["link"]}')
    await ctx.send(embed=eedh)

@bot.command(aliases=['GS', 'Google', 'Search', 'GSearch'])
async def google(ctx, *, arg=None):
    randomColor = randint(0, 16777216)
    if arg is None:
        google_embed = discord.Embed(
            title="Error : Missing Few Argument", color=randomColor)
        google_embed.add_field(
            name="Usage :", value="c!google query", inline=True)
        google_embed.add_field(
            name="Examples : ", value="c!google Temperature Of New York \nc!google Who is John Cena\nc!google Meaning of Lmao", inline=True)
        google_embed.set_footer(text="Hope You Have Understood Now")
        await ctx.send(embed=google_embed)

    randomColor = randint(0, 16777216)
    fix = arg.replace(" ", "+")
    url = f"https://www.google.com/search?&q={fix}"
    req = requests.get(url)
    sor = BeautifulSoup(req.text, "html.parser")
    temp = sor.find("div", class_='BNeawe')
    # await ctx.send(temp)
    emyd = discord.Embed(
        title=f"__Direct Google Search__",
        description=f"{temp.text}",
        color=randomColor
    )

    # emyd.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg")
    await ctx.send(embed=emyd)

@bot.command()
async def avatar(ctx, avamember: discord.Member = None):
    # Optimised Code
    if avamember is None:
        avatar_ref = ctx.message.author
    else:
        avatar_ref = avamember
    await ctx.send(avatar_ref.avatar)

@bot.command()
async def invite(ctx):
    randomColor = randint(0, 16777216)
    eppf = discord.Embed(title="You Can Add Me From This Link",
                         description='https://discord.com/api/oauth2/authorize?client_id=699489920854786089&permissions=15438961820&scope=bot', color=randomColor)
    await ctx.send(embed=eppf)


@bot.command(pass_context=True)
@has_permissions(manage_roles=True)
async def role(ctx, user: discord.Member, role: discord.Role):
    if role in user.roles:
        await user.remove_roles(role)
        await ctx.send(f"> ``Role Removed For {user.name}``  : `` {role.name}`` :eyes:")
    else:
        await user.add_roles(role)
        await ctx.send(f"> ``Role Added From {user.name}``  : `` {role.name}`` :eyes:")


@role.error
async def role_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        randomColor = randint(0, 16777216)
        embed_role_error = discord.Embed(title="Command: c!role",
                                         description="Error: You Are Missing An Argument",
                                         color=randomColor
                                         )
        embed_role_error.add_field(
            name="Usage", value="c!role @user @role", inline=True)
        embed_role_error.add_field(
            name="Example", value="c!role @DREAM TX#4263 @BEST_BOT", inline=True)
        await ctx.send(embed=embed_role_error)


@bot.command()
async def bite(ctx, user: discord.Member):
    randomColor = randint(0, 16777216)
    aur = ctx.message.author.name
    bite_gif = ["https://media.tenor.com/images/8b92d18c857f1f16ff53095ee0adaeb2/tenor.gif", "https://media.tenor.com/images/b60d919b812adae2d475b23a5124b64d/tenor.gif", "https://media1.tenor.com/images/5d3547b13131fffcf278ccfafe08efe0/tenor.gif?itemid=16834570", "https://media1.tenor.com/images/a96d558385c8dba74ffb09593c0e2860/tenor.gif?itemid=13418531",
                "https://media1.tenor.com/images/bdab052143028c31203bc4d8a7416ef6/tenor.gif?itemid=11674205", "https://media1.tenor.com/images/c22a247affcf4cd02c7d17f5a432cd95/tenor.gif?itemid=8259627", "https://media1.tenor.com/images/428f2a7ca42cf1a28c3362c4e42e8ce2/tenor.gif?itemid=12858112"]
    bite_embed = discord.Embed(
        title=f"{aur} Bites {user.name}",
        description="",
        color=randomColor
    )
    bite_embed.set_image(url=f"{random.choice(bite_gif)}")
    bite_embed.set_footer(text="GIF By Tenor")

    await ctx.send(embed=bite_embed)

@bot.command()
async def spank(ctx, user: discord.Member):
    randomColor = randint(0, 16777216)
    aur = ctx.message.author.name
    spank_gif = ["https://media1.tenor.com/images/ea6efd709845f2f80f12880e22f32c5d/tenor.gif?itemid=5769175", "https://media1.tenor.com/images/ea1c4907066591b3682989bc9b2ee8d4/tenor.gif?itemid=15351538", "https://media1.tenor.com/images/b9f5a6cba4a49bf3d316c200052d388f/tenor.gif?itemid=15782569",
                 "https://media1.tenor.com/images/e616ed8512cda0115dc8a03d8194ce7e/tenor.gif?itemid=16132466", "https://media1.tenor.com/images/599b33016df446858084136b12fba5c4/tenor.gif?itemid=17001571", "https://media1.tenor.com/images/ef5f040254c2fbf91232088b91fe2341/tenor.gif?itemid=13569259", "https://media1.tenor.com/images/d40977fe97c6c94215a9b84f990357f7/tenor.gif?itemid=7391212"]
    spank_embed = discord.Embed(
        title=f"{aur} Hurted {user.name} :(",
        description="",
        color=randomColor
    )
    spank_embed.set_image(url=f"{random.choice(spank_gif)}")
    spank_embed.set_footer(text="Gif By Tenor")

    await ctx.send(embed=spank_embed)

@spank.error
async def spank_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Mention The User To Spank Him ```Format :- c!spank (@mention)``` ```Example :- c!spank @ME66#5253```")


@bite.error
async def bite_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Mention The User To Bite Him ```Format :- c!bite (@mention)``` ```Example :- c!bite @ME66#5253```")
ctx.send("Mention The User To Kick Him As Fun ```Format :- c!funkick (@mention)``` ```Example :- c!funkickio @ME66#5253```")


@bot.command()
async def create_hook(ctx):
    await ctx.send("> ``Enter Name Of Webhook`` :eyes:")
    msg = await bot.wait_for('message', timeout=60)
    hook = ctx.channel
    remsg = msg.content
    web = await hook.create_webhook(name=f'{remsg}')
    await ctx.send(f"> ``Webhook Created`` :eyes: :smile:\n\n``Name : {remsg}``\n\n``Webhook Url ``: {web.url}")


@bot.command()
@has_permissions(manage_channels=True)
async def create_channel(ctx):
    await ctx.send("Enter Name Of Channel (Without #)")
    channl = await bot.wait_for('message', timeout=60)
    guild = ctx.message.guild
    await guild.create_text_channel(f'{channl.content}')
    await ctx.send("> ``Channel SucceFully Created`` :eyes:")


@create_channel.error
async def create_channel_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        cc_error = discord.Embed(title=f"Error : Missing Permission",
                                 description="Looks Like You Don't Have Required Permission", color=0x00ff00)
        cc_error.add_field(name="Permission Requirements :",
                           value="`manage_channels`")

        await ctx.send(embed=cc_error)


@bot.command()
@has_permissions(manage_channels=True)
async def delete_channel(ctx):
    guild = ctx.message.guild
    await ctx.send("Enter Name Of Channel (Without #)")
    channl = await bot.wait_for('message', timeout=60)
    channl_name = channl.content
    guild = ctx.message.guild
    channel = discord.utils.get(guild.text_channels, name=f"{channl_name}")
    await channel.delete()
    await ctx.send("> ``Channel SuccesFully Deleted`` :eyes:")


@delete_channel.error
async def delete_channel_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Channel Not Found \nMake Sure Channel name is exact same in the guild \nDon't Use # in channel name")
    if isinstance(error, commands.MissingPermissions):
        dc_error = discord.Embed(title=f"Error : Missing Permission",
                                 description="Looks Like You Don't Have Required Permission", color=0x00ff00)
        dc_error.add_field(name="Permission Requirements :",
                           value="`manage_channels`")

        await ctx.send(embed=dc_error)


@bot.command()
@has_permissions(manage_channels=True)
async def nuke(ctx):
    guild = ctx.message.guild
    dtf = ctx.channel.name
    channel = discord.utils.get(guild.text_channels, name=f"{dtf}")
    await channel.delete()
    await guild.create_text_channel(f'{dtf}', category=ctx.channel.category)
    nuked = discord.utils.get(guild.text_channels, name=f"{dtf}")
    xxy = await nuked.send("``Nuked This Channel SuccessFully`` \nhttps://tenor.com/view/destory-eexplode-nuke-gif-6073338")
    await asyncio.sleep(5)
    await xxy.delete()


@nuke.error
async def nuke_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        nuke_error = discord.Embed(title=f"Error : Missing Permission",
                                   description="Looks Like You Don't Have Required Permission", color=0x00ff00)
        nuke_error.add_field(
            name="Permission Requirements :", value="`manage_channels`")

        await ctx.send(embed=nuke_error)


@bot.command()
async def support(ctx):
    await ctx.send("https://discord.gg/GV5Ejuy")

#  AUTOMATIC DISCORD LINK PREVENTION & EMOJI GETTER
@bot.event
async def on_message(message):
    randomColor = randint(0, 16777216)
    if "discord.gg" in message.content.lower():
        if message.author.guild_permissions.administrator == False:

            await message.delete()
            link_embed = discord.Embed(
                title=f"No Advertising Allowed", description=f"{message.author.mention} You cannot send links Here  :eyes:")
            link_embed.set_footer(
                text="Note : Only server owner/admins can send links")
            await message.channel.send(embed=link_embed)
        else:
            print("Admin Sent A Link")
            
	# Not Working Properly Now
    # elif "--" in message.content.lower():
    #     await message.delete()
    #     msg = message.content.replace("--", "")
    #     emote = discord.utils.get(bot.emojis, name=f'{msg}')
    #     autor = message.author.name
    #     emoteembed = discord.Embed(
    #         title=f'**{autor}**', description=f'{emote}', colour=randomColor)
    #     # embed.set_footer(text="Made By ❰Mℜ. MOD̷丂❱ #2577")
    #     await message.channel.send(embed=emoteembed)
    # await bot.process_commands(message)

# Not Working Now
# @bot.command()
# async def ascii(ctx, *, text):
#     r = requests.get(f"https://artii.herokuapp.com/make?text={text}")
#     sor = BeautifulSoup(r.text, "html.parser")
#     await ctx.send(f"```{sor}```")


@bot.command()
async def gif(ctx, *, text):
    
    t = TenGiphPy.Tenor(token=tenor_token)
    gif_link = t.random(f"{text}")
    gif_embed = discord.Embed(title=f"GIF Search By {ctx.author.name}")
    gif_embed.set_image(url=gif_link)
    gif_embed.set_footer(text="GIF By Tenor")
    await ctx.send(embed=gif_embed)


@gif.error
async def gif_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        randomColor = randint(0, 16777216)
        gif_embed = discord.Embed(
            title="Error : Missing Few Argument", color=randomColor)
        gif_embed.add_field(name="Usage :", value="c!gif <text>", inline=True)
        gif_embed.add_field(name="Example : ",
                            value="c!gif party", inline=True)
        gif_embed.set_footer(text="Hope You Have Understood Now")
        await ctx.send(embed=gif_embed)

# Not Working Now
# @ascii.error
# async def ascii_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         randomColor = randint(0, 16777216)
#         ascii_embed = discord.Embed(
#             title="Error : Missing Few Argument", color=randomColor)
#         ascii_embed.add_field(
#             name="Usage :", value="c!ascii <text>", inline=True)
#         ascii_embed.add_field(
#             name="Example : ", value="c!ascii james", inline=True)
#         ascii_embed.set_footer(text="Hope You Have Understood Now")
#         await ctx.send(embed=ascii_embed)

# Test Bot
# -> Run Here

# Orginal Bot
bot.run(token)
