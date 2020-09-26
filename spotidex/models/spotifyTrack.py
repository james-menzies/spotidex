from typing import List

from .context import *


class SpotifyTrack:
    
    def __init__(self, raw_data: str, contexts: List):
        self.__information = {
            "raw_data": raw_data
        }
        
        self.__information.update(BasicInfo.fetch(self.__information))
        self.__information.update(ClassicalInfo.fetch(self.__information))
        
       
    
    @property
    def information(self):
        return self.__information
