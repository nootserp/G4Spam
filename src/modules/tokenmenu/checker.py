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

class checker:
    def __init__(self):
        self.module = 'Checker'
        self.logger = logger(self.module)
        self.ui = ui(self.module)

        self.valids = []
        self.failed = []
        self.locked = []
        self.nitro = []
        self.nonitro = []

    def check(self, token, cl: client=None):
        ctoken = self.ui.cut(token, 20, '...')
        try:
            if not cl:
                cl = client(token)

            r = cl.sess.get(
                f'https://discord.com/api/v9/users/@me/library',
                headers=cl.headers,
            )

            if r.status_code == 200:
                self.valids.append(token)

                self.logger.succeded(text=f'{ctoken} Valid TOKEN INFO IS PAID ONLY')

            elif 'retry_after' in r.text:
                limit = r.json().get('retry_after', 1.5)
                self.logger.ratelimited(f'{ctoken} Rate limited', limit)
                time.sleep(float(limit))
                self.check(token, cl)

            elif 'Try again later' in r.text:
                self.logger.ratelimited(f'{ctoken} Rate limited', 5)
                time.sleep(5)
                self.check(token, cl)

            elif 'Cloudflare' in r.text:
                self.logger.cloudflared(f'{ctoken} Cloudflare rate limited', 10)
                time.sleep(10)
                self.check(token, cl)
            
            elif 'captcha_key' in r.text:
                self.logger.hcaptcha(f'{ctoken} Hcaptcha required')

            elif 'You need to verify' in r.text:
                self.logger.locked(f'{ctoken} Locked/Flagged')

            else:
                error = self.logger.errordatabase(r.text)
                self.logger.error(f'{ctoken}', error)

        except Exception as e:
            self.logger.error(f'{ctoken} Failed to check', e)

    def menu(self):
        self.ui.prep()
        self.delay = self.ui.delayinput()

        threading(
            func=self.check,
            tokens=files.gettokens(),
            delay=self.delay,
        )

        if self.valids:
            save = self.ui.input('Replace tokens.txt with only valid tokens', bool)
            if save:
                with open('data\\tokens.txt', 'w') as f:
                    f.write('\n'.join(self.valids))
        
        else:
            self.logger.log('Blud has no valid tokens 😭😭😭')

        timestamp = dt.now().strftime('%Y-%m-%d--%H-%M-%S')
        timestamp = f'{timestamp}--{len(files.gettokens())}-TOKENS-LIMITED-REPORT'
        fullpath = f'data\\checker\\{timestamp}'
        os.makedirs(fullpath, exist_ok=True)

        with open(f'{fullpath}\\valids.txt', 'w') as f:
            f.write('\n'.join(self.valids))

        with open(f'{fullpath}\\failed-invalid.txt', 'w') as f:
            f.write('\n'.join(self.failed))

        with open(f'{fullpath}\\locked.txt', 'w') as f:
            f.write('\n'.join(self.locked))

        with open(f'{fullpath}\\nitro.txt', 'w') as f:
            f.write('\n'.join(self.nitro))

        with open(f'{fullpath}\\nonitro.txt', 'w') as f:
            f.write('\n'.join(self.nonitro))

        os.system(f'start {fullpath}')

        self.logger.log(f'Made limited report on {fullpath} (FULL DETAILED REPORT WITH WAY MORE INFO IS PAID ONLY)')