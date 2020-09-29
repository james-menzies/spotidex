from typing import Callable, Any

import urwid

from spotidex.viewmodels.entry_vm import EntryVM
from .scroll import Scrollable
from .subviews import *
from . import main_menu
from .terminal_wrapper import TerminalWrapper


class EntryPile(urwid.Pile):
    
    def __init__(self, widget_list):
        super().__init__(widget_list)
        self.callbacks: Dict[str, Callable] = {}
    
    def keypress(self, size, key) -> None:
        key = super().keypress(size, key)
        if key in self.callbacks:
            self.callbacks[key]()
    
    def register_button(self, btn: urwid.Button, key: str) -> None:
        btn.set_label(f"{btn.label} ({key.upper()})")
        callback = lambda: btn.keypress((15,), 'enter')
        self.callbacks[key] = callback
        self.callbacks[key.upper()] = callback


class Entry:
    
    def __init__(self):
        self.vm: EntryVM = EntryVM()
        self.main_view: BaseSubView = self.vm.main_view
        self.sub_views: List[BaseSubView] = self.vm.sub_views
        self.current_sub_view: int = 0
        
        self.top_container = EntryPile([])
        self.__widget = urwid.Filler(urwid.Padding(self.top_container, left=1, right=1))
        self.__init__header()
        
        self.main_view_frame: urwid.Frame = urwid.Frame(self.main_view.widget)
        self.__add_subview_frame(self.main_view_frame, 10, "Track Information")
        
        self.__init__subview_selection()
        
        self.sub_view_frame: urwid.Frame = urwid.Frame(self.sub_views[0].widget)
        self.__add_subview_frame(self.sub_view_frame, 30, "More Information")
        
        self.__init__button_bar()
    
    def __add_to_top_container(self, widget: urwid.Widget) -> None:
        self.top_container.contents.append(
            (widget, ('pack', None))
        )
    
    def __add_subview_frame(self, frame: urwid.Frame, rows: int, title: str) -> None:
        line_box = urwid.LineBox(frame, title=title)
        adapter = urwid.BoxAdapter(line_box, rows)
        self.__add_to_top_container(adapter)
    
    def __create_button(self, label: str, function: Callable[[urwid.Button], None],
                        key: Optional[str] = None, user_data: Any = None) -> urwid.LineBox:
        button: urwid.Button = urwid.Button(label.upper(), function, user_data=user_data)
        
        if key:
            self.top_container.register_button(button, key)
        return urwid.LineBox(button)
    
    def __init__header(self):
        def go_back(button: urwid.Button) -> None:
            TerminalWrapper.change_screen(main_menu.MainMenu())
        
        back = self.__create_button("Go back", go_back, key='b')
        back_padding: urwid.Padding = urwid.Padding(back, align='left', left=2)
        title: urwid.Text = urwid.Text("Spotidex", align='center')
        title_padding = urwid.LineBox(urwid.BoxAdapter(urwid.Filler(title), 3))
        self.__add_to_top_container(urwid.GridFlow([back_padding, title_padding], 25, 1, 1, 'center'))
    
    def __init__subview_selection(self):
        buttons = []
        for index, view in enumerate(self.sub_views):
            buttons.append(self.__create_button(view.title, self.change_sub_view, user_data=index))
        walker = urwid.SimpleFocusListWalker(buttons)
        
        grid_flow = urwid.GridFlow(walker, cell_width=25, h_sep=1, v_sep=1, align='center')
        self.__add_to_top_container(grid_flow)
    
    def __init__button_bar(self):
        
        previous_btn = self.__create_button("Previous", self.previous, key='p')
        next_btn = self.__create_button("Next", self.next, key="n")
        static_btn = self.__create_button("Static", self.static, key='s')
        refresh_btn = self.__create_button("Refresh", self.refresh_views, key='r')
        grid_flow = urwid.GridFlow([previous_btn, next_btn, static_btn, refresh_btn], 20, 1, 1, 'center')
        self.__add_to_top_container(grid_flow)
        
    @property
    def widget(self):
        return self.__widget
    
    def update_views(self, data):
        
        if not self.vm.matching_song_data and self.vm.current_song_data:
            self.main_view_frame.contents["body"] = (
                self.main_view.update_widget(self.vm.current_song_data), None)
            for view in self.sub_views:
                view.update_widget(self.vm.current_song_data)
            
            self.sub_view_frame.contents["body"] = (
                self.sub_views[self.current_sub_view].widget, None)
        
        if self.vm.current_song_data:
            TerminalWrapper.flash_message(data)
        else:
            TerminalWrapper.flash_message(data, clear=False)
    
    def refresh_views(self, button):
        TerminalWrapper.run_task(self.vm.refresh_data, self.update_views)
    
    def change_sub_view(self, button: urwid.Button, index: int) -> None:
        self.sub_view_frame.contents['body'] = (self.sub_views[index].widget, None)
        self.current_sub_view = index
    
    
    def next(self, button) -> None:
        TerminalWrapper.flash_message("Called Next")
    
    def previous(self, button) -> None:
        TerminalWrapper.flash_message("Called previous")
    
    def static(self, button) -> None:
        TerminalWrapper.flash_message("Called static")
        