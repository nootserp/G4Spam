from src import *
from src.util.logger import logger
from src.util.ui import ui

class funnymenu:
    def __init__(self):
        self.module = 'Funny Menu'
        self.logger = logger(self.module)
        self.ui = ui(self.module)

    def menu(self):
        self.ui.prep()
        self.ui.createmenu([
            'Reaction speller (PAID)',
            'Chat crasher (PAID)',
            'Audit log fucker (PAID)',
            'Mass caller (PAID)',
            'Back'
        ])
        chosen = self.ui.input('Option', str)

        if chosen == '1':
            self.logger.log('This feature is paid only')

        elif chosen == '2':
            self.logger.log('This feature is paid only')

        elif chosen == '3':
            self.logger.log('This feature is paid only')

        elif chosen == '4':
            self.logger.log('This feature is paid only')

        elif chosen == '5':
            return
        
        else:
            self.menu()