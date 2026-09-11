FROM python:3.11-slim

# ffmpeg + node (لازم للـ POT provider)
RUN apt-get update && apt-get install -y ffmpeg nodejs npm git && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ثبّت بروفايدر التوكن كـ plugin لـ yt-dlp
RUN pip install --no-cache-dir bgutil-ytdlp-pot-provider

COPY . .
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
