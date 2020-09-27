import urwid

from spotidex.viewmodels.entry_vm import EntryVM
from .scroll import Scrollable
from .subviews import *
from . import main_menu
from .terminal_wrapper import TerminalWrapper


class EntryPile(urwid.Pile):
    
    def __init__(self, widget_list, refresh_func):
        super().__init__(widget_list)
        self.refresh_func = refresh_func
    
    def keypress(self, size, key):
        key = super().keypress(size, key)
        if key == 'q':
            TerminalWrapper.change_screen(main_menu.MainMenu())
        elif key == 'r':
            self.refresh_func()
        else:
            return key


class Entry:
    
    def __init__(self):
        self.vm = EntryVM()
        self.main_view = self.vm.main_view
        self.sub_views = self.vm.sub_views
    
    def update_views(self, data):
        new_data = self.vm.last_refresh_request
        self.main_view_frame.contents["body"] = (self.main_view.update_widget(new_data), None)
    
    def refresh_views(self):
        TerminalWrapper.run_task(self.vm.refresh_data, self.update_views)
    
    @property
    def widget(self) -> urwid.Widget:
        def callback(button: urwid.Button, index: int) -> None:
            subview_frame.contents['body'] = (self.sub_views[index].widget, None)
        
        buttons = []
        for index, view in enumerate(self.sub_views):
            buttons.append(urwid.LineBox(urwid.Button(view.title, callback, index)))
        
        walker = urwid.SimpleFocusListWalker(buttons)
        grid_flow = urwid.GridFlow(walker, cell_width=25, h_sep=1, v_sep=1, align='center')
        
        subview_frame = urwid.Frame(self.sub_views[0].widget)
        subview_display = urwid.LineBox(subview_frame, title="More info")
        subview_display = urwid.BoxAdapter(subview_display, 25)
        self.main_view_frame = urwid.Frame(self.main_view.widget)
        main_view_display = urwid.BoxAdapter(self.main_view_frame, 7)
        pile = EntryPile([main_view_display, grid_flow, subview_display], self.refresh_views)
        return urwid.Filler(pile)
