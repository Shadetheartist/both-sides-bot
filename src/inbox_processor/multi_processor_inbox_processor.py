from abc import ABC, abstractmethod
from src.inbox_processor.base_inbox_processor import BaseInboxProcessor
from typing import List

class MultiProcessorInboxProcessor(BaseInboxProcessor):

    def __init__(self, processors: List[BaseInboxProcessor]):
        self.processors = processors
        pass

    def process_inbox(self):
        print('Running multiple inbox processors...')
        for processor in self.processors:
            processor.process_inbox()
            pass