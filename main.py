import json
import os
import discord
from discord.ext import tasks, commands #adding the commands ext for cleaner code and slash commands
from discord.ui import Button, View
from discord.utils import find
import topgg
import asyncio
from datetime import datetime, timezone, timedelta#y for yes so it will respond with yes to all of the prompts
#from discord.commands import Option
##### VARIABLES ###############
blocked_json_filename = "/root/AntiScammer/blocked.json"
scammers_json_filename = "/root/AntiScammer/scammers.json"  
admin_json_filename = "/root/AntiScammer/admins.json"
BotOwner = 0
 
###############################
intents = discord.Intents.default()
client = commands.Bot(intents=intents, command_prefix="/") # use the discord bot class with the command prefix ! with the correct intents
client.remove_command("help")
dbl_token = ("Top.gg Token here") 
client.topggpy = topgg.DBLClient(client, dbl_token)
now = datetime.now(tz=timezone.utc)
until = now + timedelta(weeks=1)
 
 
# check the blocked json
with open(blocked_json_filename, 'r') as blocked_file:
    blocked_list = json.load(blocked_file)
# check the admin json
with open(admin_json_filename, 'r') as admin_file:
    admin_list = json.load(admin_file)
 
async def check_admin(some_member):
    with open(admin_json_filename, 'r') as admin_file:
        admin_list = json.load(admin_file)
    for i in admin_list["admins"]:
        if int(i) == some_member.id:
            return True
    return False 
 
 
@client.event
async def on_ready():
    # says hello in terminal
    print('Ready. Logged as {0.user}'.format(client))
    print('Currently in '+str(len(client.guilds))+' servers')
 
    
  
    
@client.slash_command(description="Only for AntiScammer Admins")
async def remove(ctx,url):
    # check the blocked json
    with open(blocked_json_filename, 'r') as blocked_file:
        blocked_list = json.load(blocked_file)
    if not await check_admin(ctx.author):
        embed=discord.Embed(title="Access Denied", color=0xdf0707)
        embed.add_field(name="You don't have the sufficient permissions to use this command.", value="\u200b", inline=False)
        embed.set_footer(text="AntiScammer Admin Menu")
        await ctx.respond(embed=embed, ephemeral=True)
        return
    if url not in blocked_list['blockedURLs']:
        embed=discord.Embed(title="Error", color=0xdf0707)
        embed.add_field(name="That URL isn't blocked.", value="\u200b", inline=False)
        embed.set_footer(text="AntiScammer Admin Menu")
        await ctx.respond(embed=embed, ephemeral=True)
        return
    blocked_list['blockedURLs'].remove(url)
    with open(blocked_json_filename, 'w') as blocked_file:
        json.dump(blocked_list, blocked_file)
            
            # notify that everything worked
    embed=discord.Embed(title="Successfully Removed", color=0x23e515)
    embed.add_field(name=url, value="\u200b", inline=False)
    embed.set_footer(text="AntiScammer Admin Menu")
    await ctx.respond(embed=embed, ephemeral=True)
    return
 

@client.event
async def on_message(message):
    # check the blocked json
    with open(blocked_json_filename, 'r') as blocked_file:
        blocked_list = json.load(blocked_file)
    if message.author == client.user:
        return
    for i in blocked_list['blockedURLs']:
        if i in str(message.content).lower():
            await message.delete()
            print('Message deleted')
            await message.Channel.send(message.author.mention + " just sent a scam link, shame on them.")
            print('Message sendt')
            print('Adding muted role')
            # adds the role
            await message.author.timeout(until, reason="Posted a scam link")


            # adds to the scammer list # This is 2
            with open(scammers_json_filename, 'r') as scammers_file:
                scammers_list = json.load(scammers_file)


            if message.author.id in scammers_list['scammers']:
                return

            scammers_list['scammers'].append(after.author.id)
            with open(scammers_json_filename, 'w') as scammers_file:
                json.dump(scammers_list, scammers_file)
            print('Added to scammers.json')

    await client.process_commands(message)
    
 
 
    
@client.slash_command(description="Shows you the credits")
 
async def credits(ctx): 
    embed=discord.Embed(title="Credits")
    embed.add_field(name="Kf637", value="Developer", inline=False)
    embed.add_field(name="spnemanja", value="Developer", inline=False)
    await ctx.respond(embed=embed, ephemeral=True)
    return

@client.slash_command(description="Invite to the support server")
 
async def support(ctx): 
    button = discord.ui.Button(style=4, label="Join the support server", url="https://discord.gg/A4stGpE5tR")
    embed=discord.Embed(title="Support Server Invite", color=0x1281e2)
    view = discord.ui.View()
    view.add_item(button)
    await ctx.respond(embed=embed, view=view, ephemeral=True)
    return

@client.slash_command(description="Only for AntiScammer Admins")
 
async def addadmin(ctx,userid):  
    with open(admin_json_filename, 'r') as admin_file:
        admin_list = json.load(admin_file)
 
    if not ctx.author.id == 515402023223427072:
        return
    if userid in admin_list['admins']:
        embed=discord.Embed(title="Error", color=0xdf0707)
        embed.add_field(name='That user is already an administrator.', value=":x:", inline=False)
        embed.set_footer(text="AntiScammer Admin Menu")
        await ctx.respond(embed=embed, ephemeral=True)
        return
    
    admin_list['admins'].append(int(userid))
    with open(admin_json_filename, 'w') as admin_file:
        json.dump(admin_list, admin_file)

    # notify that everything worked
    embed=discord.Embed(title="Successfully Added Administrator", color=0x23e515)
    embed.add_field(name='ID: '+userid, value='<@'+userid+'> has been added as an administrator', inline=False)
    embed.set_footer(text="AntiScammer Admin Menu")
    await ctx.respond(embed=embed, ephemeral=True)
    return
 
@client.slash_command(description="Only for AntiScammer Admins")
 
async def removeadmin(ctx,userid):
    with open(admin_json_filename, 'r') as admin_file:
        admin_list = json.load(admin_file)
    if not ctx.author.id == 515402023223427072:
        return
    print(userid)
    if int(userid) not in admin_list['admins']:
        embed=discord.Embed(title="Error", color=0xdf0707)
        embed.add_field(name='That user is not an administrator.', value="\u200b", inline=False)
        embed.set_footer(text="AntiScammer Admin Menu")
        await ctx.respond(embed=embed, ephemeral=True)
        return
    print("Removing admin")
    print(admin_list['admins'])
    admin_list['admins'].remove(int(userid))
    with open(admin_json_filename, 'w') as admin_file:
        json.dump(admin_list, admin_file)
        print("Admin Removed, Sending message")

    # notify that everything worked
    embed=discord.Embed(title="Successfully Removed Administrator", color=0x23e515)
    embed.add_field(name='ID: '+userid, value='<@'+userid+'> has been removed as an administrator', inline=False)
    embed.set_footer(text="AntiScammer Admin Menu")
    await ctx.respond(embed=embed, ephemeral=True)
    print("Message has been sent")
    return
@client.slash_command(description="Invite")
 
async def invite(ctx):
    button = discord.ui.Button(style=4, label="Invite me!", url='https://discord.com/api/oauth2/authorize?client_id=762478293743435837&permissions=1099511639040&scope=bot%20applications.commands')
    embed=discord.Embed(title="Invite", description="Want AntiScammer on your server? Click on the button below")
    embed.set_author(name=ctx.author.name)
    embed.set_footer(text="AntiScammer Invite Menu")
    view = discord.ui.View()
    view.add_item(button)
    await ctx.respond(embed=embed, view=view, ephemeral=True)
    return
 

      
 
 
 
 
        
 
@client.slash_command(description="Used for reporting new scam links")
async def report(ctx):
    button = discord.ui.Button(style=4, label="Report now", url="https://forms.gle/6PxuoH1euaPbhSQ68")
    embed=discord.Embed(title="Scam Report", description="Found a scam link? Report it and we'll review the report")
    embed.set_author(name=ctx.author.name)
    embed.set_footer(text="AntiScammer")
    view = discord.ui.View()
    view.add_item(button)
    await ctx.respond(embed=embed, view=view, ephemeral=True)
    return
@client.slash_command(description="Server counter") 
async def servercount(ctx):
    embed=discord.Embed(title="Server Count", url="", description='Currently in **'+str(len(client.guilds))+'** servers')
    embed.set_author(name=ctx.author.name)
    embed.set_footer(text="AntiScammer")
    await ctx.respond(embed=embed, ephemeral=True)
    return
@client.slash_command(description="Feedback link")
async def feedback(ctx):
    button = discord.ui.Button(style=4, label="Open Link", url="https://antiscammer-feedback.nolt.io")
    embed=discord.Embed(title="AntiScammer Feedback", description="Here can you give feedback, suggestions and bug reports")
    embed.set_author(name=ctx.author.name)
    embed.set_footer(text="AntiScammer")
    view = discord.ui.View()
    view.add_item(button)
    await ctx.respond(embed=embed, view=view, ephemeral=True)
    return

 
@client.slash_command(description="Shows you the bot's commands")
async def help (ctx):
        embed=discord.Embed(title="Commands", color=0x1281e2)
        embed.set_author(name=ctx.author.name)
        embed.add_field(name="/invite", value="Let's you add the bot to other servers", inline=False)
        embed.add_field(name="/report", value="Will send you a forum where you can report a new scam link ", inline=False)
        embed.add_field(name="/help", value="Shows this menu", inline=False)
        embed.add_field(name="/servercount", value="Shows you how many servers the bot is in", inline=False)
        embed.add_field(name="/credits", value="Shows you who made this bot", inline=False)
        embed.add_field(name="/info", value="Shows you some basic info about the bot", inline=False)
        embed.add_field(name="/support", value="Gives you an invite to our support server", inline=False)
        embed.add_field(name="/feedback", value="Gives you a link where you can give feedback, suggestions and bug reports", inline=False)
        embed.set_footer(text="AntiScammer")
        await ctx.respond(embed=embed, ephemeral=True)
        return

@client.slash_command(description="Only for AntiScammer Admins")
async def add(ctx,url):
    # check the blocked json
    with open(blocked_json_filename, 'r') as blocked_file:
        blocked_list = json.load(blocked_file)
    if not await check_admin(ctx.author):
        embed=discord.Embed(title="Access Denied", color=0xdf0707)
        embed.add_field(name="You don't have the sufficient permissions to use this command.", value="\u200b", inline=False)
        embed.set_footer(text="AntiScammer Admin Menu")
        await ctx.respond(embed=embed, ephemeral=True)
        return
    blocked_list['blockedURLs'].append(url)
    with open(blocked_json_filename, 'w') as blocked_file:
        json.dump(blocked_list, blocked_file)
            
            # notify that everything worked
    embed=discord.Embed(title="Successfully Added", color=0x23e515)
    embed.add_field(name=url, value="\u200b", inline=False)
    embed.set_footer(text="AntiScammer Admin Menu")
    await ctx.respond(embed=embed, ephemeral=True)
    return
  
@client.slash_command(description="Only for AntiScammer Admins")
async def admincommands(ctx):
        embed=discord.Embed(title="Admin Commands", color=0x1281e2)
        embed.set_author(name=ctx.author.name)
        embed.add_field(name="/add", value="Let's you add URL's to the blacklist, use /addexample if you are new before adding", inline=False)
        embed.add_field(name="/remove", value="Will remove a scam link from the blacklist ", inline=False)
        embed.add_field(name="/addexample", value="Shows you how to use the /add command", inline=False)
        embed.set_footer(text="AntiScammer Admin Commands")
        await ctx.respond(embed=embed, ephemeral=True)
        return
 

@client.slash_command(description="Only for AntiScammer Admins")
async def addexample(ctx):
    
     embed=discord.Embed(title="Example Command", color=0x1281e2)
     embed.set_author(name=ctx.author.name)
     embed.add_field(name="Example for /add command", value="Dicord.gg, roblox.com, goggle.com", inline=False)
     embed.add_field(name="Don't do", value="https://discord.gg/, https://discord.gg/, https://youtube.com/, discord.gg/ roblox.com/", inline=False)
     embed.add_field(name="Info", value="If you include the https, http or the /, the bot will not recognize the link as it can be easily bypassed ", inline=False)
     embed.set_footer(text="AntiScammer Admin Commands")
     await ctx.respond(embed=embed, ephemeral=True)

@client.slash_command(description="Fun Command")
async def tank(ctx):

     embed=discord.Embed(title="Long Tank", color=0x1281e2)
     embed.add_field(name="\u200b", value='    [░░░░░███████]▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▃\n▂▄▅████████████████████▅▄▃▂\nI█████████████████████████████]\n◥⊙▲⊙▲⊙▲⊙▲⊙▲⊙▲⊙▲⊙▲⊙▲⊙◤', inline=False)
     embed.set_footer(text="Made for PC")
     await ctx.respond(embed=embed,ephemeral=True)

    



@client.event
async def on_message_edit(before,after):
    for i in blocked_list['blockedURLs']:
        if i in str(after.content).lower():
            await after.delete()
            print('Message deleted')
            await after.Channel.send(after.author.mention + " just sent a scam link, shame on them.")
            print('Message sendt')
            # adds the role
            await after.author.timeout(until, reason="Posted a scam link (Auto Timeout)")


            # adds to the scammer list # This is 2
            with open(scammers_json_filename, 'r') as scammers_file:
                scammers_list = json.load(scammers_file)


            if after.author.id in scammers_list['scammers']:
                return

            scammers_list['scammers'].append(after.author.id)
            with open(scammers_json_filename, 'w') as scammers_file:
                json.dump(scammers_list, scammers_file)
            print('Added to scammers.json')

@client.slash_command(description="Only for AntiScammer Admins")
 
async def shutdown(ctx):  
    if not ctx.author.id == BotOwner:
        embed=discord.Embed(title="Access Denied", color=0xdf0707)
        embed.add_field(name="You don't have the sufficient permissions to use this command.", value="\u200b", inline=False)
        embed.set_footer(text="AntiScammer Admin Menu")
        await ctx.respond(embed=embed, ephemeral=True)
        return
      
    if ctx.author.id == BotOwner:
        embed5=discord.Embed(title="Shutting Down in 5 seonds", color=0x8)
        embed4=discord.Embed(title="Shutting Down in 4 seonds", color=0xdf0707)
        embed3=discord.Embed(title="Shutting Down in 3 seonds", color=0x8)
        embed2=discord.Embed(title="Shutting Down in 2 seonds", color=0xdf0707)
        embed1=discord.Embed(title="Shutting Down in 1 seonds", color=0x8)
        embed0=discord.Embed(title="Shutting Down!", color=0xdf0707)
        embed0.add_field(name="AntiScammer is now shutting down", value="\u200b", inline=False)
        await ctx.respond(embed=embed5)
        await asyncio.sleep(1)
        await ctx.edit(embed=embed4)
        await asyncio.sleep(1)
        await ctx.edit(embed=embed3)
        await asyncio.sleep(1)
        await ctx.edit(embed=embed2)
        await asyncio.sleep(1)
        await ctx.edit(embed=embed1)
        await asyncio.sleep(1)
        await ctx.edit(embed=embed0)
        await exit()
        return

@tasks.loop(minutes=1)
async def update_stats():
    #This function runs every 1 minute to automatically update your server count.
    try:
        await client.topggpy.post_guild_count()
        print(f"Posted server count ({client.topggpy.guild_count})")
        await asyncio.sleep(60)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=str(len(client.guilds))+' servers'))
        await asyncio.sleep(30)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="AntiScammer is online 24/7"))
    except Exception as e:
        print(f"Failed to post server count\n{e.__class__.__name__}: {e}")
 
        await asyncio.sleep(60)
    
update_stats.start()
            
@client.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general',  guild.text_Channels)
    if general and general.permissions_for(guild.me).send_messages:
        embed=discord.Embed(title="Thanks for adding AntiScammer!")
        embed.add_field(name="AntiScammer is here to protect Discord server against scammers.", value="\u200b", inline=True)
        embed.add_field(name="Every message send is scanned for any scam links and if any where to be detected then the message would be deleted and the sender receive a timeout.", value="\u200b", inline=True)
        await general.send(embed=embed)

client.run("TOKEN HERE")
