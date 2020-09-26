import abc
import json
from typing import Tuple
import requests


class Context:
    
    @classmethod
    @abc.abstractmethod
    def fetch(cls, data: dict) -> True:
        pass


class BasicInfo(Context):
    @classmethod
    def fetch(cls, data: dict):
        raw_data = data["raw_data"]
        keys = {}
        final = {"basic_info": keys}
        keys["id"] = raw_data["item"]["id"]
        keys["track"] = raw_data["item"]["name"]
        keys["artists"] = [artist["name"] for artist in raw_data["item"]["artists"]]
        keys["album"] = raw_data["item"]["album"]["name"]
        
        return final


class ClassicalInfo(Context):
    
    @classmethod
    def fetch(cls, data: dict):
        basic_info = data["basic_info"]
        keys = {}
        final = {"classical_info": keys}
        composer = basic_info["artists"][0]
        composer_info = cls.retrieve_composer_info(composer)
        
        if not composer_info:
            return final
        
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

    @classmethod
    def retrieve_composer_info(cls, name: str) -> dict:
        url = f"https://api.openopus.org/composer/list/search/{name}.json"
        data = requests.get(url).json()
        if data["status"]["success"] == 'true':
            return data["composers"][0]
        else:
            return {}
