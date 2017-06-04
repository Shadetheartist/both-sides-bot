from abc import ABC, abstractmethod


class BaseOutput(ABC):

    def build_post(self, left_post, right_post):
        print("Building new post...")
        print("    Left: [", left_post.id, "] : ", left_post.title)
        print("    Right: [", right_post.id, "] : ", right_post.title)

        post_title = self.build_post_title(left_post, right_post)
        post_body = self.build_post_body(left_post, right_post)
        return (post_title, post_body)

    @abstractmethod
    def build_post_title(self, left_post, right_post):
        pass

    @abstractmethod
    def build_post_body(self, left_post, right_post):
        pass
    
    @abstractmethod
    def build_reply(self, index, left_comment, right_comment):
        pass

    @abstractmethod
    def build_notification(self, center_post, home_post, away_post):
        pass
