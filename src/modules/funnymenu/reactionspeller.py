# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.logger import logger
from src.util.client import client
from src.util.ui import ui
from src.util.discordutils import discordutils
from src.util.threading import threading
from src.util.files import files

class reactionspeller:
    def __init__(self):
        self.module = 'Reaction Speller'
        self.logger = logger(self.module)
        self.ui = ui(self.module)
        self.channelid = None
        self.messageid = None
        self.word = None
        self.delay = 0

    def react(self, token, cl: client=None):
        ctoken = self.ui.cut(token, 20, '...')
        try:
            if not cl:
                cl = client(token)

            for letter in self.word.lower():
                if letter.isalpha():
                    emoji = f'🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿'[ord(letter) - ord('a')]
                    
                    r = cl.sess.put(
                        f'https://discord.com/api/v9/channels/{self.channelid}/messages/{self.messageid}/reactions/{emoji}/@me',
                        headers=cl.headers
                    )

                    if r.status_code == 204:
                        self.logger.succeded(f'{ctoken} Reacted with {emoji}')
                    else:
                        self.logger.error(f'{ctoken} Failed to react with {emoji}')

                    time.sleep(self.delay)

        except Exception as e:
            self.logger.error(f'{ctoken}', e)

    def menu(self):
        self.ui.prep()
        message_link = self.ui.input('Message Link', str)
        ids = discordutils.extractids(message_link)
        self.channelid = ids['channel']
        self.messageid = ids['message']
        
        self.word = self.ui.input('Word to spell', str)
        self.delay = float(self.ui.delayinput())

        threading(
            func=self.react,
            tokens=files.gettokens()[:1],  # Only use one token
            delay=0,
        )