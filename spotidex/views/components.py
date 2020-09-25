import urwid
from typing import Dict, Callable


class Menu:
    
    def __init__(self, title: str = ""):
        
        self.__body = []
        self.div = urwid.Divider()
        
        if title:
            self.__title = urwid.Text(title)
            self.__body.extend([self.__title, self.div])
    
    def add_text(self, txt: urwid.Text, div: bool = True) -> None:
        self.__body.append(txt)
        if div:
            self.__body.append(self.div)
    
    def add_choice_block(self, choices: Dict[str, Callable]) -> None:
        
        for choice in choices:
            button = urwid.Button(choice)
            urwid.connect_signal(button, 'click', choices[choice])
            self.__body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    
    def build(self) -> urwid.Padding:
        
        menu = urwid.ListBox(urwid.SimpleFocusListWalker(self.__body))
        return urwid.Padding(menu, left=20, right=20, align='center')
