from abc import ABC, abstractmethod
from src.storage.base_storage import BaseStorage
from src.output.standard_output import StandardOutput

class UnintrusiveStandardOutput(StandardOutput):

    def build_username(self, redditor):
        if redditor is None:
            return 'unknown'

        if self.storage.is_user_blacklisted(redditor.name):
            return '/-/' + redditor.name + ' : blacklisted'

        return '/-/' + redditor.name