from src.sub_comparor.base_sub_comparor import BaseSubComparor
from src.storage.base_storage import BaseStorage

class HotPostSubComparor(BaseSubComparor):
    def __init__(self, reddit, storage: BaseStorage, post_search_limit, num_comments_needed_to_care=5):
        self.reddit = reddit
        self.storage = storage
        self.post_search_limit = post_search_limit
        self.num_comments_needed_to_care = num_comments_needed_to_care

    def compare(self, left_sub_name, right_sub_name):

        left_sub = self.reddit.subreddit(left_sub_name)
        right_sub = self.reddit.subreddit(right_sub_name)

        left_hot_posts = list(left_sub.hot(limit=self.post_search_limit))
        right_hot_posts = list(right_sub.hot(limit=self.post_search_limit))

        comparablePosts = []

        for left_hot_post in left_hot_posts:
            for right_hot_post in right_hot_posts:
                if left_hot_post.url == right_hot_post.url:
                    if self.validate_comparison(left_hot_post, right_hot_post):
                        comparablePosts.append((left_hot_post, right_hot_post))

        return comparablePosts

    def validate_comparison(self, left_post, right_post):
        if self.storage.posts_have_been_compared(left_post, right_post):
            return False

        if self.check_enough_comments(left_post, right_post) == False:
            return False
        
        return True

    def check_enough_comments(self, left_post, right_post):
        left_comments = self.get_valid_comments(left_post.comments)
        right_comments = self.get_valid_comments(right_post.comments)
        return len(left_comments) > self.num_comments_needed_to_care and len(right_comments) > self.num_comments_needed_to_care

    def get_valid_comments(self, comments):
        comments.replace_more(limit=0)
        return list(filter(lambda comment: not comment.stickied and comment.body != '[removed]' and comment.body != '[deleted]', list(comments)))
