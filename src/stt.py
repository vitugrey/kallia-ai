# ============ Importação ============= #
import os
import io
import json
import wave
import pyaudio
import keyboard
import numpy as np
from time import sleep
from dotenv import load_dotenv
from typing import Optional, List

import assemblyai as aai
from faster_whisper import WhisperModel


# ============ Constantes ============= #
_ = load_dotenv('.env')
ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')


# ============== Código =============== #
class SpeechToText:
    def __init__(self):
        self.config = self._load_config("config_bot.json")

    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get("stt", {})

    def record_manual(self) -> Optional[List[bytes]]:
        print(f"\nPressione e segure '{self.config["record_key"]}' para gravar. Solte para finalizar (ou Ctrl+C para cancelar).\n")
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=self.config["channels"],
            rate=self.config["rate"],
            input=True,
            frames_per_buffer=self.config["chunk"]
        )
        frames = []
        try:
            c=0
            while not keyboard.is_pressed(self.config["record_key"]):
                # (01)
                # c+=1
                # print(f"{c} - Aguardando gravação...")
                sleep(0.3)
                pass
            while keyboard.is_pressed(self.config["record_key"]):
                data = stream.read(self.config["chunk"], exception_on_overflow=False)
                frames.append(data)
        except KeyboardInterrupt:
            print("Gravação cancelada.")
            return None
        except Exception as e:
            print(f"Erro durante a gravação: {e}")
            return None
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
        return frames if frames else None

    def get_audio_bytes(self, frames: List[bytes]) -> bytes:
        """Converte frames em bytes WAV em memória."""
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wf:
            wf.setnchannels(self.config["channels"])
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.config["rate"])
            wf.writeframes(b''.join(frames))
        buffer.seek(0)
        return buffer.read()

# Transcrição Local whisper
    def transcribe_whisper(self, audio_bytes: bytes, model_size: Optional[str] = None,
                           compute_type: Optional[str] = None, device: Optional[str] = None) -> Optional[str]:
        model_size = model_size or self.config["whisper_model_size"]
        compute_type = compute_type or self.config["whisper_compute_type"]
        device = device or self.config["whisper_device"]
        try:
            # Converter bytes para numpy array
            audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            model = WhisperModel(model_size, device=device, compute_type=compute_type)
            segments, _ = model.transcribe(audio_np, language='pt')
            transcription = " ".join(segment.text for segment in segments).strip()
            return transcription.capitalize()
        except Exception as e:
            print(f"Erro na transcrição Whisper: {e}")
            return None

# Transcrição Online AssemblyAI 
    def transcribe_assemblyai(self, audio_bytes: bytes, api_key: Optional[str] = None) -> Optional[str]:
        key = api_key or ASSEMBLYAI_API_KEY
        if not key:
            print("API key para AssemblyAI não fornecida.")
            return None
        aai.settings.api_key = key
        config = aai.TranscriptionConfig(language_code="pt")
        transcriber = aai.Transcriber(config=config)
        try:
            transcript = transcriber.transcribe(data=audio_bytes)
            return transcript.text
        except Exception as e:
            print(f"Erro na transcrição AssemblyAI: {e}")
            return None


    def run(self, stt_provider: str = "assemblyai", **kwargs) -> Optional[str]:
        frames = self.record_manual()
        if frames:
            audio_bytes = self.get_audio_bytes(frames)
            if stt_provider == "assemblyai":
                return self.transcribe_assemblyai(audio_bytes, **kwargs)
            elif stt_provider == "whisper":
                return self.transcribe_whisper(audio_bytes, **kwargs)
            else:
                print("Método inválido.")
                return None
        return None

# ============= Execução ============== #
if __name__ == "__main__":
    stt = SpeechToText()
    result = stt.run(method="whisper")
    if result:
        print(f"Transcrição: {result}")
    else:
        print("Nenhuma transcrição gerada.")
