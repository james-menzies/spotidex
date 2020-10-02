import os
from typing import Protocol, Callable, Any, List, Tuple, Optional
from threading import Thread, RLock
import urwid


class View(Protocol):
    
    def widget(self) -> urwid.Widget:
        ...


class TerminalWrapper:
    __palette: List[Tuple[str]] = [
        ('bg', 'dark green', 'black',),
        ('reversed', 'black', 'white',),
        ('border', 'light magenta', 'black', ),
        ('button', 'white', 'dark magenta', ),
        ('title', 'light gray,bold,underline', 'black'),
        ('standout', 'light gray,bold', 'black')
    ]
    __background = urwid.SolidFill('*')
    __placeholder = urwid.WidgetPlaceholder(urwid.SolidFill())
    __status = urwid.Text(" ", align='left')
    __footer = urwid.Text(" ", align='center')
    __frame = urwid.Frame(urwid.AttrMap(__placeholder, 'bg'), footer=urwid.AttrMap(__footer, 'standout'))
    __linebox = urwid.LineBox(__frame, tlcorner= u'\u2554',
                              trcorner=u'\u2557', blcorner=u'\u255A',
                              brcorner=u'\u255D')
    __overlay = urwid.Overlay(__linebox, urwid.AttrMap(__background, 'bg'),
                              align='center', width=('relative', 85),
                              valign='middle', height=('relative', 90),
                              )
    __open_pipes: List[int] = []
    
    __loop = urwid.MainLoop(urwid.AttrMap(__overlay, 'border'), palette=__palette)

    @classmethod
    def start_application(cls, initial_screen: View) -> None:
        cls.__placeholder.original_widget = initial_screen.widget
        cls.__loop.run()
    
    @classmethod
    def change_screen(cls, view: View) -> None:
        cls.__placeholder.original_widget = view.widget
    
    @classmethod
    def exit(cls, button: Optional[urwid.Button] = None) -> None:
        cls.clean_resources()
        raise urwid.ExitMainLoop()
    
    @classmethod
    def clean_resources(cls):
        for pipe in cls.__open_pipes:
            cls.remove_pipe(pipe)
    
    @classmethod
    def run_task(cls, task: Callable, fd: int) -> None:
        
        def write_func(data: str) -> None:
            try:
                os.write(fd, str.encode(str(data)))
            except OSError:
                # Pipe has already been closed.
                pass
        
        thread = Thread(target=task, args=(write_func,))
        thread.setDaemon(True)
        
        thread.start()
    
    @classmethod
    def get_pipe(cls, update: Callable) -> int:
        fd = cls.__loop.watch_pipe(update)
        cls.__open_pipes.append(fd)
        return fd

    
    @classmethod
    def remove_pipe(cls, fd: int) -> str:
    
        status = f"watch pipe removed: {cls.__loop.remove_watch_pipe(fd)}"
        os.close(fd)
        cls.__open_pipes.remove(fd)

        return status
    
    @classmethod
    def clear_status(cls, arg1: Any = None, arg2: Any = None):
        # extra args required for set alarm callback.
        cls.__footer.set_text(" ")
    
    @classmethod
    def flash_message(cls, message: str, clear: bool = True, duration: float = 0.5):
        """
        Flashes a message in the main widgets status footer. If clear is false,
        the status must be cleared manually. This method is thread safe.
        """
        cls.__footer.set_text(message)
        if clear:
            cls.__loop.set_alarm_in(duration, cls.clear_status)
