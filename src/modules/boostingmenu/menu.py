# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam


from src import *
from src.util.logger import logger
from src.util.ui import ui

class boostingmenu:
    def __init__(self):
        self.module = 'Boosting Menu'
        self.logger = logger(self.module)
        self.ui = ui(self.module)

    def menu(self):
        self.ui.prep()
        self.ui.createmenu([
            'If somone wants this quicker give me a nitro token to test and make it :skull:',
            'Back'
        ])
        chosen = self.ui.input('Option', str)

        if chosen == '1':
            self.menu()

        elif chosen == '2':
            return
        
        else:
            self.menu()