import logging

import discord
from discord.ext import commands

from cogs.utils.paginator import Pages


class Roles:
    def __init__(self, bot):
        self.bot = bot
        logging.basicConfig(level=logging.INFO)

    async def on_error(self, error, *args, **kwargs):
        print(error)
        print(args)
        print(kwargs)

    @commands.group()
    async def role(self, ctx):
        """Add or create Waifu roles"""
        if ctx.invoked_subcommand is None:
            await ctx.send(f"Gomen onii-san, thats not how you use this command >-<\nC-Can you try `{ctx.prefix}help`?")

    @role.command()
    @commands.has_permissions(manage_roles=True)
    async def new(self, ctx, name, source, color=None):
        """Create a new Waifu role"""
        roles = self.bot.roles
        role = discord.utils.get(ctx.guild.roles, name=name)

        if role is None:
            role = await ctx.guild.create_role(name=name, color=discord.Color(int(color, 16)), mentionable=True)
            await role.edit(reason="Adjust role position to fit other roles", position=20)
        if role.name in roles:
            await ctx.send("Dame dame, onii-chan! This role is already a waifu role!")
            return

        query = """INSERT INTO roles VALUES ($1, $2, $3)"""
        async with self.bot.pool.acquire() as conn:
            await conn.execute(query, name, role.id, source)
        self.bot.roles[role.name] = {"id": role.id, "source": source}
        await ctx.send(f"Yatta! New waifu role `{role.name}` has been added!")

    @role.command()
    async def add(self, ctx, *, name):
        """Add a Waifu role to yourself"""
        role = discord.utils.find(lambda m: m.name.lower() == name.lower(), ctx.guild.roles)
        roles = self.bot.roles

        if role is None:
            await ctx.send("Gomen! This role doesn't exist. Did you write the name wrong, baka?")
        elif role in ctx.author.roles:
            await ctx.send("B-but you have this role already!")
        elif role.name not in roles:
            await ctx.send("Chotto! That isn't a waifu role!")
        else:
            await ctx.author.add_roles(role)
            await ctx.send(f"I did it onii-san! You now have `{role.name}`!")

    @role.command()
    async def remove(self, ctx, *, name):
        """Remove a Waifu role from yourself"""
        role = discord.utils.find(lambda m: m.name.lower() == name.lower(), ctx.guild.roles)
        roles = self.bot.roles

        if role is None:
            await ctx.send("Gomen! This role doesn't exist. Did you write the name wrong, baka?")
        elif role.name not in roles:
            await ctx.send("Chotto! That isn't a waifu role!")
        elif role not in ctx.author.roles:
            await ctx.send("You don't have that role! Baka!")
        else:
            await ctx.author.remove_roles(role)
            await ctx.send(f"I did it onii-san! You no longer have `{role.name}`!")

    @role.command(name="list")
    async def _list(self, ctx):
        """List all Waifu roles"""
        roles = self.bot.roles
        entries = [f"{ctx.guild.get_role(roles[r]['id']).mention}\n    \
                  {roles[r]['source']}" for r in roles]

        try:
            p = Pages(self.bot, message=ctx.message, entries=entries)
            p.embed.set_author(name=ctx.bot.user.display_name, icon_url=ctx.bot.user.avatar_url)
            await p.paginate()
        except Exception as e:
            await ctx.send(e)


def setup(bot):
    bot.add_cog(Roles(bot))
