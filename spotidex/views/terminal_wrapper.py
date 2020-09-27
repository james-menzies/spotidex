import os
import time
from typing import Protocol, Callable
from threading import Thread, RLock
import urwid

current_threads = {}
thread_lock = RLock()


def _clean_subroutine(*args):
    loop, *rest = args
    while True:
        time.sleep(60)
        thread_lock.acquire()
        old_threads = []
        for thread, fd in current_threads.items():
            
            if not thread.isAlive():
                try:
                    loop.remove_watch_pipe(fd)
                    os.close(fd)
                except:
                    pass
                
                old_threads.append(thread)
        
        for thread in old_threads:
            current_threads.pop(thread, None)
        
        thread_lock.release()


class View(Protocol):
    
    def widget(self) -> urwid.Widget:
        ...


class TerminalWrapper:
    __palette = {
        ('bg', 'dark green', 'black',),
        ('reversed', 'black', 'white',),
    }
    __placeholder = urwid.SolidFill()
    __title = urwid.Text("Spotidex v1.0", align='left')
    __frame = urwid.Frame(__placeholder, header=__title)
    
    __loop = urwid.MainLoop(__frame, palette=__palette)
    
    clean_thread = Thread(target=_clean_subroutine, args=(__loop,))
    clean_thread.setDaemon(True)
    clean_thread.start()
    
    @classmethod
    def start_application(cls, initial_screen: View) -> None:
        cls.__loop.widget = urwid.AttrMap(initial_screen.widget, 'bg')
        cls.__loop.run()
    
    @classmethod
    def change_screen(cls, view: View):
        cls.__loop.widget = urwid.AttrMap(view.widget, 'bg')
    
    @staticmethod
    def exit(button):
        raise urwid.ExitMainLoop()
    
    @classmethod
    def run_task(cls, task: Callable, update: Callable):
        thread_lock.acquire()
        write_func = lambda x: os.write(fd, str.encode(str(x)))
        fd = cls.__loop.watch_pipe(update)
        thread = Thread(target=task, args=(write_func,))
        thread.setDaemon(True)
        current_threads[thread] = fd
        thread.start()
        thread_lock.release()
