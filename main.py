import os
import  warnings

warnings.filterwarnings("ignore", category=UserWarning, module="pygame.pkgdata")
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from time import sleep
from src.assistentbot import AssistentBot

if __name__ == "__main__":
    bot = AssistentBot()
    try:
        while True:
            bot.run()
    except KeyboardInterrupt:
        print("\nEncerrando o KaLLia-AI. Até a próxima!")
        sleep(5)
        print("\nEu voltarei...")
        sleep(1)

