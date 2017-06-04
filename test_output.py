import praw
import os.path

from src.storage.file_storage import FileStorage
from src.poster.standard_poster import StandardPoster
from src.poster.test_poster import TestPoster
from src.output.unintrusive_standard_output import UnintrusiveStandardOutput
from src.sub_comparor.hot_post_sub_comparor import HotPostSubComparor
from src.both_sides_bot import BothSidesBot

reddit = praw.Reddit('bot')

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

#post_l = praw.models.Submission(reddit, id='6f51r2')
#post_r = praw.models.Submission(reddit, id='6f4neq')
#print(output.build_post_body(post_l, post_r))

comment_l = praw.models.Comment(reddit, id='did5pko')
comment_r = praw.models.Comment(reddit, id='difjxhd')
print(output.build_reply(0, comment_l, comment_r))
