# ============ Importação ============= #
import os
import io
import json
import pygame
import asyncio
import warnings
from dotenv import load_dotenv

from edge_tts import Communicate


# ============ Constantes ============ #
_ = load_dotenv('.env')
warnings.filterwarnings("ignore", category=UserWarning, module="pygame.pkgdata")
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


# ============== Código =============== #
class TextToSpeech:
    def __init__(self):
        self.config = self._load_config("config_bot.json")

        self.voice = self.config.get("voice", "pt-BR-FranciscaNeural")
        pygame.mixer.init()

    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get("tts", {})

    async def _edge_tts_async(self, text):
        communicate = Communicate(text, self.voice)
        audio_buffer = io.BytesIO()

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])

        audio_buffer.seek(0)
        return audio_buffer

    def _play_from_memory(self, audio_buffer):
        pygame.mixer.music.load(audio_buffer)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def convert_with_edge_tts(self, text):
        try:
            audio_buffer = asyncio.run(self._edge_tts_async(text))
            self._play_from_memory(audio_buffer)
        except Exception as e:
            print(f"Erro ao converter texto para áudio com Edge TTS: {e}")


# ============= Execução ============== #
if __name__ == "__main__":
    tts = TextToSpeech()
    tts.convert_with_elevenlabs("Ola, tudo bem?")
