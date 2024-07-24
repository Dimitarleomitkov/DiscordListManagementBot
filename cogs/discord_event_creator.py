import discord
from discord.ext import tasks, commands
from datetime import datetime
import aiohttp
import json
import re
import asyncio

async def setup(bot):
    await bot.add_cog(event_create(bot))


class event_create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.title = ""


    @commands.Cog.listener()
    async def on_ready(self):
        print("event_creator module is loaded.")


    async def create_and_update_event(self, message):
        try:
            if message.embeds[0].fields[0].name != 'Loading...':
                # Construct the message URL
                message_url = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"

                embed = message.embeds[0].to_dict()

                # Extract leader
                leader_emoji = "🏳️"
                leader = re.search(r"<:LeaderX:\d+> (\w+)", embed["fields"][0]["value"]).group(1)

                # Extract description
                description = re.search(r"\*\*\n\n(.*)", embed.get("description", "No description provided"), re.DOTALL).group(1)

                # Extract timestamps using regex
                start_time_match = re.search(r'__<t:(\d+):t>', embed["fields"][1]["value"])
                end_time_match = re.search(r'- <t:(\d+):t>', embed["fields"][1]["value"])

                if start_time_match and end_time_match:
                    start_time_unix = int(start_time_match.group(1))
                    end_time_unix = int(end_time_match.group(1))

                    # Convert Unix timestamps to datetime objects
                    start_time = datetime.utcfromtimestamp(start_time_unix).strftime('%Y-%m-%dT%H:%M:%S')
                    end_time = datetime.utcfromtimestamp(end_time_unix).strftime('%Y-%m-%dT%H:%M:%S')

                    await self.create_guild_event(guild_id = message.guild.id,
                                                        name = self.title,
                                                        description = f"{leader_emoji} {leader}\n\n**Description:**\n{description}",
                                                        start_time = start_time,
                                                        end_time = end_time,
                                                        location = message_url,
                                                        )
            else:
                self.title = message.embeds[0].title

                await asyncio.sleep(3)
                await self.create_and_update_event(message)
        except Exception as e:
            print(e)


    @commands.Cog.listener()
    async def on_message(self, message):
        # print(message.author.id)
        # print(message.content)
        
        # if message.author.id == 579155972115660803 and message.content.startswith("<@&1221852616812793968>"):
        if message.author.id == 579155972115660803:
            await self.create_and_update_event(message)


    @commands.command(  name = 'create_event',
                        help = 'The bot will create an event for Discord',
                        brief = '- Helping function for event creation.')
    async def event_create(self, ctx, *args):
        leader_emoji = "🏳️"
        leader = "undeadko"
        n_participants_emoji = "👥"
        n_participants = 25
        time_to_event_emoji = "⏳"
        time_to_event = "in 20 hours"

        try:
            await self.create_guild_event(guild_id = ctx.guild.id,
                                            name = "Test",
                                            description = f"{leader_emoji} {leader}\t{n_participants_emoji} **{n_participants}**\t{time_to_event_emoji} {time_to_event}\n\n**Description:**\nTrying to automate a bit...",
                                            start_time = "2024-07-30T17:00:00",
                                            end_time = "2024-07-30T20:00:00",
                                            location = 'https://discord.com/channels/1196048347174293544/1217741818406637638/1264149845711523862',
                                            )
        except Exception as e:
            print(e)


    async def create_guild_event(self, guild_id, name, description, start_time, end_time, location):
        url = f"https://discord.com/api/v10/guilds/{guild_id}/scheduled-events"
        headers = {
            "Authorization": f"Bot {self.bot.http.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "name": name,
            "description": description,
            "scheduled_start_time": start_time,
            "scheduled_end_time": end_time,
            "privacy_level": 2,  # GUILD_ONLY
            "entity_type": 3,  # EXTERNAL
            "entity_metadata": {
                "location": location
            }
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=json.dumps(payload)) as response:
                if response.status == 201 or response.status == 200:
                    # print("Event created successfully")
                    pass
                else:
                    print(f"Failed to create event: {response.status}")
                    print(await response.text())
