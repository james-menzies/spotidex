import urwid

from spotidex.viewmodels.entry_vm import EntryVM


class Entry:
    pass
    
    def __init__(self):
        self.vm = EntryVM()
        txt = urwid.Text(self.vm.current)
        self.__widget = urwid.Filler(txt)
    
    @property
    def widget(self):
        return self.__widget
