import os
from typing import Protocol, Callable
from threading import Thread
import urwid


class View(Protocol):
    
    @property
    def widget(self) -> urwid.Widget:
        return urwid.SolidFill()


class TerminalWrapper:
    __palette = {
        ('bg', 'dark green', 'black',),
        ('reversed', 'black', 'white',),
    }
    __placeholder = urwid.SolidFill()
    __title = urwid.Text("Spotidex v1.0", align='left')
    __frame = urwid.Frame(__placeholder, header=__title)
    
    __loop = urwid.MainLoop(__frame, palette=__palette)
    
    @classmethod
    def start_application(cls, initial_screen: View) -> None:
        cls.__loop.widget = urwid.AttrMap(initial_screen.widget, 'bg')
        cls.__loop.run()
    
    @classmethod
    def change_screen(cls, view: View):
        cls.__loop.widget = urwid.AttrMap(view.widget, 'bg')
    
    @staticmethod
    def exit():
        raise urwid.ExitMainLoop()
    
    @classmethod
    def run_task(cls, task: Callable, update: Callable):
        fd = cls.__loop.watch_pipe(update)
        write_func = lambda x: os.write(fd, str.encode(str(x)))
        close_func = lambda: cls.__loop.remove_watch_pipe(fd)
        thread = Thread(target=task, args=(write_func, close_func))
        thread.setDaemon(True)
        thread.start()
