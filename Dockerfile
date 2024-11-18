# Базовый Python-образ
FROM python:3.10-slim
WORKDIR /bot
RUN python -m venv venv
COPY requirements.txt .
RUN . venv/bin/activate && pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . .
RUN . venv/bin/activate && echo "y" | ffdl install
RUN find /root/.local/share/ffmpeg-downloader/ffmpeg -type f -name "ffmpeg" -exec cp {} ./venv/bin/ffmpeg \; && \
    find /root/.local/share/ffmpeg-downloader/ffmpeg -type f -name "ffprobe" -exec cp {} ./venv/bin/ffprobe \;

# Установка исполняемых прав
RUN chmod +x ./venv/bin/ffmpeg ./venv/bin/ffprobe
ENV PATH="/bot/venv/bin:$PATH"
CMD ["./venv/bin/python", "main.py"]
