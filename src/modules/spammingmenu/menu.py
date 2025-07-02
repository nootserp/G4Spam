# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.logger import logger
from src.util.ui import ui

from src.modules.spammingmenu.channelspammer import channelspammer

class spammingmenu:
    def __init__(self):
        self.module = 'Spamming Menu'
        self.logger = logger(self.module)
        self.ui = ui(self.module)

    def menu(self):
        options = {
            'Channel Spammer (FREE)': channelspammer().menu,
            'Multi-Channel Spammer': lambda: (self.logger.log('This option is PAID ONLY, enter to continue'), input('')),
            'Reply Spammer': lambda: (self.logger.log('This option is PAID ONLY, enter to continue'), input('')),
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