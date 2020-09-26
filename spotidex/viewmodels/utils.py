import time
from typing import Callable


def flash_message(message: str, write_func: Callable):
    write_func(message)
    time.sleep(1)
    write_func(" ")
