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

class profilemassreport:
    def __init__(self):
        self.module = 'Profile Mass Report'
        self.logger = logger(self.module)
        self.ui = ui(self.module)
        self.userid = None
        self.serverid = None
        self.reason = None
        self.delay = 0

    def report(self, token, cl: client=None):
        ctoken = self.ui.cut(token, 20, '...')
        try:
            if not cl:
                cl = client(token)

            r = cl.sess.post(
                'https://discord.com/api/v9/report',
                headers=cl.headers,
                json={
                    'version': '1.0',
                    'variant': '3',
                    'language': 'en',
                    'breadcrumbs': [10, 21, self.reason],
                    'elements': {},
                    'name': 'user',
                    'user_id': self.userid,
                    'guild_id': self.serverid
                }
            )

            if r.status_code == 201:
                self.logger.succeded(f'{ctoken} Reported user')

            elif 'retry_after' in r.text:
                limit = r.json().get('retry_after', 1.5)
                self.logger.ratelimited(f'{ctoken} Rate limited', limit)
                time.sleep(float(limit))
                self.report(token, cl)

            elif 'Try again later' in r.text:
                self.logger.ratelimited(f'{ctoken} Rate limited', 5)
                time.sleep(5)
                self.report(token, cl)

            elif 'Cloudflare' in r.text:
                self.logger.cloudflared(f'{ctoken} Cloudflare rate limited', 10)
                time.sleep(10)
                self.report(token, cl)
            
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
        self.userid = self.ui.input('User ID to report', str)
        self.serverid = self.ui.input('Server ID (where the user is)', str)
        
        reasons = {
            '1': 'Spam',
            '2': 'Harassment',
            '3': 'Doxxing',
            '4': 'Self-harm',
            '5': 'NSFW content'
        }
        
        self.ui.createmenu(list(reasons.values()))
        choice = self.ui.input('Report reason', int)
        self.reason = choice
        
        self.delay = self.ui.delayinput()

        threading(
            func=self.report,
            tokens=files.gettokens(),
            delay=self.delay,
        )