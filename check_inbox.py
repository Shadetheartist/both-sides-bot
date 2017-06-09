import os
import time
from src.both_sides_bot_factory import BothSidesBotFactory

base_path = dir_path = os.path.dirname(os.path.realpath(__file__))
both_sides_bot = BothSidesBotFactory(base_path).buildTestBot()



while(1):
    both_sides_bot.process_inbox()

    print('Waiting 5 minutes\n')
    time.sleep(60 * 5)