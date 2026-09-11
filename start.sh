#!/bin/sh
set -e

echo "Starting POT token server..."
node /pot-provider/server/build/main.js &

# ننتظر ثانيتين لضمان إنو سيرفر التوكن جاهز قبل ما نبدأ uvicorn
sleep 2

echo "Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port $PORT
