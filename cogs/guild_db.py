import discord
from datetime import datetime
from discord.ext import commands
import sqlalchemy as db
from sqlalchemy import (create_engine, MetaData, Table, Column, Integer, String, DateTime, Boolean, select, text, delete, update)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import selectinload
from itertools import islice
import re
import greenlet


Base = declarative_base()


class Player(Base):
    __tablename__ = "Players"
    char_id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(12), nullable = False, unique = True, server_default = "NAME_FOR_CH!")
    points = db.Column(db.Integer(), nullable = False, unique = False, server_default = "0")
    rank = db.Column(db.String(5), nullable = False, unique = False, server_default = "LR0")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"({self.char_id}) {self.name}, {self.points}, {self.rank}"


async def setup(bot):
    await bot.add_cog(gdb(bot))


class gdb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.engine = create_async_engine(f"sqlite+aiosqlite:///WipeMeBabyOneMoreTime.db", echo = True)
        self.embed_list_message = None
        self.start_of_list = 0
        self.end_of_list = 0
        self.ranks = {
            "LR0": 5,
            "LR1": 10,
            "LR2": 25,
            "LR3": 50,
            "LR4": 100,
            "LR5": 250,
            "LR6": 500,
            "LR7": 1000,
            "LR8": 1500,
            "LR9": 2000,
            "LR10": 2500,
            "LR11": 3000,
            "LR12": 3500,
        }


    @commands.Cog.listener()
    async def on_ready(self):
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        except Exception as e:
            print(e)

        print("gdb module is loaded.")


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        try:
            if self.embed_list_message.id == payload.message_id and\
                payload.user_id != 842664616676687912 and\
                (payload.emoji.name == '⬅️' or payload.emoji.name == '➡️'):

                async_session = sessionmaker(self.engine, expire_on_commit = False, class_ = AsyncSession)
                async with async_session() as session:
                    async with session.begin():
                        # Get the the players
                        players = await session.execute(select(Player).order_by(Player.name))

                players_list = []
                for player in players:
                    players_list.append(player[0])

                if payload.emoji.name == '⬅️':
                    if self.start_of_list - 10 >= 0:
                        self.start_of_list -= 10
                        self.end_of_list -= 10
                        await self.new_list_page(players_list)
                        await self.embed_list_message.remove_reaction('⬅️', payload.member)

                if payload.emoji.name == '➡️':
                    if self.start_of_list + 10 < len(players_list):
                        self.start_of_list += 10
                        self.end_of_list += 10
                        await self.new_list_page(players_list)
                        await self.embed_list_message.remove_reaction('➡️', payload.member)
        except Exception as e:
            print(f"[ON_RAW_REACTION_ADD] {e}")


    async def new_list_page(self, players):
        try:
            embed = discord.Embed(title = f"<WipeMeBabyOneMoreTime> Rank List Page {int(self.end_of_list / 10)}",
                                color = discord.Colour(0xe67e22))
            embed.set_thumbnail(url = "https://cdn.wowclassicdb.com/npcs/6491.png")
            
            players = players[self.start_of_list:(self.end_of_list + 1):1]

            i = self.start_of_list
            for player in players:
                if i >= self.end_of_list:
                    break
                i += 1

                rank = int(re.search(r'\d+', player.rank).group())
                embed.add_field(name = f"{i}. {player.name}",
                                value = f"Rank: {rank} (Points: {player.points})",
                                inline = False)

            await self.embed_list_message.edit(embed = embed)
        except Exception as e:
            print(f"[NEW_LIST_PAGE] {e}")


    async def raiders_list(self, ctx):
        try:
            embed = discord.Embed(title = f"<WipeMeBabyOneMoreTime> Rank List Page 1",
                                color = discord.Colour(0xe67e22))
            embed.set_thumbnail(url = "https://cdn.wowclassicdb.com/npcs/6491.png")

            async_session = sessionmaker(self.engine, expire_on_commit = False, class_ = AsyncSession)
            async with async_session() as session:
                async with session.begin():
                    # Get the the players
                    players = await session.execute(select(Player).order_by(Player.name))

            i = 0
            for player in players:
                if i >= 10:
                    break

                rank = int(re.search(r'\d+', player[0].rank).group())
                embed.add_field(name = f"{i + 1}. {player[0].name}",
                                value = f"Rank: {rank} (Points: {player[0].points})",
                                inline = False)
                i += 1

            self.embed_list_message = await ctx.send(embed = embed)
            self.start_of_list = 0
            self.end_of_list = 10

            emojis = ['⬅️', '➡️'];
            for my_emoji in emojis:
                await self.embed_list_message.add_reaction(my_emoji)

        except Exception as e:
            await ctx.send(f"[RAIDERS_LIST] {e}")


    @commands.command(  name = 'gdb_list',
                        help = 'The bot will print the entire list of guild members, their points and ranks.',
                        brief = '- Prints the entire list of guild members, their points and ranks.')
    async def list(self, ctx):
        try:
            # await ctx.message.delete()

            channel = ctx.channel
            channel_id = ctx.channel.id

            if channel_id != 1217479171811315712 and channel_id != 1197166207200153641:
                proper_channel = self.bot.get_channel(1217479171811315712)
                await channel.send(f"This command can only be executed in {proper_channel.mention}")
                return

            await self.raiders_list(ctx)
        except Exception as e:
            await ctx.send(f"[LIST] {e}")


        # try:
        #     async_session = sessionmaker(self.engine, expire_on_commit = False, class_ = AsyncSession)
            
        #     async with async_session() as session:
        #         async with session.begin():
        #             # Query all players
        #             players = await session.execute(select(Player).order_by(Player.name))

        #             for player in players:
        #                 await ctx.send(f"{player[0].name:<12} | {player[0].points:<5} | {player[0].rank:<5}")
        # except Exception as e:
        #     await ctx.send(f"[LIST] {e}")


    @commands.command(  name = 'gdb_add_new_player',
                        alias = 'gdb_add_player',
                        help = 'The bot will create a new entry in the database for the player.',
                        brief = '- Creates a new entry in the database for the player.')
    @commands.has_any_role("Guild Master", "Officer")
    async def add_player(self, ctx, player_name = None):
        try:
            if player_name == None:
                await ctx.send("Please enter a name. Example:\n >gdb_add_new_player undeadkoBot")
                return

            async_session = sessionmaker(self.engine, expire_on_commit = False, class_ = AsyncSession)
            async with async_session() as session:
                async with session.begin():
                    session.add(Player(name = player_name))

            await ctx.send(f"{player_name} was added to the database.")
        except Exception as e:
            await ctx.send(f"[ADD_PLAYER] {e}")


    @commands.command(  name = 'gdb_award_points',
                        help = 'The bot will print the entire list of guild members and their ranks and points.',
                        brief = '- Prints the entire list of guild members and their ranks and points.')
    @commands.has_any_role("Guild Master", "Officer")
    async def add_points(self, ctx, *args):
        try:
            if len(args) != 2 or any(chr.isdigit() for chr in args[1]) == False:
                await ctx.send(f"Please enter a full command with <name> <points>. Example:\n >gdb_award_points undeadkoBot 1")
                return

            if any(chr.isdigit() for chr in args[0]) == True:
                await ctx.send(f"Invalid name {args[0]}. Example:\n >gdb_award_points undeadkoBot 1")
                return

            player_name = args[0]
            awarded_points = args[1]

            async_session = sessionmaker(self.engine, expire_on_commit = False, class_ = AsyncSession)
            async with async_session() as session:
                async with session.begin():
                    # Get the points of the player
                    player = await session.execute(select(Player).where(Player.name == player_name))

                    if player.first() == None:
                        await self.add_player(ctx, player_name)

            async with async_session() as session:
                async with session.begin():
                    # Get the points of the player
                    player = await session.execute(select(Player).where(Player.name == player_name))

                    player_points = int(player.first()[0].points) + int(awarded_points)
                    player_rank = self.update_rank(player_points)

                    # Update player
                    player = await session.execute(update(Player)
                                                    .where(Player.name == player_name)
                                                    .values(points = player_points, rank = player_rank)
                                                    .execution_options(synchronize_session = "fetch"))

            await ctx.send(f"Awarded {awarded_points} to {player_name}")
        except Exception as e:
            await ctx.send(f"[ADD_POINTS] {e}")


    def update_rank(self, player_points):
        for key, value in self.ranks.items():
            if player_points < value:
                return key


    @commands.command(  name = 'gdb_award_points_to_players',
                        help = 'The bot will print the entire list of guild members and their ranks and points.',
                        brief = '- Prints the entire list of guild members and their ranks and points.')
    @commands.has_any_role("Guild Master", "Officer")
    async def add_points_to_players(self, ctx, *args):
        try:
            if len(args) < 3 or any(chr.isdigit() for chr in args[-1]) == False:
                await ctx.send(f"Please enter a full command with <name> <name2> ... <points>. Example:\n >gdb_award_points undeadkoBot Undeadko 1")
                return

            for name in args[:-1]: 
                if any(chr.isdigit() for chr in name) == True:
                    await ctx.send(f"Invalid name {name}. Example:\n >gdb_award_points undeadkoBot Undeadko 1")
                    return

            players_names = args[:-1]
            awarded_points = args[-1]

            async_session = sessionmaker(self.engine, expire_on_commit = False, class_ = AsyncSession)

            for player_name in players_names:
                async with async_session() as session:
                    async with session.begin():
                        # Get the points of the player
                        player = await session.execute(select(Player).where(Player.name == player_name))

                        if player.first() == None:
                            await self.add_player(ctx, player_name)

                async with async_session() as session:
                    async with session.begin():
                        # Get the points of the player
                        player = await session.execute(select(Player).where(Player.name == player_name))

                        player_points = int(player.first()[0].points) + int(awarded_points)
                        player_rank = self.update_rank(player_points)

                        # Update player
                        player = await session.execute(update(Player)
                                                        .where(Player.name == player_name)
                                                        .values(points = player_points, rank = player_rank)
                                                        .execution_options(synchronize_session = "fetch"))

            await ctx.send(f"Awarded {awarded_points} to {players_names}")
        except Exception as e:
            await ctx.send(f"[ADD_POINTS_TO_PLAYERS] {e}")


    @commands.command(  name = 'gdb_delete_player',
                        help = 'The bot will print the entire list of guild members and their ranks and points.',
                        brief = '- Prints the entire list of guild members and their ranks and points.')
    @commands.has_any_role("Guild Master", "Officer")
    async def delete_player(self, ctx, player_name = None):
        try:
            if player_name == None:
                await ctx.send("Please enter a name. Example:\n >gdb_delete_player undeadkoBot")
                return

            if any(chr.isdigit() for chr in player_name) == True:
                await ctx.send(f"Invalid name {player_name}. Example:\n >gdb_delete_player undeadkoBot")
                return

            async_session = sessionmaker(self.engine, expire_on_commit = False, class_ = AsyncSession)
            async with async_session() as session:
                async with session.begin():
                    # Delete the player
                    player = await session.execute(delete(Player)
                                                    .where(Player.name == player_name)
                                                    .execution_options(synchronize_session = "fetch"))

                    await ctx.send(f"{player_name} deleted from the data base.")
        except Exception as e:
            await ctx.send(f"[DELETE_PLAYER] {e}")
