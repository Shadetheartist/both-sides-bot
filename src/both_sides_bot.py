import praw

from src.sub_comparor.base_sub_comparor import BaseSubComparor
from src.storage.base_storage import BaseStorage
from src.poster.base_poster import BasePoster
from src.inbox_processor.base_inbox_processor import BaseInboxProcessor


class BothSidesBot(object):

    #dependency injection pattern if you were wondering...
    def __init__(
            self,
            reddit,
            sub_comparor: BaseSubComparor,
            storage: BaseStorage,
            poster: BasePoster,
            inbox_processor : BaseInboxProcessor
        ):
        self.reddit = reddit
        self.sub_comparor = sub_comparor
        self.storage = storage
        self.poster = poster
        self.inbox_processor = inbox_processor

    def run(self, post_to):
        print("Running BothSidesBot, posting to [{0}]".format(post_to))

        center_sub = self.reddit.subreddit(post_to)

        subs_to_compare = self.storage.get_subs_to_compare()

        for sub_pair in subs_to_compare:
            subs = sub_pair.split(' ')
            self.compare_subs(center_sub, subs[0], subs[1])

    def compare_subs(self, center, left, right):
        print("Comparing [{0}] and [{1}]. Posting to [{2}]".format(
            left, right, center))

        comparable_posts = self.sub_comparor.compare(left, right)

        for postPair in comparable_posts:
            self.post_to_center(center, postPair[0], postPair[1])

    def post_to_center(self, center, left_post, right_post):
        new_center_post = self.poster.submit_post(center, left_post, right_post)

    def process_inbox(self):
        new_center_post = self.inbox_processor.process_inbox()
