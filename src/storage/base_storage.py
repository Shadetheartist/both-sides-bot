from abc import ABC, abstractmethod


class BaseStorage(ABC):

    @abstractmethod
    def get_subs_to_compare(self):
        pass

    @abstractmethod
    def add_post_to_history(self, post):
        pass

    @abstractmethod
    def get_post_history(self):
        pass

    @abstractmethod
    def is_in_history(self):
        pass

    @abstractmethod
    def posts_have_been_compared(self, left_post, right_post):
        pass

    @abstractmethod
    def get_blacklisted_subs(self):
        pass

    @abstractmethod
    def blacklist_sub(self, sub_name):
        pass

    @abstractmethod
    def is_sub_blacklisted(self, sub_name):
        pass

    @abstractmethod
    def get_blacklisted_users(self):
        pass

    @abstractmethod
    def blacklist_user(self, user_name):
        pass

    @abstractmethod
    def is_user_blacklisted(self, user_name):
        pass
