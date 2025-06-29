# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.logger import logger
from src.util.ui import ui
from src.util.threading import threading
from src.util.files import files

class formatter:
    def __init__(self):
        self.module = 'Formatter'
        self.logger = logger(self.module)
        self.ui = ui(self.module)
        self.one = None
        self.second = None
        self.third = None
        self.seperator = None
        self.tokeep = None
        self.formatted = []

    def format(self, tokendata):
        try:
            email, password, token = tokendata
            
            map = {
                'email': email,
                'password': password,
                'token': token,
                'none': None
            }
            
            keepvalue = map.get(self.tokeep.lower(), None)
            if not keepvalue:
                self.logger.error(f'Invalid tokeep {self.tokeep}')
            
            selected = [self.one, self.second, self.third]
            selectedvalues = []
            for item in selected:
                v = map.get(item.lower(), None)
                if v == keepvalue:
                    selectedvalues.append(v)

            if keepvalue not in selectedvalues:
                return

            formatted_token = self.seperator.join(selectedvalues)
            self.logger.succeded(f'Formatted token {formatted_token}')
            self.formatted.append(formatted_token)

        except Exception as e:
            self.logger.error(e)

    def menu(self):
        self.ui.prep()
        self.one = self.ui.input('First position (email/password/token/none) (most commonly email)')
        self.second = self.ui.input('Second position (email/password/token/none) (most commonly password)')
        self.third = self.ui.input('Third position (email/password/token/none) (most commonly token)')
        self.seperator = self.ui.input('Seperator (most commonly :)')
        self.tokeep = self.ui.input('What to keep (email/password/token) (most commonly token)')

        threading(
            func=self.format,
            tokens=files.gettokens(),
        )

        savetokens = self.ui.input('Save formatted tokens to tokens.txt', True)
        if savetokens:
            with open('data\\tokens.txt', 'w') as f:
                f.write('\n'.join(self.formatted))