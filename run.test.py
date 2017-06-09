import os
from src.both_sides_bot_factory import BothSidesBotFactory

base_path = dir_path = os.path.dirname(os.path.realpath(__file__))
both_sides_bot = BothSidesBotFactory(base_path).buildTestBot()

while(1):
    both_sides_bot.run('both_sides_test')
    print('Waiting 6 hours \n')
    time.sleep(hour_in_seconds * 6)

