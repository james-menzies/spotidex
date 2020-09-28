import urwid

from spotidex.viewmodels.entry_vm import EntryVM
from .scroll import Scrollable
from .subviews import *
from . import main_menu
from .terminal_wrapper import TerminalWrapper


# class EntryPile(urwid.Pile):
#
#     def __init__(self, widget_list, refresh_func):
#         super().__init__(widget_list)
#         self.refresh_func = refresh_func
#
#     def keypress(self, size, key):
#         key = super().keypress(size, key)
#         if key == 'q':
#             TerminalWrapper.change_screen(main_menu.MainMenu())
#         elif key == 'r':
#             self.refresh_func()
#         else:
#             return key
#

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
        self.main_view_frame: urwid.Frame = urwid.Frame(urwid.SolidFill())
        self.sub_view_frame: urwid.Frame = urwid.Frame(urwid.SolidFill())
    
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
    
    def refresh_views(self):
        TerminalWrapper.run_task(self.vm.refresh_data, self.update_views)
    
    def change_sub_view(self, button: urwid.Button, index: int) -> None:
        self.sub_view_frame.contents['body'] = (self.sub_views[index].widget, None)
        self.current_sub_view = index
    
    @property
    def widget(self) -> urwid.Widget:
        
        buttons = []
        for index, view in enumerate(self.sub_views):
            buttons.append(urwid.LineBox(urwid.Button(view.title, self.change_sub_view, index)))
        
        walker = urwid.SimpleFocusListWalker(buttons)
        grid_flow = urwid.GridFlow(walker, cell_width=25, h_sep=1, v_sep=1, align='center')
        
        
        subview_display = urwid.LineBox(self.sub_view_frame, title="More info")
        subview_display = urwid.BoxAdapter(subview_display, 25)
        self.main_view_frame = urwid.Frame(self.main_view.widget)
        main_view_display = urwid.BoxAdapter(self.main_view_frame, 7)
        pile = EntryPile([main_view_display, grid_flow, subview_display], self.refresh_views)
        return urwid.Filler(pile)
