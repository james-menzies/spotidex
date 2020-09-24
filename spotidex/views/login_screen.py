import urwid
from spotidex.viewmodels.login_screen_vm import LoginScreenVM


class LoginScreen:
    
    def __init__(self):
        self.__login_menu = self.__init_login_menu()
        self.__error_screen = self.__init_error_screen()
        self.__login_screen = urwid.Padding(self.__login_menu, left=20, right=20, align='center')
        self.viewModel = LoginScreenVM()
    
    def __init_login_menu(self):
        choices = {
            "Login": self.log_in,
            "Exit Spotidex": self.exit_program,
        }
        
        title = urwid.Text("Welcome to Spotidex")
        div = urwid.Divider()
        self.__body = [title, div]
        
        for choice in choices:
            button = urwid.Button(choice)
            urwid.connect_signal(button, 'click', choices[choice])
            self.__body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        self.__body.append(div)
        self.login_status = urwid.Text("")
        self.__body.append(self.login_status)
        return urwid.ListBox(urwid.SimpleFocusListWalker(self.__body))
    
    def __init_error_screen(self):
        pass
    
    def exit_program(self, button):
        raise urwid.ExitMainLoop()
    
    def log_in(self, button):
        self.login_status.set_text("Attempting to login, press ctrl C to cancel")
        success, message = self.viewModel.login()
        self.login_status.set_text(message)
    
    def get_widget(self):
        return self.__login_screen
