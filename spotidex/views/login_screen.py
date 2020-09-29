import urwid
from spotidex.viewmodels.login_screen_vm import LoginScreenVM
from .components import Menu, Choice
from .main_menu import MainMenu
from .terminal_wrapper import TerminalWrapper


class LoginScreen:
    
    def __init__(self):
        self.__widget = self.__init_widget()
        self.__vm = LoginScreenVM()
        
        self.write_pipe = TerminalWrapper.get_pipe(self.login_update)
    
    def __init_widget(self):
        choices = [
            Choice("Login", self.log_in),
            Choice("Exit Spotidex", TerminalWrapper.exit),
        ]
        
        title = "Welcome to Spotidex"
        
        menu = Menu(title=title)
        menu.add_choice_block(choices)
        return menu.build()
    
    def login_update(self, data):
        TerminalWrapper.flash_message(data)
        
        if self.__vm.success:
            TerminalWrapper.change_screen(MainMenu())
    
    def log_in(self, button):
        TerminalWrapper.run_task(self.__vm.login, self.write_pipe)
    
    @property
    def widget(self):
        return self.__widget
