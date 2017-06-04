from abc import ABC, abstractmethod

class BasePoster(ABC):

    @abstractmethod
    def submit_post(self, subreddit, left_post, right_post):
        pass