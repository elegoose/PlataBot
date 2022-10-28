import discord
import steamfront
import requests
import locale
from discord.ext import commands, tasks
from steamfront import errors

steam = steamfront.Client()
with open('credentials.txt') as f:
    credentialsArray = f.read().splitlines()
token = credentialsArray[0]
API_KEY = credentialsArray[1]
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
rate_ars_clp, rate_usd_ars, rate_usd_clp = 0, 0, 0
client = commands.Bot(command_prefix='.', intents=intents)


@client.event
async def on_ready():
    locale.setlocale(locale.LC_NUMERIC, "es_cl")
    rate.start()
    print('PlataBot listo')


@client.command()
async def tasa(ctx):
    cien_pesos_argentinos_clp = rate_ars_clp * 100
    mil_pesos_chilenos_ars = (rate_usd_ars / rate_usd_clp) * 1000
    embed = discord.Embed(title='Tasa de cambio de ARS y CLP respecto al dólar (USD)',
                          colour=discord.Color.brand_green())
    embed.add_field(name="Tasa de cambio argentina",
                    value='1 dólar (USD) equivale a ' + f'{round(rate_usd_ars, 2):n}' + ' pesos argentinos (ARS)',
                    inline=False)
    embed.add_field(name="Tasa de cambio chilena",
                    value='1 dólar (USD) equivale a ' + f'{round(rate_usd_clp):n}' + ' pesos chilenos (CLP)',
                    inline=False)
    embed.add_field(name="Tasa de cambio chile/argentina",
                    value='100 ARS equivalen a ' + f'{round(cien_pesos_argentinos_clp):n}' +
                          ' CLP\n1.000 CLP equivalen a ' + f'{round(mil_pesos_chilenos_ars, 2):n}' + ' ARS',
                    inline=False)
    await ctx.send(embed=embed)
    print('1 peso argentino (ARS) equivale a ' + str(rate_ars_clp) + ' pesos chilenos (CLP)')


@client.command()
async def precio(ctx, *args):
    juego = ''
    ''
    for palabra in args:
        juego += palabra
        juego += ' '
    # SI NO ES BUNDLE
    try:
        game = steam.getApp(name=juego[:-1], caseSensitive=False)
        nombre = game.name
        game_id = str(game.appid)
    except errors.AppNotFound:
        await ctx.send('Juego o dlc no encontrado. Por favor, escribe el nombre exacto (no importan las mayúsculas).')
        return
    link_store = 'https://store.steampowered.com/app/' + game_id

    # STORE ARGENTINA
    urljuego_ars = 'https://store.steampowered.com/api/appdetails?appids=' + game_id + '&cc=ar&l=en'
    r_ars = requests.get(url=urljuego_ars)
    dic_ars = r_ars.json()
    imagen = dic_ars[game_id]["data"]["header_image"]

    # Obtener tipo de juego
    # SI ES JUEGO BASE
    if dic_ars[game_id]['data']['type'] == 'game':
        tipo = 'Juego Base'
        if game.is_free:
            embed = discord.Embed(title=nombre, description='Este juego es gratis!', colour=discord.Color.green(),
                                  url=link_store, )
            embed.set_image(url=imagen)
            await ctx.send(embed=embed)
            return
        if game.price_overview is None:
            embed = discord.Embed(title=nombre,
                                  description='Hubo un problema al obtener el precio de este juego, puede que ya no '
                                              'este disponible en la tienda, o que aún no haya salido.',
                                  colour=discord.Color.red(), url=link_store, )
            embed.set_image(url=imagen)
            await ctx.send(embed=embed)
            return

    elif dic_ars[game_id]['data']['type'] == 'dlc':
        tipo = 'DLC'
        if game.is_free:
            embed = discord.Embed(title=nombre, description='Este DLC es gratis!', colour=discord.Color.green(),
                                  url=link_store, )
            embed.set_image(url=imagen)
            await ctx.send(embed=embed)
            return
        if game.price_overview is None:
            embed = discord.Embed(title=nombre,
                                  description='No se pudo obtener el precio de este DLC. Esto pasa a veces porque el '
                                              'DLC no se vende por separado.',
                                  colour=discord.Color.red(), url=link_store, )
            embed.set_image(url=imagen)
            await ctx.send(embed=embed)
            return
    # Precio Argentina
    precio_ars_texto = dic_ars[game_id]["data"]["price_overview"]["final_formatted"][5:]
    # STORE CHILE
    urljuego_clp = 'https://store.steampowered.com/api/appdetails?appids=' + game_id + '&cc=cl&l=en'
    r_clp = requests.get(url=urljuego_clp)
    dic_clp = r_clp.json()
    # Precio Chile
    precio_clp_texto = dic_clp[game_id]["data"]["price_overview"]["final_formatted"][5:]

    # PRECIO ARGENTINA
    precio_ars = float(precio_ars_texto.replace('.', '').replace(',', '.'))
    if len(str(precio_ars).split('.')[1]) == 1:
        precio_ars_texto = f"{int(str(precio_ars)[:-2]):,}".replace(',', '.') + precio_ars_texto[-3:]
    else:
        precio_ars_texto = f"{int(str(precio_ars)[:-3]):,}".replace(',', '.') + precio_ars_texto[-3:]
    precio_ars_to_clp_valor = round(precio_ars * rate_ars_clp)
    precio_ars_to_clp = f"{precio_ars_to_clp_valor:,}".replace(',', '.')

    # PRECIO CHILE
    precio_clp = float(precio_clp_texto.replace('.', '').replace(',', '.'))
    precio_clp_texto = f"{int(str(round(precio_clp))):,}".replace(',', '.')
    precio_clp_to_ars = '%.2f' % (precio_clp * (1 / rate_ars_clp))  # es un string
    precio_clp_to_ars = precio_clp_to_ars.replace('.', ',')
    precio_clp_to_ars = f"{int(precio_clp_to_ars[:-3]):,}".replace(',', '.') + precio_clp_to_ars[-3:]

    # COMPARACIÓN
    if precio_ars_to_clp_valor > precio_clp:
        comparacion = 'Este ' + tipo + ' es más caro en Argentina, ya que'
        incremento = precio_ars_to_clp_valor - precio_clp
        valor = (incremento / precio_clp) * 100
        porcentaje = ' es un ' + '%.2f' % valor + '% más caro en Argentina que en Chile.'
    else:
        comparacion = 'Este ' + tipo + ' es más barato en Argentina.'
        valor = 100 - (precio_ars_to_clp_valor / precio_clp) * 100
        porcentaje = ' Cuesta un ' + '%.2f' % valor + '% más barato en Argentina que en Chile.'
    if abs(valor) <= 5:
        comparacion = 'Este ' + tipo + ' cuesta prácticamente lo mismo en Chile y Argentina, ya que '
        porcentaje = 'tienen una diferencia del ' + '%.2f' % valor + '%'

    embed = discord.Embed(title=nombre, description=tipo, colour=discord.Color.blue(), url=link_store, )
    embed.set_image(url=imagen)
    embed.add_field(name="Precio en Argentina",
                    value='$' + precio_ars_texto + ' pesos argentinos (ARS), que serían $' + str(
                        precio_ars_to_clp) + ' en pesos chilenos (CLP).', inline=False)
    embed.add_field(name='Precio en Chile',
                    value='$' + precio_clp_texto + ' CLP, que serían $' + precio_clp_to_ars + ' ARS', inline=False)
    embed.add_field(name='Diferencia de precio', value=comparacion + porcentaje, inline=False)
    await ctx.send(embed=embed)


@tasks.loop(seconds=3600)
async def rate():
    global rate_ars_clp, rate_usd_ars, rate_usd_clp  # para modificar el valor global de las rates

    url = "https://api.apilayer.com/fixer/latest?symbols=ARS%2CCLP&base=USD"

    payload = {}
    headers = {
        "apikey": API_KEY
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_dict = response.json()
    # USD TO ARS
    rate_usd_ars = response_dict['rates']['ARS']

    # USD TO CLP
    rate_usd_clp = response_dict['rates']['CLP']

    # ARS TO CLP
    rate_ars_clp = rate_usd_clp / rate_usd_ars
    print('RATE ARS-CLP: ' + str(rate_ars_clp))


client.run(token)
