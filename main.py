import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from gtm import get_class


load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'вас приветствует {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'привет, это бот {bot.user}, *внимвние мы не несем ответсвенность за последствия, не надейтесь на этого бота')

@bot.command()
async def photo(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            if attachment.filename.endswith('.jpg')or \
            attachment.filename.endswith('jpeg')or \
            attachment.filename.endswith('.png'):
                image_path = f'./images/{attachment.filename}'
                await attachment.save(image_path)
                msg = await ctx.send('обработка фото...')
                class_name, confidence_score = get_class(image_path,
                                                         './gtm_model/keras_model.h5',
                                                         './gtm_model/labels.txt')
                await msg.delete()
                await ctx.send(f'С вероятностью{confidence_score}% на фото{class_name}')
            else:
                await ctx.send('допустимый формат изображения - jpg jpeg png')
                return
    else:
        await ctx.send('прикрепи фото')


bot.run(DISCORD_TOKEN)