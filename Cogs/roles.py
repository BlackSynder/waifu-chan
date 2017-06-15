import discord
import logging
from discord.ext import commands
import json
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from bot import WaifuChan

class Roles:
    def __init__(self, bot):
        self.bot = bot
        logging.basicConfig(level=logging.INFO)

    async def on_error(error, *args, **kwargs):
        print(error)
        print(args)
        print(kwargs)

    @commands.group()
    async def role(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"Gomen onii-san, thats not how you use that command >-<\nC-Can you try `{ctx.prefix}help`?")

    @role.command()
    @commands.has_permissions(manage_roles=True)
    async def new(self, ctx, name, source, color=None):
        roles = json.load(open("roles.json"))
        role = discord.utils.get(ctx.guild.roles, name=name)
        if role is None:
            role = await ctx.guild.create_role(name=name, color=discord.Color(int(color, 16)), mentionable=True)
            await role.edit(reason="Adjust role position to fit other roles", position=20)
        if role.name in roles:
            await ctx.send("Dame dame, onii-chan! This role is already a waifu role!")
            return
        roles[role.name] = [str(role.id), source]
        json.dump(roles, open("roles.json", "r+"), indent=4)
        with open("roles.json") as f:
            await ctx.bot.update_json(os.environ["ROLES_JSON"], json.load(f))
        await ctx.send(f"Yatta! New waifu role `{role.name}` has been added!")

    @role.command()
    async def add(self, ctx, *, name):
        role = discord.utils.find(lambda m: m.name.lower() == name.lower(), ctx.guild.roles)
        roles = json.load(open("roles.json"))
        if role is None:
            await ctx.send("Gomen! This role doesn't exist. Did you write the name wrong, baka?")
            return
        if role in ctx.author.roles:
            await ctx.send("B-but you have this role already!")
        elif str(role.id) not in roles.values():
            await ctx.send("Chotto! That isn't a waifu role!")
        else:
            await ctx.author.add_roles(role)
            await ctx.send(f"I did it onii-san! You now have `{role.name}`!")



    @role.command(name="list")
    async def _list(self, ctx):
        roles = json.load(open("roles.json"))
        role_list = discord.Embed(description=f"You can assign these roles by typing `{ctx.prefix}role add <role_name>`")
        role_list.set_author(name="Waifu-chan")
        role_list.add_field(name="Roles", value="\n".join([f"{discord.utils.get(ctx.guild.roles, id=int(roles[r][0])).mention}\n    {roles[r][1]}" for r in roles]))
        await ctx.send(embed=role_list)

def setup(bot):
    bot.add_cog(Roles(bot))
