import os
import discord
import requests
import keep_alive
from discord import Intents
from discord.ext import commands
from AnilistPython import Anilist

TOKEN = os.environ['TOKEN']

PREFIX = 'a!'
GUILD_ID = '1167784466018730034'
CHANNEL_ID = '1169680345457754202'

intents = Intents.all()
client = commands.Bot(command_prefix=PREFIX, intents=intents)

anilist = Anilist()


@client.event
async def on_ready():
  print("===========================================")
  print(f'Logged In As : {client.user}')
  print("===========================================")


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
    cover_image = anime_dict["cover_image"]

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
    anime_embed.add_field(name="Anime ID", value=anime_id, inline=False)
    anime_embed.add_field(name="\u200b", value="\u200b", inline=False)
    anime_embed.add_field(name="Airing Date", value=starting_time, inline=True)
    anime_embed.add_field(name="Ending Date", value=ending_time, inline=True)
    anime_embed.add_field(name="\u200b", value="\u200b", inline=True)

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
      anime_embed.add_field(name="\u200b", value="\u200b", inline=True)
      anime_embed.add_field(name="\u200b", value="\u200b", inline=False)
      anime_embed.add_field(name="Season", value=season, inline=True)
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
    await ctx.send(f'An Error Occured Searching For Anime \n\n Error :  {e}')

keep_alive.keep_alive()
client.run(TOKEN)
