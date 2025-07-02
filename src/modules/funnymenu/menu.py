from src import *
from src.util.logger import logger
from src.util.ui import ui

class funnymenu:
    def __init__(self):
        self.module = 'Funny Menu'
        self.logger = logger(self.module)
        self.ui = ui(self.module)

    def menu(self):
        options = {
            'Reaction Speller': lambda: (self.logger.log('This option is PAID ONLY, enter to continue'), input('')),
            'Chat Crasher': lambda: (self.logger.log('This option is PAID ONLY, enter to continue'), input('')),
            'Audit Log Fucker': lambda: (self.logger.log('This option is PAID ONLY, enter to continue'), input('')),
            'Mass Caller': lambda: (self.logger.log('This option is PAID ONLY, enter to continue'), input('')),
        }
        
        while True:
            self.ui.optionmenu(options)
            choice = self.ui.input('Option', int) - 1
            keys = list(options.keys())
            
            if choice == len(keys):
                return
            
            elif choice < len(keys):
                options[keys[choice]]()
                break

            else:
                self.logger.log('Invalid option')
                input('')