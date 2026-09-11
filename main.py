from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
import yt_dlp
import os

app = FastAPI()

PROXY_URL = os.environ.get("PROXY_URL")  # حطها من Render Environment Variables

ATTEMPTS = [
    {"player_client": ["ios"]},
    {"player_client": ["android"]},
    {"player_client": ["web"]},
]

def build_opts(outtmpl, client_conf):
    opts = {
        'format': '140/bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': outtmpl,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '128',
        }],
        'extractor_args': {
            'youtube': client_conf,
            'youtubepot-bgutilhttp': {'base_url': 'http://127.0.0.1:4416'}
        },
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
    }
    if PROXY_URL:
        opts['proxy'] = PROXY_URL
    if os.path.exists('cookies.txt'):
        opts['cookiefile'] = 'cookies.txt'
    return opts

@app.get("/download")
async def download_audio(url: str, background_tasks: BackgroundTasks):
    outtmpl = '%(id)s.%(ext)s'
    last_error = None

    for attempt in ATTEMPTS:
        opts = build_opts(outtmpl, attempt)
        filename = None
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = f"{info['id']}.m4a"

            if not os.path.exists(filename):
                raise Exception("الملف لم يُنشأ")

            background_tasks.add_task(os.remove, filename)
            return FileResponse(
                path=filename,
                filename=f"{info['title']}.m4a",
                media_type='audio/mp4'
            )
        except Exception as e:
            last_error = str(e)
            if filename and os.path.exists(filename):
                os.remove(filename)
            continue

    raise HTTPException(status_code=502, detail=f"فشلت كل المحاولات. آخر خطأ: {last_error}")
