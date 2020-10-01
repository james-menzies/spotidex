from typing import Callable, Any

import urwid

from spotidex.viewmodels.play_info_vm import PlayInfoVM
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
        self.callbacks[key] = self.callbacks[key.upper()] = lambda: btn.keypress((15,), 'enter')


class PlayInfo:
    
    def __init__(self):
        
        self.vm: PlayInfoVM = PlayInfoVM()
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
        self.__write_pipe = TerminalWrapper.get_pipe(self.__update_views)
        
        TerminalWrapper.run_task(self.vm.refresh_loop, self.__write_pipe)
    
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
        
        back = self.__create_button("Go back", self.go_back, key='b')
        back_padding: urwid.Padding = urwid.Padding(back, align='left', left=2)
        title: urwid.Text = urwid.Text("Spotidex", align='center')
        title_padding = urwid.LineBox(urwid.BoxAdapter(urwid.Filler(title), 3))
        self.__add_to_top_container(urwid.GridFlow([back_padding, title_padding], 25, 1, 1, 'center'))
    
    def __init__subview_selection(self):
        buttons = []
        for index, view in enumerate(self.sub_views):
            buttons.append(self.__create_button(view.title, self.__change_sub_view, user_data=index))
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
    
    def __change_sub_view(self, button: urwid.Button, index: int) -> None:
        self.sub_view_frame.contents['body'] = (self.sub_views[index].widget, None)
        self.current_sub_view = index
    
    def __update_views(self, data):
        """
        Refresh method that gets called when self.__write_pipe is written to by the VM.
        VM will expose a dictionary object to enable the subviews to update. If no update
        is required the vm's current_song_data will be None.
        """
        
        if self.vm.current_song_data:
            self.main_view_frame.contents["body"] = (
                self.main_view.update_widget(self.vm.current_song_data), None)
            for view in self.sub_views:
                view.update_widget(self.vm.current_song_data)
            
            self.sub_view_frame.contents["body"] = (
                self.sub_views[self.current_sub_view].widget, None)
        
        if self.vm.automatic_refresh and self.vm.current_song_data:
            TerminalWrapper.flash_message(data)
        else:
            TerminalWrapper.flash_message(data, clear=False)
    
    @property
    def widget(self):
        return self.__widget
    
    def refresh_views(self, button):
        TerminalWrapper.run_task(self.vm.refresh_data, self.__write_pipe)
    
    def go_back(self, button: urwid.Button) -> None:
        self.vm.kill_refresh()
        TerminalWrapper.remove_pipe(self.__write_pipe)
        TerminalWrapper.flash_message("")
        TerminalWrapper.change_screen(main_menu.MainMenu())
    
    def next(self, button) -> None:
        TerminalWrapper.run_task(self.vm.next, self.__write_pipe)
    
    def previous(self, button) -> None:
        TerminalWrapper.run_task(self.vm.previous, self.__write_pipe)
    
    def static(self, button) -> None:
        self.vm.automatic_refresh = not self.vm.automatic_refresh
        if self.vm.automatic_refresh:
            self.refresh_views(button)
        else:
            TerminalWrapper.flash_message("Static Mode", clear=False)
