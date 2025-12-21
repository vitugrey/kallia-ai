import asyncio
import io
import pygame
import json

from edge_tts import Communicate


# (08) testa outras vozes
class TextToSpeech:
    def __init__(self):
        self.config = self._load_config("config_bot.json")

        self.voice = self.config.get("voice", "pt-BR-FranciscaNeural")
        pygame.mixer.init()

    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get("tts", {})

    def convert_with_edge_tts(self, text):
        try:
            audio_buffer = asyncio.run(self._edge_tts_async(text))
            self._play_from_memory(audio_buffer)
        except Exception as e:
            print(f"Erro ao converter texto para áudio com Edge TTS: {e}")

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


if __name__ == "__main__":
    tts = TextToSpeech()
    tts.convert_with_edge_tts("Ola, tudo bem?")
