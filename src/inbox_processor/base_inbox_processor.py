from abc import ABC, abstractmethod


class BaseInboxProcessor(ABC):

    @abstractmethod
    def process_inbox(self):
        pass
