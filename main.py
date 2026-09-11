from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
import yt_dlp
import os

app = FastAPI()

@app.get("/download")
async def download_audio(url: str, background_tasks: BackgroundTasks):
    # إعدادات yt_dlp النهائية باستخدام عميل الـ mweb بدون كوكيز
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '192',
        }],
        'extractor_args': {'youtube': ['client=mweb,ios']},  # دمج عميل الموبايل لتجاوز الفحص تماماً
        'quiet': True,
        'no_warnings': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = f"{info['id']}.m4a"

        # حذف الملف من سيرفر Render تلقائياً بعد الإرسال
        background_tasks.add_task(os.remove, filename)

        return FileResponse(
            path=filename,
            filename=f"{info['title']}.m4a",
            media_type='audio/mp4'
        )

    except Exception as e:
        return {"error": str(e)}
