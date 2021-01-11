from datetime import datetime
from discord.ext import commands
from discord import Embed, Member
from discord.utils import find, get

class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.snipeCache = {}
        self.editSnipeCache = {}
        self.color = 0x2F3136

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: Member, *, reason=None):
        """Ban a specified Discord Member."""
        try:
            await member.ban(reason=reason)
            embed = Embed(title="Ban", description=f"Hey {ctx.author.mention} you have succsesfully banned {member}", color=self.color)
            await ctx.send(embed=embed)
        except:
            return await ctx.send(f"Sorry {ctx.author.mention} That person has higher or the same permissions as me!")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/ban <member> <reason>`")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f'Sorry {ctx.author.mention} you don\'t have the permissions to do this!')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: Member, *, reason=None):
        """Kick a specified Discord member."""
        try:
            await member.kick(reason=reason)
            embed = Embed(title="Kick", description=f"Hey {ctx.author.mention} you have succsesfully kicked {member}", color=self.color)
            await ctx.send(embed=embed)
        except:
            return await ctx.send(f"Sorry {ctx.author.mention} That person has higher or the same permission as me!")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/kick <member> <reason>`")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f'Sorry {ctx.author.mention} you don\'t have the permissions to do this!') 

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: Member, *, reason=None):
        """Mute a specified discord member"""
        role = get(ctx.guild.roles, name="Muted")
        if not role:
            try:
                createrole = await ctx.guild.create_role(name="Muted", reason="This was created so the bot can mute discord members!")
                for channel in ctx.guild.channels:
                    await channel.set_permissions(createrole, send_messages=False)
            except:
                return await ctx.send(f"Sorry {ctx.author.mention} i don't have permissions to create a roll called `Muted`.")
        else:
            await user.add_roles(role)
            embed = Embed(title="Muted", description=f"Hey {ctx.author.mention} you have succsesfully muted {user}", color=self.color)
            return await ctx.send(embed=embed)
        await user.add_roles(createrole)
        embed = Embed(title="Muted", description=f"Hey {ctx.author.mention} you have succsesfully muted {user}", color=self.color)
        return await ctx.send(embed=embed)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f'Sorry {ctx.author.mention} you don\'t have the permissions to do this!')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/mute <member> <reason>`")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        """Delete messages in BULK."""
        if amount >= 100:
            return await ctx.send(f"Sorry {ctx.author.mention} `100` is max limit.")
        if amount <= 1:
            return await ctx.send(f"Sorry {ctx.author.mention} Please purge more than `1` message")
        else:
            await ctx.channel.purge(limit=amount)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'Sorry {ctx.author.mention} Please Type `w/purge <amount>')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f'Sorry {ctx.author.mention} you don\'t have the permissions to do this!')
        

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: str):
        """Unban a banned Member"""
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = Embed(title="Unban", description=f"Hey {ctx.author.mention} you have succsesfully unbanned {member}", color=self.color)
                return await ctx.send(embed=embed)

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f'Sorry {ctx.author.mention} you don\'t have the permissions to do this!, Or that user is not banned!')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/unban <member>`")

    @commands.command()
    async def poll(self, ctx, *, desc):
        """Start a poll and let users react!"""
        embed = Embed(title="Poll", description=f"{ctx.author.mention} Started a poll!", color=self.color)
        embed.add_field(name="Please React", value=f"**{desc}**", inline=False)
        embed.set_footer(text="👍 for Yes, 👎 for No.")
        message = await ctx.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")

    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/poll <text>`")


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        """Changes Permissions for Guild's Default role. send_messages=False"""
        await ctx.message.channel.set_permissions(ctx.guild.default_role, read_messages=True, send_messages=False)
        embed = Embed(title="Lockdown", description=f"{ctx.author.mention} has locked this channel.", color=self.color)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def nuke(self, ctx, channel=None):
        """Deletes the specified channel, Then clones it and makes a new one"""
        channel = channel or ctx.channel
        nuke_ = Embed(
            title="Nuke",
            description=f"Would you like to nuke `{channel}`?\nThis will delete the channel and remake it.",
            color=self.color
            )

        nuke_fail = Embed(
            title="Nuke Failed",
            description=f"You Chose not to nuke `{channel}`",
            color=self.color
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
                    embed = Embed(title="Error:", description=e, color=self.color)
                    return await ctx.send(embed=embed)
            elif emoji=='❎':
                await message.edit(embed=nuke_fail)
                break

            res = await self.bot.wait_for('reaction_add', check=lambda r, u: u.id == ctx.author.id and r.message.id == message.id, timeout=15)
            if res==None:
                break
            if str(res[1])!='World#4520':
                emoji=str(res[0].emoji)

        await message.clear_reactions()
        
    @nuke.error
    async def nuke_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f'Sorry {ctx.author.mention} you don\'t have the permissions to do this!')

 
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        """Changes Permissions for Guild's Default role. send_messages=True"""
        await ctx.message.channel.set_permissions(ctx.guild.default_role, read_messages=True, send_messages=True)
        embed = Embed(title="Lockdown over", description=f"{ctx.author.mention} has unlocked this channel!", color=self.color)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, seconds: int):
        """Set the slowmode of the channel you are using the bot in!"""
        if seconds >= 21600:
            return await ctx.send(f"Sorry {ctx.author.mention} `21600` is max slowmode range.")
        await ctx.message.channel.edit(slowmode_delay=seconds)
        embed = Embed(title="Slowmode", description=f"I have set the slowmode for <#{ctx.message.channel.id}> to `{seconds}`", color=self.color)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: Member, *, reason=None):
        """Unmute a user"""
        if user == ctx.author:
            return await ctx.send(f"Sorry {ctx.author.mention} you can't mute yourself!")
        role = get(ctx.guild.roles, name="Muted")
        if not role:
            return await ctx.send(f"Sorry {ctx.author.mention} there seems to not be a role called `Muted`!")
        if not find(lambda role: role.name == "Muted", user.roles):
            return await ctx.send(f"Sorry {ctx.author.mention} that user is not muted?")
        await user.remove_roles(role)
        embed = Embed(title="Unmute", description=f"Hey {ctx.author.mention} you have succsesfully unmuted {user}!", color=self.color)
        return await ctx.send(embed=embed)

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/unmute <member> <reason>`")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f'Sorry {ctx.author.mention} you don\'t have the permissions to do this!')

    @slowmode.error
    async def slowmode_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f'Sorry {ctx.author.mention} you don\'t have the permissions to do this!') 
   
    @lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f'Sorry {ctx.author.mention} you don\'t have the permissions to do this!') 
        
    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f'Sorry {ctx.author.mention} you don\'t have the permissions to do this!') 

    @commands.command()
    async def snipe(self, ctx):
        """Fetches the last Deleted message in the channel and shows you the content of it."""
        try:
            badwords = ["nigger", "nig", "coon", "nigga", "retard", "rapist", "rape", "niggar", "faggot", "fag", "dyke", "whore"]
            if self.snipeCache[ctx.channel.id]["content"] in badwords:
                return await ctx.send(f"Sorry {ctx.author.mention} there is nothing to snipe!")
            embed = Embed(title="Snipe", color=self.color, timestamp=datetime.utcnow())
            embed.add_field(name="User", value=self.snipeCache[ctx.channel.id]["user"])
            embed.add_field(name="Content", value=self.snipeCache[ctx.channel.id]["content"])
            embed.add_field(name="Channel", value=f"<#{self.snipeCache[ctx.channel.id]['channel']}>")
            await ctx.send(embed=embed)
            del self.snipeCache[ctx.channel.id]
        except:
            return await ctx.send(f"Sorry {ctx.author.mention} there is nothing to snipe!")


    @commands.command()
    async def editsnipe(self, ctx):
        """Fetches the last Edited message in the channel and shows you the content of it."""
        try:
            badwords = ["nigger", "nig", "coon", "nigga", "retard", "rapist", "rape", "niggar", "faggot", "fag", "dyke", "whore"]
            if self.editSnipeCache[ctx.channel.id]["bcontent"] in badwords:
                return await ctx.send(f"Sorry {ctx.author.mention} there is nothing to snipe!")
            embed = Embed(title="Edit Snipe", colour=self.color, timestamp=datetime.utcnow())
            embed.add_field(name="User", value=self.editSnipeCache[ctx.channel.id]["user"])
            embed.add_field(name="Content", value=self.editSnipeCache[ctx.channel.id]["bcontent"])
            embed.add_field(name="Channel", value=f"<#{self.editSnipeCache[ctx.channel.id]['channel']}>")
            await ctx.send(embed=embed)
            del self.editSnipeCache[ctx.channel.id]
        except:
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
