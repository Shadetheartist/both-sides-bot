from abc import ABC, abstractmethod
from src.inbox_processor.base_inbox_processor import BaseInboxProcessor
from src.poster.base_poster import BasePoster
from src.storage.base_storage import BaseStorage
from pprint import pprint


class UserBlacklistInboxProcessor(BaseInboxProcessor):

    def __init__(self, reddit, storage: BaseStorage):
        self.reddit = reddit
        self.storage = storage

    def process_inbox(self):
        print('Processing inbox for users to blacklist')
        for comment in self.reddit.inbox.unread():
            if 'blacklist me' in comment.body.lower():
                self.process_user_self_blacklist_request(comment)
            elif 'blacklist me' in comment.subject.lower():
                self.process_user_self_blacklist_request(comment)
            elif 'fucking blacklist' in comment.subject.lower():
                self.process_mod_bulk_blacklist_request(comment)
            elif 'fucking blacklist' in comment.subject.lower():
                self.process_mod_blacklist_request(comment)

    def process_user_self_blacklist_request(self, comment):
        user = comment.author.name
        self.storage.blacklist_user(user)
        comment.reply('It is done my lord. You have been blacklisted from /r/both_sides_bot username mentions.')
        self.reddit.inbox.mark_read([comment])

    def validate_mod_blacklist(self, comment):
        if comment.author.name == 'both_sides_blacklist':
            return True

        if comment.author.name == 'both_sides_bot':
            return True

    def process_mod_blacklist_request(self, comment):
        self.validate_mod_blacklist(comment)

        blacklist_list_str = comment.body.lower()
        blacklist_list_str_words = blacklist_list_str.split(' ')
        
        # fucking blacklist [2](username)
        user_to_blacklist = blacklist_list_str[2]

        #4 space prefix makes reddit format in monospace (like the robot i am >:I)
        comment.reply('    Motherfucker just GOT blacklisted my FRIEND. WOO.')

        self.reddit.inbox.mark_read([comment])
        
    def process_mod_bulk_blacklist_request(self, comment):
        self.validate_mod_blacklist(comment)

        blacklist_list_str = comment.body.lower()
        blacklist_list = blacklist_list_str.split(', ')

        for username in blacklist_list:
            self.storage.blacklist_user(username)
            comment.reply('Dem motherfuckers just got BLACK LISTED my DUDE.')
            self.reddit.inbox.mark_read([comment])
        