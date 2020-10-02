from abc import abstractmethod
from typing import List, Optional, Dict

import urwid

from .scroll import Scrollable


def generate_column_view(column1: List[str], column2: List[str]) -> urwid.Widget:
    """
    Utility method to help generate a two column view of keys and pairs.
    The Raw Info and Main View use this function to render their respective
    widgets.
    """
    col_body = []
    
    body1 = [('pack', urwid.Text(item, wrap='ellipsis')) for item in column1]
    body1 = urwid.AttrMap(urwid.Pile(body1), 'standout')
    col_body.append((16, body1))
    
    body2 = [('pack', urwid.Text(item, wrap='ellipsis')) for item in column2]
    body2 = urwid.AttrMap(urwid.Pile(body2), 'border')
    col_body.append(body2)
    
    return urwid.Filler(urwid.Padding(urwid.Columns(col_body), align='center', left=2, right=2))


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
        
        retrieved_data = self._get_data_section(data, "classical_info", ["work", "composer"])
        if not retrieved_data:
            self.__widget = RawInfoSubView().update_widget(data)
            return self.__widget
        
        data = retrieved_data
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
        super().__init__(title="Spotify")
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
        super().__init__(title="Suggested")
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
        title = urwid.Text(('title', f"Other Works by {data2['name']}"), align='center')
        labels = [urwid.Text(('border', str(work)), align='center') for work in works]
        pile = urwid.Pile([title, urwid.Divider(), *labels])
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
        
        if not data or not data["composer_info"]:
            self.__widget = self.placeholder
            return self.__widget
        
        data = self.get_wiki_contents(data)
        
        title = urwid.Text(("title", self.title), align='center')
        div = urwid.Divider()
        body = [div, title, div]
        
        for item in data:
            
            if item["type"] == 'heading':
                text = urwid.Text(("title", item["content"]), align="center")
                body += [text, div]
            else:
                text = urwid.Text(('border', item["content"]))
                body += [text, div]
        
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
        super().__init__("Composer")
    
    def get_introduction(self, data: Optional[Dict[str, Dict]]) -> Optional[urwid.Widget]:
        return None
    
    def get_wiki_contents(self, data: Optional[Dict[str, Dict]]) -> List[Dict[str, str]]:
        return data["composer_wiki_info"]["content"]


class WorkWikiSubView(WikiSubview):
    
    def __init__(self):
        super().__init__("Work")
    
    def get_introduction(self, data: Optional[Dict[str, Dict]]) -> Optional[urwid.Widget]:
        return None
    
    def get_wiki_contents(self, data: Optional[Dict[str, Dict]]) -> List[Dict[str, str]]:
        return data["work_wiki_info"]["content"]
