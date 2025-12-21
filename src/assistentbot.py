# ============ IMPORTAÇÕES ============ #
import os
import time
from typing import List, Optional
import json

from pathlib import Path

from llm import LanguageLargeModel 
from stt import SpeechToText
from tts import TextToSpeech

# ============ CONSTANTES ============ #


# ============ Código ============ #


class AssistentBot:
    def __init__(self):
        self.config = self._load_config("config_bot.json")

        # Inicializar LLM e criar team
        self.stt = SpeechToText()
        self.llm = LanguageLargeModel()
        self.tts = TextToSpeech()

        self.session_id = "main_session"

    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get("bot", {})



    def run(self):
        print("Assistente Bot iniciado. Pressione Ctrl+C para sair.")
        prompt = self.stt.run(method="assemblyai")
        print(f"Usuário: {prompt}")

        self.llm.make_team()

        response = self.llm.generate_response(prompt=prompt, session_id=self.session_id)
        # print(f"Bot: {response}")

        self.tts.convert_with_edge_tts(response)
        # (06) log
        





# ============ Run server ============ #
if __name__ == "__main__":
    bot = AssistentBot()
    try:
        while True:
            bot.run()
    except KeyboardInterrupt:
        print("\nBot interrompido pelo usuário.")
