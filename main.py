from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
import yt_dlp
import os

app = FastAPI()

@app.get("/download")
async def download_audio(url: str, background_tasks: BackgroundTasks):
    # إعدادات yt-dlp المحدثة لتجاوز حظر يوتيوب واستخدام عميل الأندرويد والكوكيز
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '192',
        }],
        'cookiefile': 'cookies.txt',
        'extractor_args': {'youtube': ['client=android']},  # الحل الجذري لتجاوز خطأ "The page needs to be reloaded"
        'quiet': True,
        'no_warnings': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = f"{info['id']}.m4a"

        # حذف الملف من سيرفر Render فور انتهاء الإرسال لتوفير المساحة
        background_tasks.add_task(os.remove, filename)

        return FileResponse(
            path=filename,
            filename=f"{info['title']}.m4a",
            media_type='audio/mp4'
        )

    except Exception as e:
        return {"error": str(e)}
