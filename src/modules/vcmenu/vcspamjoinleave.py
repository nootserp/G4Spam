# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.logger import logger
from src.util.client import client
from src.util.ui import ui
from src.util.threading import threading
from src.util.files import files
from src.util.other import other

class vcspamjoinleave:
    def __init__(self):
        self.module = 'VC Spam Join-Leave'
        self.logger = logger(self.module)
        self.ui = ui(self.module)
        self.channelid = None
        self.serverid = None
        self.delay = 0

    def spam(self, token, cl: client=None):
        ctoken = self.ui.cut(token, 20, '...')
        while True:
            try:
                if not cl:
                    cl = client(token)

                # Join VC
                r = cl.sess.patch(
                    f'https://discord.com/api/v9/guilds/{self.serverid}/voice-states/@me',
                    headers=cl.headers,
                    json={
                        'channel_id': self.channelid,
                        'self_mute': False,
                        'self_deaf': False
                    }
                )

                if r.status_code == 204:
                    self.logger.succeded(f'{ctoken} Joined VC')
                else:
                    self.logger.error(f'{ctoken} Failed to join VC')
                    break

                other.delay(self.delay)

                # Leave VC
                r = cl.sess.patch(
                    f'https://discord.com/api/v9/guilds/{self.serverid}/voice-states/@me',
                    headers=cl.headers,
                    json={'channel_id': None}
                )

                if r.status_code == 204:
                    self.logger.succeded(f'{ctoken} Left VC')
                else:
                    self.logger.error(f'{ctoken} Failed to leave VC')

                other.delay(self.delay)

            except Exception as e:
                self.logger.error(f'{ctoken}', e)
                break

    def menu(self):
        self.ui.prep()
        self.serverid = self.ui.input('Server ID', str)
        self.channelid = self.ui.input('Voice Channel ID', str)
        self.delay = self.ui.delayinput()

        threading(
            func=self.spam,
            tokens=files.gettokens(),
            delay=self.delay,
        )