import yt_dlp
from yt_dlp.utils import sanitize_filename


ytdl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': '%(title)s.%(ext)s',
    'nocheckcertificate': True,
    'quiet': False,
}


def download_audio(url, output_name='audio'):
    opts = ytdl_opts.copy()
    if output_name:
        safe_name = sanitize_filename(output_name)
        # usamos un placeholder de extensión
        # para que el postprocessor genere .mp3
        opts['outtmpl'] = safe_name + '.%(ext)s'

    with yt_dlp.YoutubeDL(opts) as ydl:
        # usamos extract_info para forzar descarga y
        # obtener metadata si la necesitamos
        ydl.extract_info(url, download=True)

    if output_name:
        return safe_name + '.mp3'
    return None
