from typing import List, Callable, Any

import urwid


class Choice:
    
    def __init__(self, label: str, callback: Callable, description: str = ""):
        self.label = label
        self.callback = callback
        self.description = description


class Button:
    
    def init(self, label, callback: Callable[[], Any], user_data: Any = None):
        self.__button = urwid.Button(label, on_press=callback, user_data=user_data)
        div = urwid.Divider()
        pile = urwid.Pile([div, self.__button, div], focus_item=self.__button)
        self.__decorated_button = urwid.AttrMap(pile, 'button', focus_map='reversed')
    
    @property
    def decorated_button(self) -> urwid.AttrMap:
        return self.__decorated_button
    
    @property
    def button(self) -> urwid.Button:
        return self.__button


class Menu:
    
    def __init__(self):
        font = urwid.font.HalfBlock5x4Font()
        txt = urwid.BigText("Spotidex", font)
        txt = urwid.Padding(txt, "center", width="clip")
        version = urwid.Text("v 1.0", align='center')
        div = urwid.Divider(top=4)
        self.__body = [txt, version, div]
    
    def add_choice_block(self, choices: List[Choice], description: str = "") -> None:
        
        block = []
        if description:
            block.append(urwid.Text(description))
            block.append(urwid.Divider())
        
        for choice in choices:
            block.append(button(choice.label, choice.callback))
            block.append(urwid.Divider())
        
        pile = urwid.Pile(block)
        
        self.__body.append(urwid.Padding(pile, align="center", width=20))
    
    def build(self) -> urwid.Widget:
        
        return urwid.Filler(urwid.Pile(self.__body))
