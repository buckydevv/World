import discord
import datetime
from discord.ext import commands
import asyncio

world_pfp = ("https://cdn.discordapp.com/attachments/727241613901824563/764885646162395156/world.png")

class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.snipeCache = {}
        self.editSnipeCache = {}

    @commands.command(help="Ban a user.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        em = discord.Embed(title="The Ban Hammer Has Rised!<")
        em.description = (f"{ctx.author.mention} Has Banned {member}")
        em.add_field(name=f"**Ban Hammer**", value=f'Banned By {ctx.author.mention}', inline=False)
        em.set_thumbnail(url='https://cdn.discordapp.com/attachments/717867181827817984/719525512715960350/s.png')
        em.colour = (0xFF0000)
        await ctx.send(embed=em)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/ban <member> <reason>`")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f':regional_indicator_x: Sorry {ctx.author.mention} You Do Not Have Perms To Ban People!')

    @commands.command(help="Kick a user.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        em = discord.Embed(title="The Kick Machine Has Awoken")
        em.description = (f"{ctx.author.mention} Has Kicked {member}")
        em.add_field(name=f"**Kick Machine**", value=f'Kicked By {ctx.author.mention}', inline=False)
        em.set_thumbnail(url='https://cdn.discordapp.com/attachments/546331074876145666/719526555587575919/a.png')
        em.colour = (0xFF0000)
        await ctx.send(embed=em)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/kick <member> <reason>`")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f':regional_indicator_x: Sorry {ctx.author.mention} You Do Not Have Perms To Kick People!')

    @commands.command(help="Mute a user.")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: discord.Member, *, reason=None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        mute = discord.utils.get(ctx.guild.text_channels, name="MUTED-TIME-OUT")
        if not role:
            try:
                global muted
                muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
                for channel in ctx.guild.channels:
                    await channel.set_permissions(muted, send_messages=False,
                                                read_message_history=False,
                                                read_messages=False)
            except discord.Forbidden:
                return await ctx.send("I have no permissions to make a muted role!")
            await user.add_roles(muted)
            mute1 = discord.Embed(title = f"{user} has been Muted | Reason = {reason}", color =0x2F3136)
            await ctx.send(embed=mute1)
        else:
            await user.add_roles(role)
            mute = discord.Embed(title = f"{user} has been Muted | Reason = {reason}", color =0x2F3136)
            await ctx.send(embed=mute)
       
        if not mute:
            overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_message_history=False),
                        ctx.guild.me: discord.PermissionOverwrite(send_messages=True),
                        muted: discord.PermissionOverwrite(read_message_history=True)}
            try:
                channel = await ctx.create_channel('MUTED-TIME-OUT', overwrites=overwrites)
                await channel.send("Welcome to Hell You will spend your time here until you get unmuted")
            except discord.Forbidden:
                return await ctx.send("I have no permissions to make #MUTED-TIME-OUT")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(':regional_indicator_x: Sorry you dont have permissions to do this!')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/mute <member> <reason>`")

    @commands.command(help="Delete specified messages.")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        if amount >= 100:
            return await ctx.send(f":regional_indicator_x: Sorry {ctx.author.mention} `100` is max limit.")
        if amount <= 1:
            return await ctx.send(f":regional_indicator_x: Sorry {ctx.author.mention} Please purge more than `1` message")
        else:
            await ctx.channel.purge(limit=amount)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'Sorry {ctx.author.mention} Please Type `w/purge <amount>')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f':regional_indicator_x: Sorry {ctx.author.mention} You Do Not Have The Role Perm: `manage messages`!')
        

    @commands.command(help="Unban a user.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user 

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                em = discord.Embed(title="Someone Has Used The Unban Hammer!")
                em.description = (f"{ctx.author.mention} Has UnBanned {user.name}#{user.discriminator}")
                em.add_field(name=f"**UnBan Hammer**", value=f'UnBanned By {ctx.author.mention}', inline=False)
                em.set_thumbnail(url='https://cdn.discordapp.com/attachments/717867181827817984/719525512715960350/s.png')
                em.colour = (0x2F3136)
                await ctx.send(embed=em)
                return

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f':regional_indicator_x: Sorry {ctx.author.mention} You Dont Have Perms Or This Person Cannot Be Unbanned')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/unban <member>`")

    @commands.command(help="Start a Poll.")
    @commands.has_permissions(ban_members=True)
    async def poll(self, ctx, *, desc):
        await ctx.send('@here NEW POLE VOTE TO TAKE PART!')
        embed = discord.Embed(
            colour = 0x2F3136
        )
        embed.set_author(name=f"New Poll Vote To Take Part", icon_url=ctx.author.avatar_url)
        embed.description = (f'{ctx.author.mention} Has Started A New Poll')
        embed.add_field(name="World | Poll - Question", value=f"`POLL:` **{desc}**", inline=False)
        embed.set_footer(text="👍 for Yes, 👎 for No.")
        add_reactions_to = await ctx.send(embed=embed)
        await add_reactions_to.add_reaction("👍")
        await add_reactions_to.add_reaction("👎")

    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(':regional_indicator_x: Sorry you dont have permissions to do this!')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/poll <description>`")

    @commands.command(help="Start a Poll.")
    @commands.has_permissions(ban_members=True)
    async def polln(self, ctx, *, desc):
        embed = discord.Embed(
            colour = 0x2F3136
        )
        embed.set_author(name=f"New Poll Vote To Take Part", icon_url=ctx.author.avatar_url)
        embed.description = (f'{ctx.author.mention} Has Started A New Poll')
        embed.add_field(name="World | Poll - Question", value=f"`POLL:` **{desc}**", inline=False)
        embed.set_footer(text="👍 for Yes, 👎 for No.")
        add_reactions_to = await ctx.send(embed=embed)
        await add_reactions_to.add_reaction("👍")
        await add_reactions_to.add_reaction("👎")

    @polln.error
    async def polln_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/polln <description>`")

    @commands.command(help="Lockdown the current channel.")
    @commands.has_permissions(ban_members=True)
    async def lock(self, ctx):
        guild = ctx.guild
        await ctx.message.channel.set_permissions(guild.default_role,read_messages = True, send_messages = False)
        embed = discord.Embed(title="World - Lockdown")
        embed.add_field(name="**INFO:**", value=f"🔒 Channel locked.")
        embed.add_field(name="**Requested By**", value=f"{ctx.author.mention}")
        embed.color = (0x2F3136)
        await ctx.send(embed=embed)




    @commands.command(help="Nuke a specified channel.")
    @commands.has_permissions(manage_messages=True)
    async def nuke(self, ctx, channel=None):
    	channel = channel or ctx.channel
    	nuke_ = discord.Embed(
    		title="Nuke",
    		description=f"Would you like to nuke `{channel}`?\nThis will delete the channel and remake it.",
    		color=0x2F3136
    		)

    	nuke_fail = discord.Embed(
    		title="Nuke Failed",
    		description=f"You Chose not to nuke `{channel}`",
    		color=0x2F3136
    		)

    	message = await ctx.send(embed=nuke_)

    	await message.add_reaction('✅')
    	await message.add_reaction('❎')

    	emoji = ''

    	while True:
    		if emoji=='✅':
    			try:
    				await channel.delete()
    				nuked_channel = await channel.clone()
    				message_ = self.bot.get_channel(nuked_channel.id)
    				await message_.send(f"{ctx.author.mention} <#{nuked_channel.id}> was nuked.\nhttps://tenor.com/view/explosion-explode-clouds-of-smoke-gif-17216934")
    				break
    			except Exception as e:
    				embed = discord.Embed(title="Error:", description=e, color=0x2F3136)
    				return await ctx.send(embed=embed)
    		if emoji=='❎':
    			await message.edit(embed=nuke_fail)
    			break

    		res = await self.bot.wait_for('reaction_add', check=lambda r, u: u.id == ctx.author.id and r.message.id == message.id, timeout=15)
    		if res==None:
    			break
    		if str(res[1])!='Luffy#0728':
    			emoji=str(res[0].emoji)

    	await message.clear_reactions()
        
    @nuke.error
    async def nuke_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f':regional_indicator_x: Sorry {ctx.author.mention} You Do Not Have The Role Permission: `manage messages`!')

 
    @commands.command(help="Unlock the current channel.")
    @commands.has_permissions(ban_members=True)
    async def unlock(self, ctx):
        guild = ctx.guild
        await ctx.message.channel.set_permissions(guild.default_role,read_messages = True, send_messages = True)
        embed = discord.Embed(title="World- Lockdown Over")
        embed.add_field(name="**INFO:**", value=f"🔒 Channel unlocked.")
        embed.add_field(name="**Requested By**", value=f"{ctx.author.mention}")
        embed.color = (0x2F3136)
        await ctx.send(embed=embed)

    @commands.command(help="Set the slowmode of the channel.")
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, seconds: int):
        if seconds >= 21600:
            return await ctx.send(f":regional_indicator_x: Sorry {ctx.author.mention} 21600 is max slowmode range.")
        await ctx.message.channel.edit(slowmode_delay=seconds)
        embed = discord.Embed(title="Slowmode",
            description=f"I have set the slowmode for <#{ctx.message.channel.id}> to `{seconds}`",
            color=0x2F3136)
        await ctx.send(embed=embed)

    @commands.command(help="Unmute a member")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: discord.Member, *, reason=None):
        if user == ctx.author:
            return await ctx.send("You can't unmute yourself")
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            return await ctx.send("How can I unmute a member if there's no Muted role ?")
        if not discord.utils.find(lambda role: role.name == "Muted", user.roles):
            return await ctx.send(f"**{user.name}** is already unmuted!")
        await user.remove_roles(role)
        mute1 = discord.Embed(title = f"{user} has been unmuted! | Reason = {reason}", color =0x2F3136)
        return await ctx.send(embed=mute1)

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/unmute <member> <reason>`")

    @slowmode.error
    async def slowmode_error(self, ctx, error):
        await ctx.send(f":regional_indicator_x: Sorry {ctx.author.mention} `{error}`")
   
    @lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f':regional_indicator_x: Sorry {ctx.author.mention} This Command Can Only Be Used By Admins') 
        
    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f':regional_indicator_x: Sorry {ctx.author.mention} This Command Can Only Be Used By Admins')

    @commands.command(help="Direct message a user.")
    @commands.cooldown(rate=1, per=20, type=commands.BucketType.member)
    @commands.has_permissions(administrator=True)
    async def dm(self, ctx, member : discord.Member, *, msg):
        embed = discord.Embed(description=f"World - Direct Message", timestamp=ctx.message.created_at)
        embed.add_field(name="Direct Message", value=f"{ctx.author.mention} Sent A Message To {member}\n Message: \n `{msg}`")
        embed.set_author(name="Succsesfully Sent Direct Message", icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/717029914360020992/730135115673370684/contest1replace.png")
        embed.set_footer(text=f"World - Direct Message")
        embed.color = (0x2F3136)
        await ctx.send(embed=embed)
        embed1 = discord.Embed(description=f"You Have Recived A Message", timestamp=ctx.message.created_at)
        embed1.add_field(name="Message:", value=f"`{msg}`\n --------------\n From - {ctx.author.mention}\n Guild = `{ctx.guild}`")
        embed1.set_author(name="World - Direct Message", icon_url=self.bot.user.avatar_url)
        embed1.set_thumbnail(url=world_pfp)
        embed1.set_footer(text=f"World - Direct Message")
        embed1.color = (0x2F3136)
        await member.send(embed=embed1)

    @dm.error
    async def dm_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/dm <member> <message>`")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f':regional_indicator_x: Sorry {ctx.author.mention} You Do Not Have Perms To Direct Message Members!')
        elif isinstance(error, commands.CommandOnCooldown):
            a = error.retry_after
            a = round(a)
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {a} seconds.")

    @commands.command(help="Snipe a deleted message.")
    async def snipe(self, ctx):
    	try:
    		embed = discord.Embed(title="Snipe", color=0x2F3136, timestamp=datetime.datetime.utcnow())
    		embed.add_field(name="User", value=self.snipeCache[ctx.channel.id]["user"])
    		embed.add_field(name="Content", value=self.snipeCache[ctx.channel.id]["content"])
    		embed.add_field(name="Channel", value=f"<#{self.snipeCache[ctx.channel.id]['channel']}>")
    		await ctx.send(embed=embed)
    		del self.snipeCache[ctx.channel.id]
    	except Exception as e:
    		return await ctx.send(f"Sorry {ctx.author.mention} there is nothing to snipe!")


    @commands.command(help="Snipe a edited message.")
    async def editsnipe(self, ctx):
    	try:
    		embed = discord.Embed(title="Edit Snipe", colour=0x2F3136, timestamp=datetime.datetime.utcnow())
    		embed.add_field(name="User", value=self.editSnipeCache[ctx.channel.id]["user"])
    		embed.add_field(name="Content", value=self.editSnipeCache[ctx.channel.id]["bcontent"])
    		embed.add_field(name="Channel", value=f"<#{self.editSnipeCache[ctx.channel.id]['channel']}>")
    		await ctx.send(embed=embed)
    		del self.editSnipeCache[ctx.channel.id]
    	except Exception as e:
    		return await ctx.send(f"Sorry {ctx.author.mention} there is nothing to editsnipe!")


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.snipeCache.update(
            {message.channel.id: {
            "user": message.author,
            "content": message.content,
            "channel": message.channel.id
            }})


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        self.editSnipeCache.update(
            {before.channel.id: {
                "user": before.author,
                "bcontent": before.content,
                "channel": before.channel.id
            }})


def setup(bot):
    bot.add_cog(ModCog(bot))
