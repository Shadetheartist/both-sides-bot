from abc import ABC, abstractmethod


class BaseSubComparor(ABC):

    @abstractmethod
    def compare(self, left, right):
        pass
