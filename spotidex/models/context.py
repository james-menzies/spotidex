import abc

import requests
from .wikipediaScraper import WikipediaScraper


class Context:
    
    @abc.abstractmethod
    def fetch(self, data: dict):
        pass


class BasicInfo(Context):
    
    def fetch(self, data: dict):
        raw_data = data["raw_data"]
        keys = {}
        final = {"basic_info": keys}
        
        if not data["raw_data"]:
            return final
        
        keys["id"] = raw_data["item"]["id"]
        keys["track"] = raw_data["item"]["name"]
        keys["artists"] = [artist["name"] for artist in raw_data["item"]["artists"]]
        keys["album"] = raw_data["item"]["album"]["name"]
        
        return final


class ComposerInfo(Context):
    _cache = {}
    
    def fetch(self, data: dict):
        basic_info = data["basic_info"]
        if not basic_info:
            return
        
        composer = basic_info["artists"][0]
        if composer in self._cache:
            return {"composer_info": self._cache[composer]}
        
        composer_info = self.retrieve_composer_info(composer)
        self._cache[composer] = composer_info
        return {"composer_info": composer_info}
    
    @staticmethod
    def retrieve_composer_info(name: str) -> dict:
        url = f"https://api.openopus.org/composer/list/search/{name}.json"
        data = requests.get(url).json()
        if data["status"]["success"] == 'true':
            return data["composers"][0]
        else:
            return {}


class ClassicalInfo(Context):
    
    def fetch(self, data: dict):
        if not data["basic_info"]:
            return
        
        keys = {}
        final = {"classical_info": keys}
        if not data["composer_info"]:
            return final
        
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
    
    def fetch(self, data: dict) -> True:
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
    
    def fetch(self, data: dict) -> True:
        query = self.determine_query(data)
        keys = {}
        final = {
            self.name: keys,
        }
        
        if not query or not data:
            return final
        
        keys["content"] = WikipediaScraper(query).get_sanitized_wiki()
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
