from discord.ext.commands import Bot
import os
import json
import aiohttp
import asyncio
import logging

ext_list = ["roles"]
extensions = ["Cogs." + extension for extension in ext_list]
token = os.environ.get("TOKEN")
logging.basicConfig(level=logging.INFO)

class WaifuChan(Bot):
    def __init__(self):
        super().__init__(command_prefix="w!", description="Waifu Bot for the KKK")

    async def get_json(self, json_id, file_name):
        async with aiohttp.ClientSession() as cs:
               async with cs.get(f'https://jsonblob.com/api/jsonBlob/{json_id}') as resp:
                   if resp.status != 200:
                       raise RuntimeError('For some reason, it failed.')
                   response = await resp.json()
                   with open(file_name+".json", "w") as json_file:
                       json.dump(response, json_file, indent=4)
                       return response

    async def update_json(self, json_id, json_file):
        async with aiohttp.ClientSession() as cs:
               async with cs.put(f'https://jsonblob.com/api/jsonBlob/{json_id}', data=json.dumps(json_file), headers = {'content-type': 'application/json'}) as resp:
                   if resp.status != 200:
                       raise RuntimeError('For some reason, it failed.')
                   return await resp.json()

    def config(self, target):
        with open("config.json") as config_file:
            configs = json.load(config_file)
            return configs[target]

    def reconfig(self, target, value):
        with open("config.json") as config_file:
            configs = json.load(config_file)
            configs[target] = value
            json.dump(configs, open("config.json", "r+"), indent=4)

    async def on_ready(self):
        print("Ready!")
        print(self.user.name)
        print(self.user.id)
        print("~-~-~-~")
        print("Cogs loaded:")
        await self.get_json(os.environ.get("ROLES_JSON"), "roles")
        for ext in extensions:
            try:
                self.load_extension(str(ext))
                extension = ext.split(".")[1]
                print(f"Loaded {extension}.")
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(ext, exc))
        print("~-~-~-~")

WaifuChan().run(token)
