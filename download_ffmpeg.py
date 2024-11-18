import os

from ffmpeg_downloader import installed, add_path


def setup_ffmpeg():
    if not installed("ffmpeg"):
        os.system("ffdl install --add-path")
        print("FFmpeg установлен.")
    else:
        print("FFmpeg уже установлен.")
    add_path()


if __name__ == "__main__":
    setup_ffmpeg()
