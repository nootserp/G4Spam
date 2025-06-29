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

class leaver:
    def __init__(self):
        self.module = 'Leaver'
        self.logger = logger(self.module)
        self.ui = ui(self.module)
        self.serverid = None

    def leave(self, token, cl: client=None):
        ctoken = self.ui.cut(text=token, length=20, end='...')
        try:
            if not cl:
                cl = client(token)

            r = cl.sess.delete(
                f'https://discord.com/api/v9/users/@me/guilds/{self.serverid}',
                headers=cl.headers,
                json={
                    'lurking': False
                }
            )

            if r.status_code == 204:
                self.logger.succeded(f'{ctoken} Left')

            elif 'retry_after' in r.text:
                limit = r.json().get('retry_after', 1.5)
                self.logger.ratelimited(f'{ctoken} Rate limited', limit)
                time.sleep(float(limit))
                self.leave(token, cl)

            elif 'Try again later' in r.text:
                self.logger.ratelimited(f'{ctoken} Rate limited', 5)
                time.sleep(5)
                self.leave(token, cl)

            elif 'Cloudflare' in r.text:
                self.logger.cloudflared(f'{ctoken} Cloudflare rate limited', 10)
                time.sleep(10)
                self.leave(token, cl)
            
            elif 'captcha_key' in r.text:
                self.logger.hcaptcha(f'{ctoken} Hcaptcha required')

            elif 'You need to verify' in r.text:
                self.logger.locked(f'{ctoken} Locked/Flagged')

            else:
                error = self.logger.errordatabase(r.text)
                self.logger.error(f'{ctoken}', error)

        except Exception as e:
            self.logger.error(f'{ctoken}', e)

    def menu(self):
        self.ui.prep()
        self.serverid = self.ui.input('Server ID', str)
        self.delay = self.ui.delayinput()

        threading(
            func=self.leave,
            tokens=files.gettokens(),
            delay=self.delay,
        )