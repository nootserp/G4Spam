from src import *
from src.util.logger import logger
from src.util.ui import ui

class scrapingmenu:
    def __init__(self):
        self.module = 'Scraping Menu'
        self.logger = logger(self.module)
        self.ui = ui(self.module)

    def menu(self):
        self.ui.prep()
        self.ui.createmenu([
            'ID Scraper (PAID)',
            'Username scraper (PAID)',
            'Invite scraper',
            'Back'
        ])
        chosen = self.ui.input('Option', str)

        if chosen == '1':
            self.logger.log('This feature is paid only')

        elif chosen == '2':
            self.logger.log('This feature is paid only')
        
        elif chosen == '3':
            self.logger.log('Soon will be added')

        elif chosen == '4':
            return
        
        else:
            self.menu()