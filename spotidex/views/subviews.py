from typing import List, Optional, Dict

import urwid
from abc import abstractmethod

from .scroll import Scrollable


def generate_column_view(*columns: List[str]) -> urwid.Widget:
    """
    Utility method to help generate a two column view of keys and pairs.
    The Raw Info and Main View use this function to render their respective
    widgets.
    """
    col_body = []
    
    for column in columns:
        body = [urwid.Text(item, wrap='ellipsis') for item in column]
        walker = urwid.SimpleListWalker(body)
        col_body.append(urwid.ListBox(walker))
    
    return urwid.Columns(col_body)


class BaseSubView:
    
    def __init__(self, title: str = "Generic View", placeholder: str = "No information available"):
        # the default for SubViews to use when data is invalid or does not
        # satisfy the required information.
        self.__placeholder = urwid.Filler(urwid.Text(placeholder, align='center'))
        self.__title = title
    
    @property
    def title(self) -> str:
        return self.__title
    
    @property
    def placeholder(self):
        return self.__placeholder
    
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
    def _get_data_section(data: Optional[Dict], key: str, req_attrs: Optional[List] = None) -> Optional[Dict]:
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
        self.__widget = self.placeholder
    
    @property
    def widget(self):
        return self.__widget
    
    def update_widget(self, data: Optional[dict] = None) -> urwid.Widget:
        
        data = self._get_data_section(data, "classical_info", ["work", "composer"])
        if not data:
            self.__widget = self.placeholder
            return self.__widget
        
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
        self.__widget = self.placeholder
    
    @property
    def widget(self):
        return self.__widget
    
    def update_widget(self, data: Optional[dict] = None) -> urwid.Widget:
        data = self._get_data_section(data, "basic_info", ["track", "artists", "album"])
        if not data:
            self.__widget = self.placeholder
            return self.__widget
        
        column1 = ["Track:", "Album:", "Artist(s):"]
        column2 = [data["track"], data["album"], *data["artists"]]
        self.__widget = generate_column_view(column1, column2)
        return self.__widget


class RecommendedSubView(BaseSubView):
    
    def __init__(self):
        super().__init__(title="Other Works")
        self.__widget = self.placeholder
    
    @property
    def widget(self):
        return self.__widget
    
    def update_widget(self, data: Optional[dict] = None) -> urwid.Widget:
        
        data1 = self._get_data_section(data, "recommended_info", ["works"])
        data2 = self._get_data_section(data, "composer_info", ["name"])
        if not data1 or not data2:
            self.__widget = self.placeholder
            return self.__widget
        
        works = data1["works"]
        if not isinstance(works, list):
            self.__widget = self.placeholder
            return self.__widget
        title = urwid.Text(f"Other Works by {data2['name']}", align='center')
        div = urwid.Divider(div_char='-', top=1, bottom=1)
        labels = [urwid.Text(str(work), align='center') for work in works]
        pile = urwid.Pile([title, div, *labels])
        self.__widget = urwid.Filler(pile)
        return self.__widget


class WikiSubview(BaseSubView):
    def __init__(self, title):
        super().__init__(title)
        self.__widget = self.placeholder
    
    @property
    def widget(self):
        return self.__widget
    
    def update_widget(self, data: Optional[Dict[str, Dict]] = None) -> urwid.Widget:
        
        data = self.get_wiki_contents(data)
        
        title = urwid.Text(self.title)
        div_title = urwid.Divider(div_char='-', top=1, bottom=1)
        div_paragraph = urwid.Divider()
        body = [title, div_title]
        
        for item in data:
            
            if item["type"] == 'heading':
                text = urwid.Text(item["content"])
                body += [div_title, text, div_title]
            else:
                text = urwid.Text(item["content"])
                body += [text, div_paragraph]
        
        pile = urwid.Pile(body)
        self.__widget = Scrollable(pile)
        return self.__widget
    
    @abstractmethod
    def get_introduction(self, data: Optional[Dict[str, Dict]]) -> Optional[urwid.Widget]:
        pass
    
    @abstractmethod
    def get_wiki_contents(self, data: Optional[Dict[str, Dict]]) -> List[Dict[str, str]]:
        pass


class ComposerWikiSubView(WikiSubview):
    
    def __init__(self):
        super().__init__("About the Composer")
    
    def get_introduction(self, data: Optional[Dict[str, Dict]]) -> Optional[urwid.Widget]:
        return None

    def get_wiki_contents(self, data: Optional[Dict[str, Dict]]) -> List[Dict[str, str]]:
        return data["composer_wiki_info"]["content"]


class WorkWikiSubView(WikiSubview):
    
    def __init__(self):
        super().__init__("About this Work")
    
    def get_introduction(self, data: Optional[Dict[str, Dict]]) -> Optional[urwid.Widget]:
        return None
    
    def get_wiki_contents(self, data: Optional[Dict[str, Dict]]) -> List[Dict[str, str]]:
        return data["work_wiki_info"]["content"]

