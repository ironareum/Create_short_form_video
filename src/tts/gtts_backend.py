# 기본 구현 (옵션)
import tempfile, os
from gtts import gTTS
from moviepy.editor import AudioFileClip
from .base import TTSBackend


class GTTSBackend(TTSBackend):
    def synthesize(self, text: str):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts = gTTS(text=text, lang=self.cfg["voice"]["lang"])
        tts.save(tmp.name)
        dur = AudioFileClip(tmp.name).duration
        return tmp.name, float(dur)