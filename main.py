import discord
from discord.ext import commands, tasks
from datetime import datetime
import os
from threading import Thread
# Fichiers persos
from webApp.keep_alive import keep_alive, updateLogs
from  commandEdouard.commandEdt.emploiDuTemps import getEdt, changerFuseau
from commandEdouard.commandTodo.todo import mainTodo
from commandEdouard.commandWiki.wiki import getRandomWiki


intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=('Edouard ', 'edouard '),
    description="Je suis le bot Ed0uard",
    intents=intents,
    case_insensitive=True)

def writeLog(message):
    time_ = changerFuseau(datetime.now())
    now = "[" + time_.strftime("%d/%m/%Y %H:%M:%S") + "]: "
    logText = now + message
    logFile = open("discord.log", "a")
    logFile.write(logText + "\n")
    logFile.close()
    print(logText)
    updateLogs(message, now)


def writeLogCommande(message, ctx):
    logText = f"Commande activée par {ctx.author.name} : {ctx.message.content}" + message
    writeLog(logText)


@bot.event
async def on_connect():
    await bot.change_presence(activity=discord.Game(name="Etre Ed0uard"))
    writeLog(f"Bot connecté en tant que {bot.user} avec les préfixes de commande : \"{bot.command_prefix}\"")
    sendEdtDaily.start()


@bot.event
async def on_member_join(member):
    userId = member.id
    f = open("commandEdouard/commandTodo/dataTodo/" + str(userId) + ".json", "w")
    f.write("[]")
    f.close() # Création et initialisation du fichier pour le stockage des Todo
    writeLog("Nouveau membre sur le serveur : " + member.name)


@bot.event
async def on_error(event, *args, **kwargs):
    if event == "on_message":
        writeLog(f"Erreur levée par un message : {args [0]}")
    elif event == "on_command_error":
        pass
    else:
        writeLog(f"Erreur levée : {args [0]}")
    raise  # Utile pour afficher les erreurs pendant la phase de développement


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"Commande non-valide : \"{ctx.message.content}\"")
    writeLog(f"Erreur levée par une commande mal utilisée : \"{error}\" de type {type(error)} causée par la commande \"{ctx.message.content}\" de {ctx.message.author}")
    raise error


@bot.event
async def on_message(message):
    if message.author == bot.user:
        pass
    else:
        author = message.author
        content = message.content
        if content.lower().startswith('salut'):
            reponse = "Bonjour " + author.mention + " !"
            await message.channel.send(reponse, tts=True)
            writeLog(f"Réponse au message de salutation de {author}")

        elif content.lower().startswith('dm me'):
            await author.create_dm()
            await author.dm_channel.send(f"Salut {author.name}, je suis là")
            writeLog(f"Nouveau DM à {author}")

        elif content.lower().startswith('merci edouard'):
            await message.channel.send(f"Je t'en prie {author.mention}")
            writeLog(f"Réponse au remerciement de {author}")

    await bot.process_commands(message)


###############
#  Commandes  #
###############

class dev(commands.Cog, name="Développement"):
    def __init__(self, bot):
        self.bot = bot
 
    @commands.command(help="Ping le bot")
    async def ping(self, ctx):
        await ctx.send("pong")
        writeLogCommande("", ctx)

    @commands.command(help="Effacer les logs du bot")
    async def clear(self, ctx):
        f = open("discord.log", "r")
        text = f.readlines()
        f.close()
        number = len(text)
        file = open("discord.log", "w")
        file.close()
        await ctx.send("Logs du bot effacés")
        writeLogCommande(f" -> Logs du bot effacés : {number} lignes supprimées", ctx)

    @commands.command(name="logs", help="Obtenir le lien vers la page des logs")
    async def logs(self, ctx):
        await ctx.send("http://projet-edouard.mart_84.repl.co/")
        writeLogCommande("", ctx)

class utilitaire(commands.Cog, name="Utilitaire"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='edt', aliases=["emploidutemps"], help="Afficher l'emploi du temps")
    async def edt(self, ctx, *args):
        if len(args) <= 2:
            message, action = getEdt(args)
        else:
            raise
        author = ctx.author
        embedColor = author.color
        e = discord.Embed(
            description=message,
            colour=embedColor,
            title="Emploi du temps",
            url='http://edt.univ-lyon1.fr/')
        await ctx.send(f"Emploi du temps de {author.mention}", embed=e)
        writeLogCommande(f" -> Affichage de l'emploi du temps : {action}", ctx)


    @commands.command(name="todo", help="Gérer la liste de Todo")
    async def todoCommande(self, ctx, *args):
        author = ctx.author
        userId = author.id
        message, action = mainTodo(args, userId)

        embedColor = author.color
        e = discord.Embed(description=message, colour=embedColor, title="Todo")
        await ctx.send(f"Todo liste de {author.mention}", embed=e)
        writeLogCommande(f" -> {action}", ctx)

    @commands.command(name="msg", help="Obtenir le lien vers la messagerie", aliases=["messagerie"])
    async def messagerie(self, ctx):
        await ctx.send("http://messagerie.mart_84.repl.co")
        writeLogCommande("", ctx)

    @commands.command(name="wiki", help="Obtenir un article aléatoire de Wikipédia", aliases=["wikipedia", "culture"])
    async def wikipedia(self, ctx):
        url, title, content = getRandomWiki()
        e = discord.Embed(
            description = content,
            title = title,
            url = url)
        await ctx.send("Un article Wikipédia sûrement très intéressant", embed=e)
        writeLogCommande(f" -> Article sur {title}", ctx)

@tasks.loop(minutes=5)
async def sendEdtDaily(*args):
    if datetime.now().hour == 17 and datetime.now().minute in range(0, 5): #Heure du fuseau horaire utc
        message, action = getEdt(["demain"])
        if not message == "Rien de spécial de prévu ce jour là":
            e = discord.Embed(
                description=message,
                title="Emploi du temps",
                url='http://edt.univ-lyon1.fr/')
            channel = bot.get_channel(798266944662142997)
            await channel.send("Emploi du temps", embed=e)
            writeLog(f"Envoi automatique de l'emploi du temps du {action}")


t = Thread(target=keep_alive)
t.start()  

bot.add_cog(dev(bot))
bot.add_cog(utilitaire(bot))
bot.run(os.getenv("TOKEN"))