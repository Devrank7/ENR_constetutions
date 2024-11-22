import os
from abc import ABC, abstractmethod

import pytesseract
from PIL import Image
from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.types import Message
from moviepy.audio.io.AudioFileClip import AudioFileClip
from pydub import AudioSegment
import speech_recognition as sr


def recognize_speech(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language="ru-RU")
        return text


class Recognize(ABC):

    def __init__(self, message: Message) -> None:
        self.message = message

    async def recognize(self) -> str:
        file_id = self.get_file_id()
        file = await self.message.bot.get_file(file_id)
        file_path = file.file_path
        audio_path, another_path = await self.get_path(file_path, file_id)
        text = recognize_speech(audio_path)
        os.remove(audio_path)
        os.remove(another_path)
        return text

    @abstractmethod
    def get_file_id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get_path(self, file_path: str, file_id: str) -> tuple[str, str]:
        raise NotImplementedError


class VoiceRecognize(Recognize):

    def get_file_id(self) -> str:
        return self.message.voice.file_id

    async def get_path(self, file_path: str, file_id: str) -> tuple[str, str]:
        voice_path = f"{file_id}.ogg"
        await self.message.bot.download_file(file_path, voice_path)
        ogg_audio = AudioSegment.from_ogg(voice_path)
        wav_path = f"{file_id}.wav"
        ogg_audio.export(wav_path, format="wav")
        return wav_path, voice_path


class VideoRoundRecognize(Recognize):

    def get_file_id(self) -> str:
        return self.message.video_note.file_id

    async def get_path(self, file_path: str, file_id: str) -> tuple[str, str]:
        video_path = f"{file_id}.mp4"
        await self.message.bot.download_file(file_path, video_path)
        audio_path = f"{file_id}.wav"
        with AudioFileClip(video_path) as video:
            print(video.duration)
            video.write_audiofile(audio_path)
        return audio_path, video_path


class SegmentedVoiceRecognize(VoiceRecognize):

    async def recognize(self) -> list[str]:
        file_id = self.get_file_id()
        file = await self.message.bot.get_file(file_id)
        file_path = file.file_path
        audio_path, another_path = await self.get_path(file_path, file_id)

        try:
            segments = self.split_audio(audio_path, chunk_length_ms=45000)  # Разделяем аудио на части по 45 секунд
            texts = []
            for segment in segments:
                segment.export("temp_segment.wav", format="wav")  # Сохраняем временный сегмент
                text = recognize_speech("temp_segment.wav")  # Распознаем сегмент
                texts.append(text)
                os.remove("temp_segment.wav")  # Удаляем временный файл после обработки
        finally:
            os.remove(audio_path)
            os.remove(another_path)

        return texts

    def split_audio(self, audio_path: str, chunk_length_ms: int) -> list[AudioSegment]:
        audio = AudioSegment.from_file(audio_path)
        chunks = [audio[start:start + chunk_length_ms] for start in range(0, len(audio), chunk_length_ms)]
        return chunks


class PhotoRecognize(Recognize):

    async def recognize(self) -> str:
        photo = self.message.photo[-1]
        file_info = await self.message.bot.get_file(photo.file_id)
        file_path = file_info.file_path
        photo_file = f"downloads/{photo.file_id}.jpg"  # Локальный путь для сохранения
        await self.message.bot.download_file(file_path, photo_file)
        try:
            image = Image.open(photo_file)
            extracted_text = pytesseract.image_to_string(image, lang="rus")
            print("extract: ", extracted_text)
            os.remove(file_path)
            return extracted_text
        except Exception as e:
            print("Exc: ", e)
            return "No"

    def get_file_id(self) -> str:
        pass

    async def get_path(self, file_path: str, file_id: str) -> tuple[str, str]:
        pass


recognize_type = {
    ContentType.VOICE: VoiceRecognize,
    ContentType.VIDEO_NOTE: VideoRoundRecognize,
    ContentType.PHOTO: PhotoRecognize,
}
