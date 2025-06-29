# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.logger import logger
from src.util.ui import ui

from src.modules.webhookmenu.infofetcher import infofetcher
from src.modules.webhookmenu.spammer import spammer
from src.modules.webhookmenu.deleter import deleter

class webhookmenu:
    def __init__(self):
        self.module = 'Webhook Menu'
        self.logger = logger(self.module)
        self.ui = ui(self.module)

    def menu(self):
        self.ui.prep()
        self.ui.createmenu([
            'Info fetcher',
            'Spammer',
            'Deleter',
            'Back'
        ])
        chosen = self.ui.input('Option', str)

        if chosen == '1':
            infofetcher().menu()

        elif chosen == '2':
            spammer().menu()

        elif chosen == '3':
            deleter().menu()

        elif chosen == '4':
            return
        
        else:
            self.menu()