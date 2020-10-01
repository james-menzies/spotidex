import urwid
from typing import List, Callable


class Choice:
    
    def __init__(self, label: str, callback: Callable, description: str = ""):
        self.label = label
        self.callback = callback
        self.description = description


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
            button = urwid.Button(choice.label)
            urwid.connect_signal(button, 'click', choice.callback)
            button = urwid.AttrMap(urwid.LineBox(button), 'button')
            block.append(button)
        
        pile = urwid.Pile(block)
        
        self.__body.append(urwid.Padding(pile, align="center", width=20))
    
    def build(self) -> urwid.Widget:
        
        return urwid.Filler(urwid.Pile(self.__body))
