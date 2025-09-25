# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install ffmpeg, a system dependency for Whisper
RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Expose the standard Hugging Face port
EXPOSE 7860

# Run the app on port 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
