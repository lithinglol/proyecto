import discord
from discord.ext import commands
import os
from gtts import gTTS
import bot_logic
# Inicializar el bot
intents = discord.Intents.default()
intents.message_content = True  # Para leer mensajes
bot = commands.Bot(command_prefix="!", intents=intents)


# Manejador de comando !start
@bot.command()
async def start(ctx):
    await ctx.send("¡Hola!")


@bot.command()
async def unir(ctx):
    connected = ctx.author.voice
    if connected:
        await connected.channel.connect()
    else:
        await ctx.send(
            'Por favor unete a un chat de voz antes de usar el comando'
        )


@bot.command()
async def salir(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()


@bot.command()
async def hablar(ctx, *, phrase):
    phrase_there = os.path.isfile('audio.mp3')
    if phrase_there:
        os.remove('audio.mp3')
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice:
        await ctx.send(
            "Debo estar conectado a un canal de voz para hablar. "
            "Usa !unir primero."
        )
        return
    speech = gTTS(text=phrase, lang='es', slow=False)
    speech.save('audio.mp3')
    voice.play(discord.FFmpegPCMAudio('audio.mp3'))


@bot.command()
async def youtube(ctx, *, url):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice:
        await ctx.send(
            "Debo estar conectado a un canal de voz para reproducir audio. "
            "Usa !unir primero."
        )
        return
    phrase_there = os.path.isfile('audio.mp3')
    if phrase_there:
        os.remove('audio.mp3')

    bot_logic.download_audio(url)

    voice.play(discord.FFmpegPCMAudio('audio.mp3'))


@bot.command()
async def terminar(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()


@bot.command()
async def pausar(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.pause()


@bot.command()
async def reanudar(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.resume()


@bot.command()
async def ayuda(ctx):
    help_text = (
        "Comandos disponibles:\n"
        "!start - Inicia el bot\n"
        "!unir - El bot se une a tu canal de voz\n"
        "!salir - El bot sale del canal de voz\n"
        "!hablar <frase> - El bot dice la frase en el canal de voz\n"
        "!youtube <url> - El bot reproduce el audio de un video de YouTube en"
        "el canal de voz\n"
        "!terminar - Detiene la reproducción actual\n"
        "!pausar - Pausa la reproducción actual\n"
        "!reanudar - Reanuda la reproducción pausada\n"
        "!ayuda - Muestra este mensaje de ayuda"
    )
    await ctx.send(help_text)


# Iniciar el bot
bot.run('YOUR_DISCORD_BOT_TOKEN')
