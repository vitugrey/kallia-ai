# ============ IMPORTAÇÕES ============ #
import os
import json
import time
import random
import threading
from dotenv import load_dotenv

from art import text2art

from .stt import SpeechToText
from .tts import TextToSpeech
from .llm import LanguageLargeModel


# ============ Constantes ============ #
_ = load_dotenv('.env')


# ============ Código ============ #
class AssistentBot:
    def __init__(self):
        self.config = self._load_config("config_bot.json")

        self.stt = SpeechToText()
        self.llm = LanguageLargeModel()
        self.tts = TextToSpeech()

        os.system('cls' if os.name == 'nt' else 'clear')
        print(text2art("KaLLia-AI", space=4))
        print(self.config.get("llm").get("instruction").get("role"))

    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config

    def generate(self):
        while True:
            try:
                prompt = self.stt.run(
                    stt_provider=self.config.get("stt").get("stt_provider")
                )

                if not prompt:
                    raise KeyboardInterrupt
                elif prompt.lower() in ["e aí", "", "tchau", "legendado por paulo montenegro"]:
                    return

                print("*"*90)
                print(f"\nVitor (Voice) 🗣️: {prompt}")
                response = self.llm.generate_response(prompt=prompt)
                print(f"KaLLia (Voice) 🤖: {response}\n")
                print("*"*90)

                self.tts.convert_with_edge_tts(response)
            except KeyboardInterrupt:
                raise

    def skill_in_background(self):
        while True:
            try:
                skills = self.config.get("skill", [])
                prompt = random.choice(skills) if skills else None
                if not prompt:
                    time.sleep(10)
                    continue

                print("*"*90)
                print(f"\nVitor (Mente) 🗣️: {prompt}")
                response = self.llm.generate_response(prompt=prompt)
                print(f"KaLLia (Voice) 🤖: {response}\n")
                print("*"*90)
                time.sleep(2)
                print(f"\nPressione e segure 'CAPS_LOOK' para gravar. Solte para finalizar (ou Ctrl+C para cancelar).\n")

                self.tts.convert_with_edge_tts(response)

                time.sleep(500)
            except KeyboardInterrupt:
                raise

    def run(self):
        threading.Thread(target=self.skill_in_background, daemon=True).start()
        self.generate()


# ============ Execução ============ #
if __name__ == "__main__":
    bot = AssistentBot()
    try:
        while True:
            bot.run()
    except KeyboardInterrupt:
        print("Bot interrompido pelo usuário.")
