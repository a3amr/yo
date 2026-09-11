import os
import tempfile
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
import yt_dlp

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Server is running perfectly!"}

@app.get("/download")
async def download_audio(url: str = Query(..., description="YouTube Video URL")):
    try:
        temp_dir = tempfile.mkdtemp()
        
        ydl_opts = {
            'format': 'm4a/bestaudio/best',
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            base, _ = os.path.splitext(filename)
            final_filename = f"{base}.m4a"

        if os.path.exists(final_filename):
            return FileResponse(
                path=final_filename,
                media_type='audio/mp4',
                filename=os.path.basename(final_filename)
            )
        else:
            raise HTTPException(status_code=500, detail="File processing failed.")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
