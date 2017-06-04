from src.both_sides_bot_factory import BothSidesBotFactory

both_sides_bot = BothSidesBotFactory().buildBot()

both_sides_bot.process_inbox()
