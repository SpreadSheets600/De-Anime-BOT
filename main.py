import os
import discord
import requests
import datetime
import keep_alive

from ping3 import ping
from discord import Intents
from discord.ext import commands
from AnilistPython import Anilist

TOKEN = os.environ['TOKEN']

PREFIX = '>'
GUILD_ID = '1167784466018730034'
CHANNEL_ID = '1169680345457754202'

intents = Intents.all()
client = commands.Bot(command_prefix=PREFIX, intents=intents)
client.remove_command('help')

anilist = Anilist()


@client.event
async def on_ready():

  client.start_time = datetime.datetime.now()

  print("===========================================")
  print(f'Logged In As : {client.user}')
  print("===========================================")
  await client.change_presence(activity=discord.Activity(
      type=discord.ActivityType.watching, name='Anime'))


@client.command()
async def anisearch(ctx, *, anime_name):
  try:
    anime_dict = anilist.get_anime(anime_name=anime_name)

    anime_id = anilist.get_anime_id(anime_name)
    anime_desc = anime_dict['desc']
    anime_title = anime_dict["name_english"]
    starting_time = anime_dict["starting_time"]
    ending_time = anime_dict["ending_time"]
    next_airing_ep = anime_dict["next_airing_ep"]
    airing_format = anime_dict["airing_format"]
    airing_status = anime_dict["airing_status"]
    airing_ep = anime_dict["airing_episodes"]
    season = anime_dict["season"]
    genres = anime_dict["genres"]
    anime_url = f'https://anilist.co/anime/{anime_id}/'
    cover_image = anime_dict["banner_image"]

    next_ep_string = ''
    try:
      initial_time = next_airing_ep['timeUntilAiring']
      mins, secs = divmod(initial_time, 60)
      hours, mins = divmod(mins, 60)
      days, hours = divmod(hours, 24)
      timer = f'{days} days {hours} hours {mins} mins {secs} secs'
      next_ep_num = next_airing_ep['episode']
      next_ep_string = f'Episode {next_ep_num} is releasing in {timer}!\
                            \n\n[{anime_title} AniList Page]({anime_url}))'

    except:
      next_ep_string = f"This Anime's Release Date Has Not Been Confirmed Yet.\
                            \n\n[{anime_title} AniList Page]({anime_url}))"

    if anime_desc != None and len(anime_desc) != 0:
      anime_desc = anime_desc.split("<br>")

    anime_embed = discord.Embed(title=anime_title, color=0xA0DB8E)
    anime_embed.set_image(url=cover_image)
    anime_embed.add_field(name="Synopsis", value=anime_desc[0], inline=False)
    anime_embed.add_field(name="\u200b", value="\u200b", inline=False)
    anime_embed.add_field(name="Anime ID", value=anime_id, inline=True)
    anime_embed.add_field(name="Airing Date", value=starting_time, inline=True)
    anime_embed.add_field(name="Ending Date", value=ending_time, inline=True)
    anime_embed.add_field(name="Season", value=season, inline=True)

    try:
      episodes = int(airing_ep)

      if episodes > 1:
        anime_embed.add_field(name="Airing Format",
                              value=f"{airing_format} ({airing_ep} Episodes)",
                              inline=True)
      else:
        anime_embed.add_field(name="Airing Format",
                              value=f"{airing_format} ({airing_ep} Episode)",
                              inline=True)

    except:
      anime_embed.add_field(name="Airing Format",
                            value=airing_format,
                            inline=True)

    if airing_status.upper() == 'FINISHED':
      anime_embed.add_field(name="Airing Status",
                            value=airing_status,
                            inline=True)
      anime_embed.add_field(name="\u200b", value="\u200b", inline=False)
      anime_embed.add_field(name="Genres",
                            value=", ".join(genres),
                            inline=False)
      anime_embed.add_field(
          name="Next Episode ~",
          value=
          f"The Anime Has Finished Airing !\n\n[{anime_title} AniList Page]({anime_url})\n",
          inline=False)

    else:
      anime_embed.add_field(name="Airing Status",
                            value=airing_status,
                            inline=True)
      anime_embed.add_field(name="Genres", value=genres, inline=True)
      anime_embed.add_field(name="Next Episode ~",
                            value=next_airing_ep,
                            inline=False)

    await ctx.send(embed=anime_embed)

  except Exception as e:
    print(e)
    await ctx.send(f'An Error Occured Searching For Anime \n```Error :  {e}```'
                   )


@client.command()
async def mangasearch(ctx, *, anime_name):
  try:
    manga_dict = anilist.get_manga(anime_name)

    manga_id = anilist.get_manga_id(anime_name)
    manga_desc = manga_dict['desc']
    manga_title = manga_dict["name_english"]
    starting_time = manga_dict["starting_time"]
    ending_time = manga_dict["ending_time"]
    airing_format = manga_dict["release_format"]
    chapters = manga_dict["chapters"]
    airing_status = manga_dict["release_status"]
    season = manga_dict["volumes"]
    genres = manga_dict["genres"]
    anime_url = f'https://anilist.co/manga/{manga_id}/'
    cover_image = manga_dict["banner_image"]

    if manga_desc != None and len(manga_desc) != 0:
      manga_desc = manga_desc.split("<br>")

    anime_embed = discord.Embed(title=manga_title, color=0xA0DB8E)
    anime_embed.set_image(url=cover_image)
    anime_embed.add_field(name="Synopsis", value=manga_desc[0], inline=False)
    anime_embed.add_field(name="\u200b", value="\u200b", inline=False)
    anime_embed.add_field(name="Manga ID", value=manga_id, inline=True)
    anime_embed.add_field(name="Release Date",
                          value=starting_time,
                          inline=True)
    anime_embed.add_field(name="Ending Date", value=ending_time, inline=True)
    anime_embed.add_field(name="Volume", value=season, inline=True)

    try:
      episodes = int(chapters)

      if episodes > 1:
        anime_embed.add_field(name="Airing Format",
                              value=f"{airing_format} ({chapters} Chapters)",
                              inline=True)
      else:
        anime_embed.add_field(name="Airing Format",
                              value=f"{airing_format} ({chapters} Chapter)",
                              inline=True)

    except:
      anime_embed.add_field(name="Airing Format",
                            value=airing_format,
                            inline=True)

    if airing_status.upper() == 'FINISHED':
      anime_embed.add_field(name="Airing Status",
                            value=airing_status,
                            inline=True)
      anime_embed.add_field(name="\u200b", value="\u200b", inline=False)
      anime_embed.add_field(name="Genres",
                            value=", ".join(genres),
                            inline=False)
      anime_embed.add_field(
          name="Next Episode ~",
          value=
          f"The Manga Has Finished It's Release !\n\n[{manga_title} AniList Page]({anime_url})\n",
          inline=False)

    else:
      anime_embed.add_field(name="Airing Status",
                            value=airing_status,
                            inline=True)
      anime_embed.add_field(name="Genres", value=genres, inline=True)

    await ctx.send(embed=anime_embed)

  except Exception as e:
    print(e)
    await ctx.send(f'An Error Occured Searching For Anime \n```Error :  {e}```'
                   )


@client.command()
async def charactersearch(ctx, *, character_name):

  character_dict = anilist.get_character(character_name)
  character_id = anilist.get_character_id(character_name)

  character_desc = character_dict['desc']
  first_name = character_dict["first_name"]
  last_name = character_dict["last_name"]
  image = character_dict["image"]

  if last_name != None:
    character_name = str(first_name) + str(last_name)
  else:
    character_name = str(first_name)

  if character_desc and len(character_desc) > 1024:
    character_desc = character_desc[:970] + f"[ ... Read More. ](https://anilist.co/character/{character_id})"

  try:
    character_embed = discord.Embed(title=character_name, color=0xA0DB8E)
    character_embed.set_image(url=image)
    character_embed.add_field(name="Description",
                              value=character_desc,
                              inline=False)
    character_embed.add_field(name="\u200b", value="\u200b", inline=False)
    character_embed.add_field(name="Character Name",
                              value=character_name,
                              inline=True)
    character_embed.add_field(name="Character ID",
                              value=character_id,
                              inline=True)

    await ctx.send(embed=character_embed)

  except Exception as e:
    print(e)
    await ctx.send(
        f'An Error Occured Searching For Character \n```{e}```')


@client.command()
async def help(ctx):
  help_embed = None
  help_embed = discord.Embed(title="Help",
                             description="List Of Available Commands",
                             color=0xA0DB8E)

  help_embed.set_image(url="https://shorturl.at/bju12")
  help_embed.add_field(name="`>help`",
                       value="Display This Help Message",
                       inline=False)
  help_embed.add_field(name="`>anisearch`",
                       value="Search For An Anime",
                       inline=False)
  help_embed.add_field(name="`>mangasearch`",
                       value="Search For A Manga",
                       inline=False)
  help_embed.add_field(name="`>characterseach`",
                       value="Search For A Character",
                       inline=False)
  await ctx.send(embed=help_embed)


@client.command()
async def ping(ctx):

  latency = client.latency * 1000
  server_name = ctx.guild.name if ctx.guild else "Direct Message"
  uptime = datetime.datetime.now() - client.start_time
  uptime_seconds = uptime.total_seconds()
  uptime_str = str(datetime.timedelta(seconds=uptime_seconds)).split(".")[0]
  num_servers = len(client.guilds)

  embed = discord.Embed(title="_*Pong !*_", color=0xA0DB8E)
  embed.add_field(name="---------------------", value="     ", inline=False)
  embed.add_field(name="Servers", value=num_servers, inline=False)
  embed.add_field(name="Latency", value=f"{latency:.2f}ms", inline=False)
  embed.add_field(name="Server Name", value=server_name, inline=False)
  embed.add_field(name="Uptime", value=uptime_str, inline=False)

  await ctx.send(embed=embed)


keep_alive.keep_alive()
client.run(TOKEN)
