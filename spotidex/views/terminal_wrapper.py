import os
import time
from typing import Protocol, Callable, Any
from threading import Thread, RLock
import urwid

current_threads = {}
thread_lock = RLock()


def _clean_subroutine(*args):
    """
    This process is cleans up any pipes that have been created by
    the program which were used by threads that are no longer alive.
    It uses the lock with the run task method in Terminal Wrapper,
    to avoid the race condition that occurs when a pipe is both created
    and destroyed with the sam identifier. It should only be run once.
    """
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
    __status = urwid.Text(" ", align='left')
    __footer = urwid.Text(" ", align='center')
    __frame = urwid.Frame(__placeholder, footer=__footer)
    
    __loop = urwid.MainLoop(urwid.AttrMap(__frame, 'bg', focus_map='reversed'), palette=__palette)
    
    clean_thread = Thread(target=_clean_subroutine, args=(__loop,))
    clean_thread.setDaemon(True)
    clean_thread.start()
    
    @classmethod
    def start_application(cls, initial_screen: View) -> None:
        cls.__frame.contents["body"] = (initial_screen.widget, None)
        cls.__loop.run()
    
    @classmethod
    def change_screen(cls, view: View) -> None:
        cls.__frame.contents["body"] = (view.widget, None)
    
    @staticmethod
    def exit(button) -> None:
        raise urwid.ExitMainLoop()
    
    @classmethod
    def run_task(cls, task: Callable, update: Callable) -> None:
        """
        This is the method that should be called to safely update the
        GUI from a background process. The task process should perform
        a calculation, and accept a write function as a single parameter.
        The task function should call the write function to communicate
        any status change and when the process is complete.
        
        The update function is the function that will be called whenever the
        task function calls the write function. There is no need to clean
        up the pipes, as it is taken care of by a background process.
        """
        thread_lock.acquire()
        write_func = lambda x: os.write(fd, str.encode(str(x)))
        fd = cls.__loop.watch_pipe(update)
        thread = Thread(target=task, args=(write_func,))
        thread.setDaemon(True)
        current_threads[thread] = fd
        thread.start()
        thread_lock.release()
    
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
        cls.__loop.set_alarm_in(duration, cls.clear_status)
