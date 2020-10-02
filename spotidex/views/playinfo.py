from typing import Callable, Any

from spotidex.viewmodels.play_info_vm import PlayInfoVM
from . import components
from . import main_menu
from .subviews import *
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
        div = urwid.Divider()
        
        self.top_container = EntryPile([])
        self.__widget = urwid.Filler(urwid.Padding(self.top_container, left=1, right=1))
        self.__init__header()
        self.__add_to_top_container(div)
        
        self.main_view_frame: urwid.Frame = urwid.Frame(self.main_view.widget)
        self.__add_subview_frame(self.main_view_frame, 10, "Track Information")
        self.__add_to_top_container(div)
        
        self.__init__subview_selection()
        self.__add_to_top_container(div)
        
        self.sub_view_frame: urwid.Frame = urwid.Frame(self.sub_views[0].widget)
        self.__add_subview_frame(self.sub_view_frame, 20, "More Information")
        self.__add_to_top_container(div)
        
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
                        key: Optional[str] = None, user_data: Any = None) -> urwid.AttrMap:
        button: components.Button = components.Button(label.upper(), function, user_data)
        
        if key:
            self.top_container.register_button(button.button, key)
        return button.decorated_button
    
    def __init__header(self) -> None:
        
        back = self.__create_button("back", self.go_back, key='b')
        back_padding: urwid.Padding = urwid.Padding(back, align='left', left=2)
        # title: urwid.Text = urwid.Text("Spotidex", align='center')
        # title_padding = urwid.LineBox(urwid.BoxAdapter(urwid.Filler(title), 3))

        font = urwid.font.HalfBlock5x4Font()
        title = urwid.BigText("Spotidex", font)
        title_padding = urwid.Padding(title, "right", width="clip")
        header_widget = urwid.Columns([
            (15, back_padding),
            title_padding,
        ], dividechars=1)
        self.__add_to_top_container(header_widget)
    
    def __init__subview_selection(self) -> None:
        buttons = []
        for index, view in enumerate(self.sub_views):
            buttons.append(self.__create_button(view.title, self.__change_sub_view, user_data=index))
        walker = urwid.SimpleFocusListWalker(buttons)
        
        grid_flow = urwid.GridFlow(walker, cell_width=15, h_sep=1, v_sep=1, align='center')
        self.__add_to_top_container(grid_flow)
        self.top_container.focus_item = grid_flow
    
    def __init__button_bar(self) -> None:
        
        previous_btn = self.__create_button("Prev.", self.previous, key='p')
        next_btn = self.__create_button("Next", self.next, key="n")
        static_btn = self.__create_button("Stat.", self.static, key='s')
        refresh_btn = self.__create_button("Ref.", self.refresh_views, key='r')
        grid_flow = urwid.GridFlow([previous_btn, next_btn, static_btn, refresh_btn], 15, 1, 1, 'center')
        self.__add_to_top_container(grid_flow)
    
    def __change_sub_view(self, button: urwid.Button, index: int) -> None:
        self.sub_view_frame.contents['body'] = (self.sub_views[index].widget, None)
        self.current_sub_view = index
    
    def __update_views(self, data) -> None:
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
    def widget(self) -> urwid.Widget:
        return self.__widget
    
    def refresh_views(self, button) -> None:
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
