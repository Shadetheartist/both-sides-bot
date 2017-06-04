from abc import ABC, abstractmethod
from src.inbox_processor.base_inbox_processor import BaseInboxProcessor
from src.poster.base_poster import BasePoster
from src.storage.base_storage import BaseStorage

class UserBlacklistInboxProcessor(BaseInboxProcessor):

    def __init__(self, reddit, storage: BaseStorage):
        self.reddit = reddit
        self.storage = storage

    def process_inbox(self):
        print('Processing inbox for users to blacklist')
        for comment in self.reddit.inbox.unread():
            if 'blacklist me' in comment.body.lower():
                self.reply_to_blacklist(comment)

    def reply_to_blacklist(self, comment):

        user = comment.author.name
        self.storage.blacklist_user(user)
        comment.reply('It is done my lord. You have been blacklisted from /r/both_sides_bot username mentions.')
        comment_list = list()
        comment_list.append(comment)
        self.reddit.inbox.mark_read(comment_list)