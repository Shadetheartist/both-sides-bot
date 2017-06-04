import random
import datetime
import os

from abc import ABC, abstractmethod
from src.storage.base_storage import BaseStorage
from src.output.base_output import BaseOutput
from src.output.output_helper import OutputHelper
from string import Template


class StandardOutput(BaseOutput):

    def __init__(self, storage: BaseStorage):
        self.storage = storage
        self.postTemplate = self.get_template_content('post')
        self.commentTemplate = self.get_template_content('comment')

    def build_username(self, redditor):
        if redditor is None:
            return 'unknown'

        if self.storage.is_user_blacklisted(redditor.name):
            return '/-/' + redditor.name + ' : blacklisted'

        return '/u/' + redditor.name

    def build_post(self, left_post, right_post):
        print("Building new post...")
        print("    Left: [", left_post.id, "] : ", left_post.title)
        print("    Right: [", right_post.id, "] : ", right_post.title)

        post_title = self.build_post_title(left_post, right_post)
        post_body = self.build_post_body(left_post, right_post)
        return (post_title, post_body)

    def build_post_title(self, left_post, right_post):
        description_format = '{0}: "{1}"'

        description = ''

        if random.randint(0, 1):
            description = description_format.format(
                left_post.subreddit.display_name, left_post.title)
        else:
            description = description_format.format(
                right_post.subreddit.display_name, right_post.title)

        description_str = '{0} vs. {1} - - - {2} '.format(
            '/r/' + left_post.subreddit.display_name, '/r/' + right_post.subreddit.display_name, description)

        #reddit titles can only be 300 chars long
        if len(description_str) > 300:
            description_str = description_str[:300]

        return description_str

    def build_post_body(self, left_post, right_post):

        var_dict = dict(
            comparison_date=datetime.datetime.now().strftime("%Y-%m-%d @ %H:%M"),
            topic_of_comparison_link=left_post.url,
            left_subreddit=left_post.subreddit._path,
            left_subreddit_post_title=left_post.title,
            left_subreddit_post_link=left_post.permalink,
            right_subreddit=right_post.subreddit._path,
            right_subreddit_post_title=right_post.title,
            right_subreddit_post_link=right_post.permalink,
        )

        return self.build_template(self.postTemplate, var_dict)

    def get_score_string(self, comment):
        if comment.score_hidden:
            return '[score hidden]'
        return str(comment.score) + ' points'

    def build_reply(self, index, left_comment, right_comment):

        print("Building reply #", index)

        var_dict = dict(
            nth=OutputHelper.get_nth(index),
            left_subreddit=left_comment.subreddit.display_name,
            left_comment_context=left_comment.permalink(),
            left_comment_points=self.get_score_string(left_comment),
            left_comment=OutputHelper.quotify(left_comment.body),
            left_user=self.build_username(left_comment.author),
            right_subreddit=right_comment.subreddit.display_name,
            right_comment_context=right_comment.permalink(),
            right_comment_points=self.get_score_string(right_comment),
            right_comment=OutputHelper.quotify(right_comment.body),
            right_user=self.build_username(right_comment.author),
        )

        return self.build_template(self.commentTemplate, var_dict)

    def build_notification(self, center_post, home_post, away_post):
        notification_format = 'Huh, it looks like some people over at {0} have some thoughts on the exact same article ^(or whatever) [Check out what the *other side* has to say]({1})'
        notification_str = notification_format.format(
            away_post.subreddit._path,
            center_post.permalink
        )

        return notification_str

    def build_template(self, raw_template, var_dict):
        template_str = Template(raw_template)
        compiled_template_str = template_str.substitute(var_dict)
        return compiled_template_str

    def get_template_content(self, template_name):
        template_file_path = os.path.join(
            os.path.dirname(__file__),
            'templates/{0}.tpl'.format(template_name)
        )
        template_file = open(template_file_path)
        return template_file.read()