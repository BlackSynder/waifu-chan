import os
import logging
import ssl

import asyncpg
import discord
from discord.ext.commands import Bot

ext_list = ["roles"]
extensions = ["cogs." + extension for extension in ext_list]
token = os.environ.get("TOKEN")
logging.basicConfig(level=logging.INFO)


class WaifuChan(Bot):
    def __init__(self):
        game = discord.Game(name="w!help", type=2)
        super().__init__(command_prefix="w!", description="Waifu Bot for the KKK", game=game)

    async def close(self):
        await self.pool.close()
        await super().close()

    async def on_ready(self):
        print("Ready!")
        print(self.user.name)
        print(self.user.id)
        print("~-~-~-~")
        print("Cogs loaded:")
        self.pool = await asyncpg.create_pool(os.environ["DATABASE_URL"], ssl=ssl.SSLContext(), loop=self.loop)
        query = """SELECT * FROM roles"""
        async with self.pool.acquire() as conn:
            values = await conn.fetch(query)
            self.roles = {val["name"]: {"id": val["id"], "source": val["source"]} for val in values}
        for ext in extensions:
            try:
                self.load_extension(str(ext))
                extension = ext.split(".")[1]
                print(f"Loaded {extension}.")
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print(f'Failed to load extension {ext}\n{exc}')
        print("~-~-~-~")

    async def on_message(self, message):
        ctx = await self.get_context(message)
        if ctx.prefix is not None:
            ctx.command = self.all_commands.get(ctx.invoked_with.lower())
            await self.invoke(ctx)


WaifuChan().run(token)
