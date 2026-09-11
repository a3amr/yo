FROM python:3.11-slim

# ffmpeg للتحويل الصوتي + node/npm لسيرفر التوكن + git لسحب الأكواد
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    git \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# سحب سيرفر التوكن وبناءه
RUN git clone https://github.com/Brainicism/bgutil-ytdlp-pot-provider.git /pot-provider \
    && cd /pot-provider/server \
    && npm install \
    && npx tsc

# باقي متطلبات المشروع
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# صلاحية تشغيل للسكربت
RUN chmod +x start.sh

CMD ["./start.sh"]
