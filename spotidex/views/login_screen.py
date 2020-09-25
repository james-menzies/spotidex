import urwid
from spotidex.viewmodels.login_screen_vm import LoginScreenVM
from .components import Menu
from .main_menu import MainMenu


class LoginScreen:
    
    def __init__(self):
        self.__login_menu = self.__init_login_menu()
        
        self.viewModel = LoginScreenVM()
    
    def __init_login_menu(self):
        choices = {
            "Login": self.log_in,
            "Exit Spotidex": self.exit_program,
        }
        
        title = "Welcome to Spotidex"
        self.login_status = urwid.Text("")
        
        menu = Menu(title=title)
        menu.add_choice_block(choices)
        menu.add_text(self.login_status)
        return menu.build()
    
    def exit_program(self, button):
        raise urwid.ExitMainLoop()
    
    def log_in(self, button):
        self.login_status.set_text("Attempting to login, press ctrl C to cancel")
        success, message = self.viewModel.login()
        self.login_status.set_text(message)
        
    
    def get_widget(self):
        return self.__login_menu
