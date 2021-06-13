from tkinter import *
from LoginWindow import LoginWindow
from ClientWindow import ClientWindow

#from ClientWindow import *
import os

class Application:
    def __init__(self):
        home = os.path.expanduser("~")
        if False:# not os.path.isfile(home+"/.mailclient"):
            self.window = LoginWindow()
        else:
            pass
            self.window = ClientWindow("kamil.wrzesniak@onet.pl")


application = Application()