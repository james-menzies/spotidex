from typing import List, Optional

import urwid
from abc import abstractmethod


def generate_column_view(*columns: List[str]) -> urwid.Widget:
    col_body = []
    
    for column in columns:
        body = [urwid.Text(item) for item in column]
        walker = urwid.SimpleListWalker(body)
        col_body.append(urwid.ListBox(walker))
    
    return urwid.Columns(col_body)


class BaseSubView:
    

    
    def __init__(self, placeholder: str = "No information avaliable"):
        self.__placeholder = urwid.Filler(urwid.Text(placeholder))
        self.__widget = self.__placeholder
        self.__title = "Generic View"
    
    @property
    def widget(self) -> urwid.Widget:
        return self.__widget
    
    @property
    def title(self) -> str:
        return self.__title
    
    @abstractmethod
    def update_widget(self, data) -> None:
        pass


class ClassicalInfoSubView(BaseSubView):
    
    def __init__(self):
        super().__init__()
        self.__title = "Classical Info"
    
    def update_widget(self, data) -> None:
        info = data["classical_info"]
        
        if not info:
            self.__widget = self.__placeholder
        
        column1 = []
        column2 = []
        
        if info["movement"]:
            string = info["movement"]
            if info["act"]:
                string += f" ({info['act']})"
            column1.append("Movement:")
            column2.append(string)
        
        string = info["work"]
        if info["opus"]:
            string += f" {info['opus']}"
        column1.append("Work:")
        column2.append(string)
        
        column1.append("Composer:")
        column2.append(info["composer"])
        
        self.__widget = generate_column_view(column1, column2)
