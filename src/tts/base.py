# TTS 백엔드 인터페이스
from abc import ABC, abstractmethod


class TTSBackend(ABC):
    def __init__(self, cfg):
        self.cfg = cfg


    @abstractmethod
    def synthesize(self, text: str):
        """Return (audio_path: str, duration_sec: float)"""
        raise NotImplementedError