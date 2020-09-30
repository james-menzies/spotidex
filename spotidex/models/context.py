import abc
import threading
from typing import Optional, Dict

import requests
from .wikipediaScraper import WikipediaScraper


class Context:
    
    @abc.abstractmethod
    def fetch(self, data: dict) -> Optional[Dict[str, dict]]:
        """
        Subclasses of this class are designed to abstract a
        single piece of contextual information about a particular
        track.
        
        It will return a dict object containing a single key
        and a dict value. It is intended that the passed
        in value will be updated with the return value.
        """
        pass


class BasicInfo(Context):
    
    def fetch(self, data: dict) -> Optional[Dict[str, dict]]:
        if "raw_data" not in data:
            return
        
        raw_data = data["raw_data"]
        
        keys = {}
        final = {"basic_info": keys}
        try:
            keys["id"] = raw_data["item"]["id"]
            keys["track"] = raw_data["item"]["name"]
            keys["artists"] = [artist["name"] for artist in raw_data["item"]["artists"]]
            keys["album"] = raw_data["item"]["album"]["name"]
        except (KeyError, TypeError):
            # invalid data passed in
            return
        
        return final


class ComposerInfo(Context):
    _cache = {}
    
    def fetch(self, data: dict) -> Optional[Dict[str, dict]]:
        
        if "basic_info" not in data:
            return
        
        basic_info = data["basic_info"]
        try:
            composer = basic_info["artists"][0]
            if composer in self._cache:
                return {"composer_info": self._cache[composer]}
            
            composer_info = self.retrieve_composer_info(composer)
            self._cache[composer] = composer_info
            return {"composer_info": composer_info}
        except (KeyError, ValueError):
            # invalid data
            return
    
    @staticmethod
    def retrieve_composer_info(name: str) -> dict:
        url = f"https://api.openopus.org/composer/list/search/{name}.json"
        data = requests.get(url).json()
        if data["status"]["success"] == 'true':
            return data["composers"][0]
        else:
            return {}


class ClassicalInfo(Context):
    
    def fetch(self, data: dict) -> Optional[Dict[str, dict]]:
        required_keys = ["basic_info", "composer_info"]
        if [key for key in required_keys if key not in data]:
            return
        
        keys = {}
        final = {"classical_info": keys}
        
        basic_info = data["basic_info"]
        composer = basic_info["artists"][0]
        keys["composer"] = composer
        
        last_name = composer.split()[-1]
        track_tokens = basic_info["track"].split(':')
        
        if len(track_tokens) > 1 and last_name in track_tokens[0]:
            track_tokens.pop(0)
        
        if len(track_tokens) > 1:
            keys["movement"] = track_tokens[-1].strip()
            track_tokens.pop(-1)
        
        track = ":".join(track_tokens)
        if ',' in track:
            work_plus_opus = ":".join(track_tokens).split(',')
            final_token = work_plus_opus.pop(-1)
            if 'Act' in final_token:
                keys['act'] = final_token.strip()
                keys['opus'] = work_plus_opus.pop(-1).strip()
            else:
                keys['opus'] = final_token.strip()
            keys["work"] = work_plus_opus[0].strip()
        elif '/' in track:
            tokens = track.split('/')
            keys["work"] = tokens[0].strip()
            keys["act"] = tokens[-1].strip()
        else:
            keys["work"] = track.strip()
        
        return final


class RecommendedInfo(Context):
    
    def fetch(self, data: dict) -> Optional[Dict[str, dict]]:
        keys = {}
        final = {"recommended_info": keys}
        
        composer_id = data["composer_info"]["id"]
        params = {
            "composer": {composer_id}
        }
        results = requests.get(f"https://api.openopus.org/dyn/work/random", params=params).json()
        keys["works"] = [work["title"] for work in results["works"]][:10]
        
        return final


class WikiInfo(Context):
    _cache = {}
    _lock = threading.Lock()
    
    def fetch(self, data: dict) -> Optional[Dict[str, dict]]:
        
        try:
            query = self.determine_query(data)
        except KeyError:
            return None
        
        keys = {}
        final = {
            self.name: keys,
        }
        
        # given that this cache is accessed asynchronously, it's important to lock it.
        self._lock.acquire()
        if query in self._cache:
            keys["content"] = self._cache[query]
        else:
            self._cache[query] = keys["content"] = WikipediaScraper(query).get_sanitized_wiki()
        self._lock.release()
        
        return final
    
    @abc.abstractmethod
    def determine_query(self, data: dict) -> str:
        pass
    
    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass


class ComposerWikiInfo(WikiInfo):
    
    def determine_query(self, data: dict) -> str:
        return data["classical_info"]["composer"]
    
    @property
    def name(self) -> str:
        return "composer_wiki_info"


class WorkWikiInfo(WikiInfo):
    
    def determine_query(self, data: dict) -> str:
        composer = data["classical_info"]["composer"]
        work = data["classical_info"]["work"]
        return f"{composer} {work}"
    
    @property
    def name(self) -> str:
        return "work_wiki_info"
