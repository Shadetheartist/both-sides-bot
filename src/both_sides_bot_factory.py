import praw
import os

# storage
from src.storage.file_storage import FileStorage

# poster
from src.poster.test_poster import TestPoster
from src.poster.standard_poster import StandardPoster

# output
from src.output.unintrusive_standard_output import UnintrusiveStandardOutput
from src.output.unintrusive_standard_output import StandardOutput

# comparator
from src.sub_comparor.hot_post_sub_comparor import HotPostSubComparor

# inbox processor
from src.inbox_processor.user_black_list_inbox_processor import UserBlacklistInboxProcessor
from src.inbox_processor.multi_processor_inbox_processor import MultiProcessorInboxProcessor
from src.inbox_processor.compare_request_inbox_processor import CompareRequestInboxProcessor

# the bot
from src.both_sides_bot import BothSidesBot


class BothSidesBotFactory(object):

    def __init__(self):
        self.reddit = praw.Reddit('bot')

    def buildTestBot(self):

        print("*** Building Test Bot ***\n")

        reddit = self.reddit

        print("Initializing File Storage")
        script_path = dir_path = os.path.dirname(os.path.realpath(__file__))
        storage = FileStorage(
            compare_list_file_path=script_path + '/storage/compare_list.txt',
            post_history_file_path=script_path + '/storage/post_history.txt',
            sub_blacklist_file_path=script_path + '/storage/blacklisted_subs.txt',
            user_blacklist_file_path=script_path + '/storage/blacklisted_users.txt',
        )

        print("Initializing UnintrusiveStandardOutput")
        output = UnintrusiveStandardOutput(storage)

        print("Initializing StandardPoster")
        poster = StandardPoster(reddit, output, storage, force_post=True)

        print("Initializing HotPostSubComparor")
        comparor = HotPostSubComparor(
            reddit, storage, post_search_limit=500, num_comments_needed_to_care=1)

        processors = [
            UserBlacklistInboxProcessor(reddit, storage),
            CompareRequestInboxProcessor(reddit, poster, storage)
        ]

        print("Initializing MultiProcessorInboxProcessor")
        inbox_processor = MultiProcessorInboxProcessor(processors)

        print("Initializing BothSidesBot")
        both_sides_bot = BothSidesBot(
            reddit, comparor, storage, poster, inbox_processor)

        return both_sides_bot

    def buildBot(self):

        print("*** Building [REAL BOY] Bot ***\n")

        reddit = self.reddit

        print("Initializing File Storage")
        script_path = dir_path = os.path.dirname(os.path.realpath(__file__))
        storage = FileStorage(
            compare_list_file_path=script_path + '/storage/compare_list.txt',
            post_history_file_path=script_path + '/storage/post_history.txt',
            sub_blacklist_file_path=script_path + '/storage/blacklisted_subs.txt',
            user_blacklist_file_path=script_path + '/storage/blacklisted_users.txt',
        )

        print("Initializing StandardOutput")
        output = StandardOutput(storage)

        print("Initializing StandardPoster")
        poster = StandardPoster(reddit, output, storage, force_post=True)

        print("Initializing HotPostSubComparor")
        comparor = HotPostSubComparor(
            reddit, storage, post_search_limit=500, num_comments_needed_to_care=1)

        processors = [
            UserBlacklistInboxProcessor(reddit, storage),
            CompareRequestInboxProcessor(reddit, poster, storage)
        ]

        print("Initializing MultiProcessorInboxProcessor")
        inbox_processor = MultiProcessorInboxProcessor(processors)

        print("Initializing BothSidesBot")
        both_sides_bot = BothSidesBot(
            reddit, comparor, storage, poster, inbox_processor)

        return both_sides_bot
