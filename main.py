from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
import yt_dlp
import os

app = FastAPI()

@app.get("/download")
async def download_audio(url: str, background_tasks: BackgroundTasks):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '192',
        }],
        'extractor_args': {
            'youtubepot-bgutilhttp': {
                'base_url': 'http://127.0.0.1:4416'
            }
        },
        'quiet': True,
        'no_warnings': True,
    }

    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'

    filename = None
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = f"{info['id']}.m4a"

        if not os.path.exists(filename):
            raise HTTPException(status_code=500, detail="فشل إنشاء الملف الصوتي بعد التحميل")

        background_tasks.add_task(os.remove, filename)

        return FileResponse(
            path=filename,
            filename=f"{info['title']}.m4a",
            media_type='audio/mp4'
        )

    except yt_dlp.utils.DownloadError as e:
        raise HTTPException(status_code=502, detail=f"خطأ من يوتيوب: {str(e)}")

    except Exception as e:
        if filename and os.path.exists(filename):
            os.remove(filename)
        raise HTTPException(status_code=500, detail=str(e))
