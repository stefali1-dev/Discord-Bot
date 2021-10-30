import discord, random, asyncio
from selenium import webdriver
from discord.ext import commands
from hello import stringToHex
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings("ignore")

bot = commands.Bot(command_prefix = "!")

async def user_aparitii_cuv(channel_id):

    print("Ma pun la treaba")

    channel = bot.get_channel(channel_id)
    autori_mesaje = {}
    cuvinte_useri = {}
    aparitii_cuv = {}
    aparitii_cuv_user = {}

    async for elem in channel.history(limit=None):
        author_id = str(elem.author)
        author_id = author_id[:-5]
        if elem.content:
            try:
                autori_mesaje[author_id].append(elem.content)
            except:
                autori_mesaje[author_id] = []
                autori_mesaje[author_id].append(elem.content)
                # am luat toate mesajele de la useri

            try:
                for cuv in elem.content.split():
                    cuvinte_useri[author_id].append(cuv)
            except:
                cuvinte_useri[author_id] = []
                for cuv in elem.content.split():
                    cuvinte_useri[author_id].append(cuv)
                    # am luat toate cuvintele de la useri
    for user in cuvinte_useri:
        for cuvant in cuvinte_useri[user]:
            try:
                aparitii_cuv[cuvant] += 1;
            except:
                aparitii_cuv[cuvant] = 1;
        copy = aparitii_cuv.copy()
        aparitii_cuv_user[user] = copy
        # stocheaza cuvintele cu aparitii cu fiecare user
        aparitii_cuv.clear()

    return aparitii_cuv_user

@bot.event
async def on_ready():
    print("Bot is ready!!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
                                                        name="Brate si Piept"))

@bot.command()
async def plot(ctx, *, txt):
    driver = webdriver.Chrome()

    url = 'https://www.wolframalpha.com/input/?i=' + stringToHex(txt)

    driver.get(url)

    arr = []
    seconds = 0

    while not arr:
        imgs = driver.find_elements_by_tag_name('img')

        for element in imgs:

            alt_atr = element.get_attribute("alt")

            if alt_atr == 'Plots' or alt_atr == 'Plot' or alt_atr == 'Polar plot':
                src = element.get_attribute("src")
                arr.append(src)

        await asyncio.sleep(1)
        seconds += 1
        if seconds > 11:
            break

    driver.close()

    if not arr:
        await ctx.reply('Not a function or computation time exceeded')

    else:
        await ctx.channel.send('**Graficul functiei**: ' + txt)
        for link in arr:
            await ctx.channel.send(link)


@bot.command()
async def ceva_deep(ctx):

    file = open("citate.txt", "r")

    lines = file.readlines()
    indice = random.randint(1, 729)
    random_line = lines[indice]

    if random_line == "\n":
        random_line = lines[indice-1]

    poz1 = random_line.find(".") + 2
    poz2 = random_line.find("_") - 1
    random_line = random_line[poz1: poz2]

    await ctx.send(random_line)

"""
@bot.command()
async def exec(ctx, *, command):
    command = command.replace("!n", "\n")
    command = command.replace("!t", "\t")
    execc(command)
    f = open("printed.txt", "r")
    try:
        await ctx.send(f.read())
    except:
        await ctx.send("```Ai intrecut maximul de 2000 caractere.```")
"""

@bot.command()
async def utilizari(ctx, user):
    user_id = int(user[3:-1])
    user_ = await bot.fetch_user(user_id)

    user_name = user_.name

    channel = ctx.channel

    name_canal = channel.name
    cuv_aparitii_user = await user_aparitii_cuv(channel.id)

    if channel.id == 613486318219034626:
        channel = bot.get_channel(780152771424813076)

    d = cuv_aparitii_user[user_name]
    aparitii_sortate = sorted(d.items(), key=lambda x: x[1], reverse=True)
    i=0
    cuvinte_utilizate = []
    aparitii_cuv_util = []
    for elem in aparitii_sortate:
        i +=1
        if i<=10:
            cuvinte_utilizate.append(elem[0])
            aparitii_cuv_util.append(elem[1])

    np.random.seed(19680801)

    plt.rcdefaults()
    fig, ax = plt.subplots()

    people = cuvinte_utilizate
    y_pos = np.arange(len(people))
    performance = aparitii_cuv_util

    ax.barh(y_pos, performance, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(people)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Utilizari')
    ax.set_title('10 cele mai utilizate cuvinte de '+user_name)

    fig.set_size_inches(10, 6)
    plt.savefig('info.png')
    await asyncio.sleep(5)
    file = discord.File("./info.png")
    await channel.send(
        "\n***-----*** Informatii " + user + " de pe canalul '" + name_canal + "' ***-----***" +
        "\n\n\nCele mai utilizate **10 cuvinte** sunt:")
    await channel.send(file=file)

@bot.command()
async def da_mesaj(ctx, channel_id, message):

    channel = await bot.fetch_channel(channel_id)

    await channel.send(message)

@bot.command()
async def aparitii(ctx, mesaj):
    channel = ctx.channel

    if channel.id == 613486318219034626:
        channel2 = bot.get_channel(780152771424813076)
        await channel2.send("Am preluat cerinta, dureaza cam 5 minute :nerd:")

    nume_canal = channel.name
    aparitii_cuv_user = await user_aparitii_cuv(channel.id)

    user_list = []
    aparitii_list = []
    for user in aparitii_cuv_user:
        ok = 0
        for cuvant in aparitii_cuv_user[user]:
            if cuvant == mesaj:
                aparitii_list.append(aparitii_cuv_user[user][cuvant])
                user_list.append(user)

    np.random.seed(19680801)

    plt.rcdefaults()
    fig, ax = plt.subplots()

    people = user_list
    y_pos = np.arange(len(people))
    performance = aparitii_list

    ax.barh(y_pos, performance, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(people)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Utilizari cuvant "'+mesaj+'"')
    ax.set_title('AndreiDeiuBot3.0')

    fig.set_size_inches(10, 6)
    plt.savefig('info.png')
    await asyncio.sleep(5)
    file = discord.File("./info.png")

    if channel.id == 613486318219034626:
        channel = bot.get_channel(780152771424813076)

    await channel.send('Utilizarile cuvantului "'+mesaj+'" in canalul "'+nume_canal+'".')
    await channel.send(file=file)


bot.run("Nzc4NTU0MTE3MzkxNjQ2NzUw.X7TrBg.Sq6EKAb3AU9lz1TQ36m2666d_mI")
