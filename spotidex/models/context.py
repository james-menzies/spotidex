import abc

import requests


class Context:
    
    @classmethod
    @abc.abstractmethod
    def fetch(cls, data: dict) -> True:
        pass


class BasicInfo:
    @classmethod
    def fetch(cls, data: dict):
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


class ComposerInfo:

    _cache = {}

    @classmethod
    def fetch(cls, data: dict):
        basic_info = data["basic_info"]
        if not basic_info:
            return
        
        composer = basic_info["artists"][0]
        if composer in cls._cache:
            return {"composer_info": cls._cache[composer]}

        composer_info = cls.retrieve_composer_info(composer)
        cls._cache[composer] = composer_info
        return {"composer_info": composer_info}
    
    @classmethod
    def retrieve_composer_info(cls, name: str) -> dict:
        url = f"https://api.openopus.org/composer/list/search/{name}.json"
        data = requests.get(url).json()
        if data["status"]["success"] == 'true':
            return data["composers"][0]
        else:
            return {}


class ClassicalInfo:
    
    @classmethod
    def fetch(cls, data: dict):
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
