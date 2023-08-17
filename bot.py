import asyncio
import os
import datetime
import json
import requests
import wavelink

import disnake
from disnake.ext import commands
from dotenv import load_dotenv
from disnake.ui import Button
from disnake import FFmpegPCMAudio


load_dotenv()

bot = commands.Bot(command_prefix='!', help_command=None, intents=disnake.Intents.all()) #префикс - обращение к командам бота, help_command - если захотим переписать базовую команду /help, ИНТЕНТЫ?))


@bot.event
async def on_ready():
    print(f'Bot {bot.user} is ready to work!')
    await bot.change_presence(
        activity=disnake.Activity(type=disnake.ActivityType.listening, name='Альбину Сексову'),
        status=disnake.Status.dnd)
    bot.loop.create_task(node_connect())


@bot.event
async def on_wavelink_node_ready(node=wavelink.Node):
    print(f"Node {node.identifier} is ready!")


# async def node_connect():
#     await bot.wait_until_ready()
#     await wavelink.NodePool(bot=bot, host='lavalinkinc.ml', port=443, password= "incognito", https=True)
#
#
# @bot.command()
# async def play (ctx: commands.Context, *, search: wavelink.YouTubeTrack):
#     if not ctx.voice_client:
#         vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
#     elif not ctx.author.voice_client:
#         return await ctx.send('first join')
#     else:
#         vc: wavelink.Player = ctx.voice_client
#
#     vc.play(search)


@bot.slash_command()
async def server(inter):
    """Информация о сервере"""
    await inter.response.send_message(
        f"Название сервера: {inter.guild.name}\nВсего участников: {inter.guild.member_count}"
    )


@bot.slash_command()
async def check_activity(ctx, user: disnake.Member):
    await ctx.send(user.activities)
    print(user.activities)


@bot.slash_command()
async def check_status(ctx, user: disnake.Member):
    await ctx.send(user.status)


# @bot.event
# async def on_presence_update(before, after):
#     print(f'{before.display_name} changed status from {before.status} to {after.status}')
#     if after.status == disnake.Status.online:
#         user = after
#         button = Button(style=disnake.ButtonStyle.secondary, label="click on me", custom_id="some_button")
#         button2 = Button(style=disnake.ButtonStyle.primary, label="dont click on me", custom_id="another_button")
#         components = [button, button2]
#         url = ('https://dog.ceo/api/breeds/image/random')
#         dog_data = requests.get(url).json()
#         dog_url = dog_data['message']
#         embed = disnake.Embed(color=disnake.Color.random())
#         embed.set_image(url=dog_url)
#         await user.send(embed=embed, components=components)


# @bot.command()
# async def send_dm(inter, user: disnake.User):
#     # Проверяем, что команду использовал администратор (можете изменить на свой условия)
#     # button = Button(style=disnake.ButtonStyle.secondary, label="click on me", custom_id="some_button")
#     await user.send("Here's a button for you!", components=button)
#     # await inter.send(f'Sent a DM to {user.name}')


@bot.listen("on_button_click")
async def help_listener(inter: disnake.MessageInteraction):
    if inter.component.custom_id == "some_button":
        await inter.send(f"Привет, {inter.author.mention}! Я бот, рад тебя видеть!")


@bot.listen()
async def on_guild_channel_create(channel: disnake.Guild.text_channels):
    channel_id = 1134403792142598167  # Замените на ID вашего целевого канала
    channel = bot.get_channel(channel_id)
    await channel.send('new channel created')


@bot.slash_command()
async def del_some_channels(ctx, channel: disnake.abc.GuildChannel):
    if not isinstance(channel, (disnake.TextChannel, disnake.VoiceChannel)):
        await ctx.send("Invalid channel type. Please specify a text or voice channel")
        return
    deleted_by = ctx.author.mention
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    await channel.delete()
    embed = disnake.Embed(title="Delete channel",
                          description=f"### The channel {channel.name} was deleted by ||{deleted_by}|| in {now_time}")
    embed.set_thumbnail(url=ctx.author.avatar.url)
    await ctx.send(embed=embed)


@bot.slash_command()
async def join_to_voice_channel(ctx):
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        await voice_channel.connect()
        await ctx.send(f"Подключен к {voice_channel.name}")
    else:
        await ctx.send("Ошибка")


@bot.slash_command()
async def weather(ctx, city):
    url = ('https://api.openweathermap.org/data/2.5/weather?q='+str(city)+'&units=metric&lang=ru&appid='
                                                                          '79d1ca96933b0328e1c7e3e7a26cb347')
    weather_data = requests.get(url).json()
    temperature = round(weather_data['main']['temp'], 1)
    temperature_feels = round(weather_data['main']['feels_like'], 1)
    wind_speed = round(weather_data['wind']['speed'], 1)
    type_of_weather = weather_data['weather'][0]['description']
    embed = disnake.Embed(title="Погода в доме",
                          description=f'В городе *{city}* сейчас {temperature} градусов, {type_of_weather}. '
                                      f'Ощущается, как {temperature_feels}. Скорость ветра {wind_speed} м/с',
                          color=disnake.Color.random())
    embed.set_thumbnail(url="https://images.ctfassets.net/hrltx12pl8hq/6TIZLa1AKeBel0yVO7ReIn/"
                            "1fc0e2fd9fcc6d66b3cc733aa2547e11/weather-images.jpg?fit=fill&w=600&h=400")
    await ctx.send(embed=embed)




#bot.load_extensions('cogs') #расширение .py указывать не нужно
#Для загрузки всех когов из папки cogs можно использовать bot.load_extensions('cogs')

TOKEN = os.environ['BOT_TOKEN']
bot.run(TOKEN)