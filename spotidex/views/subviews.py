from typing import List, Optional

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
    def update_widget(self, data: Optional[dict]) -> urwid.Widget:
        """
        This method will be called by the parent view when a new view
        is required. It must handle Nonetypes and check for valid keys.
        """
        pass
    
    @staticmethod
    def _get_data_section(data: Optional[dict], key: str, req_attrs: List[str] = []) -> Optional[dict]:
        """
        Convenience method for getting the correct section of data passed in
        to update method. Will validate return None if either the section of
        data is missing, or one of the required attributes within that
        section is also missing.
        """
        if not data:
            return None
        # check for required section
        elif key not in data:
            return None
        # check for missing attributes in section
        elif [key for key in req_attrs if key not in data]:
            return None
        else:
            return data[key]


class ClassicalInfoSubView(BaseSubView):
    
    def __init__(self):
        super().__init__(title="Classical Info")
    
    def update_widget(self, data) -> urwid.Widget:
        
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
        
        return generate_column_view(column1, column2)


class RawInfoSubView(BaseSubView):
    
    def __init__(self):
        super().__init__(title="Raw Spotify Info")
    
    def update_widget(self, data: Optional[dict]) -> urwid.Widget:
        
        data = self._get_data_section(data, "basic_info", ["track", "artist", ""])
        if not data:
            return self._placeholder
        
        column1 = ["Track:", "Album:", "Artist(s):"]
        column2 = [data["track"], data["album"], *data["artists"]]
        return generate_column_view(column1, column2)
