import urwid
from spotidex.viewmodels.login_screen_vm import LoginScreenVM
from .components import Menu, Choice
from .main_menu import MainMenu
from .terminal_wrapper import TerminalWrapper


class LoginScreen:
    
    def __init__(self):
        self.__widget = self.__init_widget()
        self.__vm = LoginScreenVM()
    
    def __init_widget(self):
        choices = [
            Choice("Login", self.log_in),
            Choice("Exit Spotidex", TerminalWrapper.exit),
        ]
        
        title = "Welcome to Spotidex"
        self.login_status = urwid.Text("")
        
        menu = Menu(title=title)
        menu.add_choice_block(choices)
        menu.add_text(self.login_status)
        return menu.build()
    
    def log_in_result(self, data):
        self.login_status.set_text(data)
        
        if self.__vm.success:
            TerminalWrapper.change_screen(MainMenu())
    
    def log_in(self, button):
        TerminalWrapper.run_task(self.__vm.login, update=self.log_in_result)
    
    @property
    def widget(self):
        return self.__widget
