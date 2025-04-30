import os
from random import randint
from dotenv import load_dotenv

import discord
import requests # 
from faker import Faker
from discord.ext import commands
from googletrans import Translator

import webserver



translator = Translator()
fake = Faker()
load_dotenv()
# TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)


# print('MY_ENV_VAR' in os.environ) # True of False
# print(os.environ['MY_ENV_VAR']) # Print contents of variable
# print(os.environ.get('MY_ENV_VAR')) # Its better when variable not existed


@bot.command()
async def poke(ctx, arg):
    try:
        pokemon = arg.split(' ',1)[0].lower()
        result = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon}')
        if result.text == 'Not Found':
            await ctx.send('Pokemon not found!')
        else:
            image_url = result.json()['sprites']['front_default']
            print(image_url)
            await ctx.send(image_url)
    except Exception as e:
        print('Error: ',e)
        

@poke.error
async def error_type(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('You need to specify me a pokemon name')


@bot.command()
async def clean(ctx):
    await ctx.channel.purge()
    await ctx.send(f'Messages removed', delete_after=3)


@bot.command()
async def translate(ctx, lang_destino, *, texto):
    traduccion = await translator.translate(texto, dest=lang_destino)
    await ctx.send(f"Translation ({lang_destino}): {traduccion.text}")


@bot.command()
async def gimme(ctx, what, *args):
    try:
        if what == 'name':
            res = fake.name()
            await ctx.send(f"(name): {res}")
        elif what == 'address':
            res = fake.address()
            await ctx.send(f"(address): {res}")
        else:
            raise commands.errors.BadArgument('No')
    except Exception as e:
        print('Error: ',e)


@bot.command()
async def coin(ctx, number=1):
    coin_results = []
    try:
        await ctx.send(f"Flipping coins...")
        for n in range(0,number):
            coin_results.append('head' if randint(1, 2) == 1 else 'Tail')
        await ctx.send(f"you got: {str(coin_results)}")
    except Exception as e:
        print('Error: ',e)


@bot.command()
async def dice(ctx, number=1):
    dice_results = []
    try:
        await ctx.send(f"Rolling dice...")
        for n in range(0,number):
            dice_results.append(randint(1, 6))
        await ctx.send(f"you got: {str(dice_results)}")
    except Exception as e:
        print('Error: ',e)

@dice.error
async def error_type(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('You need to specify a number of dices')
    if isinstance(error, commands.errors.ArgumentParsingError):
        await ctx.send('You need to specify a number as argument')

@gimme.error
async def error_type(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('You need to specify an argument')
    if isinstance(error, commands.errors.ArgumentParsingError):
        await ctx.send('You need to specify a ')
    if isinstance(error, commands.errors.BadArgument):
        await ctx.send('You need to specify a correct argument')

# EVENTS:

@bot.event
async def on_ready():
    print(f'Estamos dentro! {bot.user}')


@bot.event
async def on_member_join(member):
    url_mensaje_fijado = "https://discord.com/channels/1366602313975992414/1366602313975992417/1366875088288485416"  # mensaje específico
    canal_bienvenida = discord.utils.get(member.guild.text_channels, name='bienvenida-y-reglas')
    if canal_bienvenida:
        await canal_bienvenida.send(f"Wellcome {member.mention} to the server!, don't forget review the rules and useful commands: {url_mensaje_fijado}")
    else:
        print("Canal de bienvenida no encontrado.")

    

webserver.keep_alive()
bot.run(os.environ.get('TOKEN'))

