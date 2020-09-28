from typing import List, Optional, Dict

import urwid
from abc import abstractmethod


def generate_column_view(*columns: List[str]) -> urwid.Widget:
    col_body = []
    
    for column in columns:
        body = [urwid.Text(item, wrap='ellipsis') for item in column]
        walker = urwid.SimpleListWalker(body)
        col_body.append(urwid.ListBox(walker))
    
    return urwid.Columns(col_body)


class BaseSubView:
    
    def __init__(self, title: str = "Generic View", placeholder: str = "No information avaliable"):
        self._placeholder = urwid.Filler(urwid.Text(placeholder))
        self.__title = title
    
    @property
    def title(self) -> str:
        return self.__title
    
    @abstractmethod
    def update_widget(self, data: Optional[dict] = None) -> urwid.Widget:
        """
        This method will be called by the parent view when a new view
        is required. It must handle Nonetypes and check for valid keys.
        """
        pass
    
    @property
    @abstractmethod
    def widget(self):
        pass
    
    @staticmethod
    def _get_data_section(data: Optional[Dict], key: str, req_attrs: Optional[List] =None) -> Optional[Dict]:
        """
        Convenience method for getting the correct section of data passed in
        to update method. Will validate return None if either the section of
        data is missing, or one of the required attributes within that
        section is also missing.
        """
        if req_attrs is None:
            req_attrs = []
        if not data:
            return None
        # check for required section
        elif key not in data:
            return None
        # check for missing attributes in section
        elif [sub_key for sub_key in req_attrs if sub_key not in data[key]]:
            return None
        else:
            return data[key]


class ClassicalInfoSubView(BaseSubView):
    

    def __init__(self):
        super().__init__(title="Classical Info")
        self.__widget = self._placeholder
    
    
    
    def update_widget(self, data: Optional[dict] = None) -> urwid.Widget:
        
        data = self._get_data_section(data, "classical_info", ["work", "composer"])
        if not data:
            return self._placeholder
        
        column1 = []
        column2 = []
        
        if "movement" in data:
            string = data["movement"]
            if "act" in data:
                string += f" ({data['act']})"
            column1.append("Movement:")
            column2.append(string)
        
        string = data["work"]
        if "opus" in data:
            string += f" {data['opus']}"
        column1 += ["Work:", "Composer:"]
        column2 += [string, data["composer"]]
        
        self.__widget = generate_column_view(column1, column2)
        return self.__widget


class RawInfoSubView(BaseSubView):
    
    def __init__(self):
        super().__init__(title="Raw Spotify Info")
        self.__widget = self._placeholder

    @property
    def widget(self):
        return self.__widget

    def update_widget(self, data: Optional[dict] = None) -> urwid.Widget:
        
        data = self._get_data_section(data, "basic_info", ["track", "artists", "album"])
        if not data:
            return self._placeholder
        
        column1 = ["Track:", "Album:", "Artist(s):"]
        column2 = [data["track"], data["album"], *data["artists"]]
        self.__widget = generate_column_view(column1, column2)
        return self.__widget
