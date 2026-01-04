# ============ IMPORTAÇÕES ============ #
import os
import json
from dotenv import load_dotenv

from art import text2art

from llm import LanguageLargeModel
from stt import SpeechToText
from tts import TextToSpeech


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

    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get("bot", {})

    def run(self):
        prompt = self.stt.run(
            stt_provider=self.config.get("stt_provider")
        )

        if not prompt:
            print("Nenhum áudio capturado...")
            raise KeyboardInterrupt
        elif prompt.lower() in ["e aí", "", "tchau", "legendado por paulo montenegro"]:
            return

        print("*"*90)
        print(f"\nVitor (Voice) 🗣️: {prompt}")
        response = self.llm.generate_response(prompt=prompt)
        print(f"KaLLia (Voice) 🤖: {response}\n")
        print("*"*90)

        self.tts.convert_with_edge_tts(response)


# ============ Execução ============ #
if __name__ == "__main__":
    bot = AssistentBot()
    try:
        while True:
            bot.run()
    except KeyboardInterrupt:
        print("Bot interrompido pelo usuário.")
