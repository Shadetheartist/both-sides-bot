import math
from abc import ABC, abstractmethod
from src.poster.base_poster import BasePoster
from src.output.base_output import BaseOutput
from src.storage.base_storage import BaseStorage
from src.output.output_helper import OutputHelper


class StandardPoster(BasePoster):

    def __init__(self, reddit, output: BaseOutput, storage: BaseStorage, force_post=False, comment_limit=20):
        self.reddit = reddit
        self.output = output
        self.storage = storage
        self.force_post = force_post
        self.comment_limit = comment_limit

    def submit_post(self, center_sub, left_post, right_post):

        post_info = self.output.build_post(left_post, right_post)

        new_center_post = None

        try:
            new_center_post = center_sub.submit(post_info[0], post_info[1])
        except Exception as ex:
            print("Error when submitting post")
            return

        self.add_comments(self.comment_limit, new_center_post, left_post, right_post)
        self.post_to_referenced_submissions(new_center_post, left_post, right_post)
        self.storage.add_post_to_history(new_center_post, left_post, right_post)

        return new_center_post

    def add_comments(self, limit, new_post, left_post, right_post):

        left_post.comment_sort = 'best'
        right_post.comment_sort = 'best'

        left_comments = self.get_valid_comments(left_post.comments)
        right_comments = self.get_valid_comments(right_post.comments)

        print("left-leaning comments found: ", len(left_comments))
        print("right-leaning comments found: ", len(right_comments))

        for i in range(0, min(math.floor(limit), len(OutputHelper.nth), len(left_comments), len(right_comments))):
            reply_body = self.output.build_reply(
                i, left_comments[i], right_comments[i])
            try:
                new_post.reply(reply_body)
            except Exception as ex:
                print("Error when submitting comment")
                print(str(ex))
                return

    def post_to_referenced_submissions(self, new_post, left_post, right_post):

        if not self.storage.is_sub_blacklisted(left_post.subreddit.display_name):
            left_to_right_notification_str = self.output.build_notification(
                new_post, left_post, right_post)
            try:
                print("Posting a notification to the left post")
                left_post.reply(left_to_right_notification_str)
            except Exception as ex:
                print("Couldnt post a comment to the to the left post")
                print(str(ex))
        else:
            print("We're blacklisted from the left sub, not posting notification")

        if not self.storage.is_sub_blacklisted(left_post.subreddit.display_name):
            right_to_left_notification_str = self.output.build_notification(
                new_post, right_post, left_post)
            try:
                print("Posting a notification to the right post")
                right_post.reply(right_to_left_notification_str)
            except Exception as ex:
                print("Couldnt post a comment to the to the right post")
                print(str(ex))
        else:
            print("We're blacklisted from the right sub, not posting notification")

    def get_valid_comments(self, comments):
        comments.replace_more(limit=0)
        return list(filter(lambda comment: not comment.stickied and comment.body != '[removed]' and comment.body != '[deleted]', list(comments)))