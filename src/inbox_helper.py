import praw
from storage_helper import StorageHelper
from sub_comparor import SubComparor

class InboxHelper(object):
    def __init__(self):
        self.reddit = praw.Reddit('comparatorbot')

    def check_inbox(self):
        self.check_for_comapare_request()
        self.check_for_blacklist_request()
        return

    def check_for_blacklist_request(self):
        for comment in self.reddit.inbox.unread():
            if 'blacklist me' in comment.body.lower():
                self.reply_to_blacklist(comment)

    def reply_to_blacklist(self, comment):

        user = comment.author.name
        StorageHelper.blacklist_user(user)
        comment.reply('It is done my lord. You have been blacklisted from /r/both_sides_bot username mentions.')
        comment_list = list()
        comment_list.append(comment)
        self.reddit.inbox.mark_read(comment_list)

    def check_for_comapare_request(self):
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
                        #todo: urls here
                        left_post = praw.models.Submission(self.reddit, id=split_str[0])
                        right_post = praw.models.Submission(self.reddit, id=split_str[1])
                        new_post = SubComparor.submit_post(left_post, right_post, comment)
                        self.reply_to_compare(comment, new_post, left_post, right_post)



    def reply_to_compare(self, comment, new_post, left_post=None, right_post=None):
        if StorageHelper.is_sub_blacklisted(comment.subreddit.sub_display_name):
            print("Tried to reply to mention, but we're blacklisted from the that sub.")
            return

        if new_post is not None:
            print("Replying to comment [", comment.id, "]")
            comment.reply("[Your wish has been granted, here is your link!]({0})".format(new_post.permalink))
        elif left_post is not None and right_post is not None:
            history_info = StorageHelper.get_post_info_from_left_right(left_post, right_post)
            center_post_id = history_info['center_post_id']
            center_post = praw.models.Submission(self.reddit, id=center_post_id)
            comment.reply("[Your wish could not be granted, a comparison has already been made.]({0})".format(center_post.permalink))
        else:
            comment.reply("(:0 ) i legit can't rn.".format())

        print("Marking comment read [", comment.id, "]")

        comment_list = list()
        comment_list.append(comment)

        self.reddit.inbox.mark_read(comment_list)




#