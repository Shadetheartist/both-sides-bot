from abc import ABC, abstractmethod
from src.inbox_processor.base_inbox_processor import BaseInboxProcessor
import praw
from src.poster.base_poster import BasePoster
from src.storage.base_storage import BaseStorage


class CompareRequestInboxProcessor(BaseInboxProcessor):

    def __init__(self, reddit, poster: BasePoster, storage: BaseStorage):
        self.reddit = reddit
        self.poster = poster
        self.storage = storage

    def process_inbox(self):
        print('Processing inbox for user requested comparisons...')

        for comment in self.reddit.inbox.unread():
            if 'please compare' in comment.body.lower():

                lines = comment.body.split('\n')

                for line in lines:
                    if line.lower().startswith('/u/'):
                        continue

                    if line.lower().startswith('u/'):
                        continue

                    if line.lower().startswith('please'):
                        continue

                    split_str = line.split()

                    if len(split_str) == 2:
                        left_post = praw.models.Submission(
                            self.reddit, id=split_str[0])

                        right_post = praw.models.Submission(
                            self.reddit, id=split_str[1])

                        new_post = self.poster.submit_post(
                            left_post, right_post, comment)

                        self.reply_to_compare(
                            comment, new_post, left_post, right_post)

    def reply_to_compare(self, comment, new_post, left_post=None, right_post=None):
        if self.storage.is_sub_blacklisted(comment.subreddit.sub_display_name):
            print("Tried to reply to mention, but we're blacklisted from the that sub.")
            return

        if new_post is not None:
            print("Replying to comment [", comment.id, "]")
            comment.reply("[Your wish has been granted, here is your link!]({0})".format(
                new_post.permalink))

        elif left_post is not None and right_post is not None:
            history_info = self.storage.get_post_info_from_left_right(
                left_post, right_post)

            center_post_id = history_info['center_post_id']
            
            center_post = praw.models.Submission(
                self.reddit, id=center_post_id)

            comment.reply("[Your wish could not be granted, a comparison has already been made.]({0})".format(
                center_post.permalink))
        else:
            comment.reply("(:0 ) i legit can't rn.".format())

        print("Marking comment read [", comment.id, "]")

        comment_list = list()
        comment_list.append(comment)

        self.reddit.inbox.mark_read(comment_list)
