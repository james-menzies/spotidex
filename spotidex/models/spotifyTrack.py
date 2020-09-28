from typing import List

from .context import *


class SpotifyTrack:
    
    def __init__(self, raw_data: str, contexts: List):
        self.__information = {
            "raw_data": raw_data
        }
        
        contexts = [BasicInfo, ComposerInfo, ClassicalInfo]
        
        for context in contexts:
            info = context.fetch(self.__information)
            if info:
                self.__information.update(info)
    
    @property
    def information(self):
        return self.__information
