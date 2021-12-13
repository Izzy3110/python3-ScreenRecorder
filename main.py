from controller.main_controller import MainController
from controller.cli_thread import CLIThread
from controller.system import parse_commandline_options

if __name__ == '__main__':
    MainController_ = MainController()
    CLIThread_Server = CLIThread(MainController_)
    parse_commandline_options(MainController_, CLIThread_Server)
    #
    # enable disable cli-console
    # CLIThread_Server.start()
