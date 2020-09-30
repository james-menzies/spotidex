import threading
from typing import List, Optional

from .context import *


class CountDownLatch(object):
    def __init__(self, count=1):
        self.count = count
        self.lock = threading.Condition()
    
    def count_down(self):
        self.lock.acquire()
        self.count -= 1
        if self.count <= 0:
            self.lock.notifyAll()
        self.lock.release()
    
    def wait_on(self):
        self.lock.acquire()
        while self.count > 0:
            self.lock.wait()
        self.lock.release()


class SpotifyTrack:
    
    def __init__(self, raw_data: str, contexts: Optional[List[Context]] = None):
        
        if not raw_data:
            self.__information = None
            return
        else:
            self.__information = {
                "raw_data": raw_data
            }
        
        basic_contexts = [BasicInfo, ComposerInfo, ClassicalInfo]
        dependency_contexts = [RecommendedInfo, ComposerWikiInfo, WorkWikiInfo]
        lock = threading.Lock()
        
        def get_context(context, latch: Optional[CountDownLatch] = None):
            info = context().fetch(self.__information)
            if info:
                lock.acquire()
                self.__information.update(info)
                lock.release()
            if latch:
                latch.count_down()
        
        for context in basic_contexts:
            get_context(context)
        
        latch = CountDownLatch(len(dependency_contexts))
        
        for context in dependency_contexts:
            thread = threading.Thread(target=get_context, args=(context, latch))
            thread.start()
        
        latch.wait_on()
    
    def __eq__(self, other) -> bool:
        
        if not self.information or not other.information:
            return not self.information and not other.information
        
        return self.information["basic_info"]["id"] == other.information["basic_info"]["id"]
    
    @property
    def information(self) -> dict:
        return self.__information
