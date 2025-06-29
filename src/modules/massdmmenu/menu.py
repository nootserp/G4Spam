# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.logger import logger
from src.util.ui import ui

class massdmmenu:
    def __init__(self):
        self.module = 'Mass DM Menu'
        self.logger = logger(self.module)
        self.ui = ui(self.module)

    def menu(self):
        self.ui.prep()
        self.ui.createmenu([
            'One user mass DM (PAID)',
            'Back'
        ])
        self.logger.log('Use the advertising menu to mass DM with multiple targets')
        chosen = self.ui.input('Option', str)

        if chosen == '1':
            self.logger.log('This feature is paid only')

        elif chosen == '3':
            return
        
        else:
            self.menu()