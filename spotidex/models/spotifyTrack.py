from typing import List, Optional

from .context import *


class SpotifyTrack:
    
    def __init__(self, raw_data: str, contexts: Optional[List[Context]] = None):
        
        if contexts is None:
            contexts = []
        if not raw_data:
            self.__information = None
            return
        else:
            self.__information = {
                "raw_data": raw_data
            }
        
        contexts = [BasicInfo, ComposerInfo, ClassicalInfo, RecommendedInfo, ComposerWikiInfo, WorkWikiInfo]
        
        for context in contexts:
            info = context().fetch(self.__information)
            if info:
                self.__information.update(info)
    
    def __eq__(self, other) -> bool:
        
        if not self.information or not other.information:
            return not self.information and not other.information
        
        return self.information["basic_info"]["id"] == other.information["basic_info"]["id"]
    
    @property
    def information(self) -> dict:
        return self.__information
