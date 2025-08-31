import os
from random import randint
from dotenv import load_dotenv

import requests
import webserver
import discord
from faker import Faker
from discord.ext import commands
from googletrans import Translator


translator = Translator()
fake = Faker()
load_dotenv()

# API POKEMON
API_POKEMON=os.getenv('API_POKEMON')

# CANALES
CHANNEL_WELLCOME=int(os.getenv('CANAL_INICIO'))
CHANNEL_RULES=int(os.getenv('CANAL_REGLAS'))
CHANNEL_SETUP=int(os.getenv('CANAL_CONFIG'))
CHANNEL_CODES=int(os.getenv('CANAL_CODIGOS'))

# ROLES
ROLE_NEW=int(os.getenv('ROL_NUEVO'))
ROLE_MEMBER=int(os.getenv('ROL_MIEMBRO'))


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)


# Comando de configuracion
@bot.command(name="soy")
async def configurar(ctx, trainer: str = None, code: str = None, team: str = None):
    """Comando para configurar usuario con alias y código"""

    # 1. Validar canal
    if ctx.channel.id != CHANNEL_SETUP:
        return await ctx.send("❌ Este comando solo se puede usar en el canal autorizado., "+str(ctx.channel.id))

    # 2. Validar rol
    role_verificacion = ctx.guild.get_role(ROLE_NEW)
    if role_verificacion not in ctx.author.roles:
        return await ctx.send("❌ No tienes el rol requerido para usar este comando.")

    # 3. Validar argumentos
    if trainer is None or code is None:
        return await ctx.send("⚠️ Uso correcto: `$soy <entrenador> <codigo_entrenador>`")

    if not code.isdigit():
        return await ctx.send("⚠️ El código debe ser numérico.")

    # 4. Asignar rol extra
    new_role = ctx.guild.get_role(ROLE_MEMBER)
    current_role = ctx.guild.get_role(ROLE_NEW)
    if new_role and current_role:
        await ctx.author.add_roles(new_role)
        await ctx.author.remove_roles(current_role)
        await ctx.send(f"✅ {ctx.author.mention}, has sido configurado con el nombre de entrenador **{trainer}** y código **{code}**. Haora eres {role_extra.name}!!")
    else:
        await ctx.send("⚠️ No se encontró el rol extra en el servidor.")
    
    # 5. Mandar datos a canal de logs
    canal_log = bot.get_channel(CHANNEL_CODES)
    if canal_log:
        await canal_log.send(
            f"📌 Nuevo miembro de la comunidad!!:\n"
            f"👤 Usuario: {ctx.author.mention}\n"
            f"📝 Nick name: **{trainer}**\n"
            f"🔢 Código de entrenador: **{code}**"
        )

    # 6. Bienvenida como miembro oficial
    canal_log = bot.get_channel(CHANNEL_WELLCOME)
    if canal_log:
        await canal_log.send(
            f"👤 **{ctx.author.mention}** Haora eres un miembro oficial de la comunidad!! 🍾🎉🎊"
        )


@bot.command()
async def poke(ctx, arg):
    try:
        pokemon = arg.split(' ',1)[0].lower()
        result = requests.get(f'{API_POKEMON}/{pokemon}')
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

    # Asignar rol
    role = member.guild.get_role(ROLE_NEW)
    if role:
        await member.add_roles(role)
        print(f"Rol {role.name} asignado a {member.name}")


    # Canal de reglas
    c_reglas = bot.get_channel(CHANNEL_RULES)

    # Canal de configuracion
    c_setup = bot.get_channel(CHANNEL_SETUP)

    # Mandar mensaje de bienvenida
    c_inicio = bot.get_channel(CHANNEL_WELLCOME)
    if c_inicio:
        await c_inicio.send(
            f'👋 Bienvenido al servidor {member.mention}, antes de darte acceso ' +
            f'a todas las caracteristicas del servidor, por favor te invito a pasar '+
            f'a leer nuestra normativa en <#{c_reglas}> y configurar ' +
            f'tu perfil en <#{c_setup}>'
            )
    else:
        print("Canal de bienvenida no encontrado.")


webserver.keep_alive()
bot.run(os.environ.get('TOKEN'))

