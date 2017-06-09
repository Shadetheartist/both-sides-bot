import os
import time

from src.both_sides_bot_factory import BothSidesBotFactory

base_path = dir_path = os.path.dirname(os.path.realpath(__file__))
both_sides_bot = BothSidesBotFactory(base_path).buildBot()

hour_in_seconds = 60 * 60

while(1):
    both_sides_bot.run('both_sides')

    print('Waiting 6 hours \n')
    time.sleep(hour_in_seconds * 6)
