from src.both_sides_bot_factory import BothSidesBotFactory

both_sides_bot = BothSidesBotFactory().buildTestBot()

both_sides_bot.run('both_sides_test')
