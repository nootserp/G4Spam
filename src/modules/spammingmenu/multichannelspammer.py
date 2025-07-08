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
from src.util.other import other

class multichannelspammer:
    def __init__(self):
        self.module = 'Multi-Channel Spammer'
        self.logger = logger(self.module)
        self.ui = ui(self.module)
        self.messages = []
        self.channels = []
        self.delay = 0

    def spam(self, token, cl: client=None):
        ctoken = self.ui.cut(token, 20, '...')
        while True:
            try:
                other.delay(self.delay)
                if not cl:
                    cl = client(token)

                channel = random.choice(self.channels)
                message = random.choice(self.messages)

                r = cl.sess.post(
                    f'https://discord.com/api/v9/channels/{channel}/messages',
                    headers=cl.headers,
                    json={
                        'mobile_network_type': 'unknown',
                        'content': message,
                        'nonce': discordutils.getsnowflake(),
                        'flags': 0
                    }
                )

                if r.status_code == 200:
                    self.logger.succeded(f'{ctoken} Sent message to {channel}')
                    continue

                elif 'retry_after' in r.text:
                    limit = r.json().get('retry_after', 1.5)
                    self.logger.ratelimited(f'{ctoken} Rate limited', limit)
                    time.sleep(float(limit))
                    continue

                elif 'Try again later' in r.text:
                    self.logger.ratelimited(f'{ctoken} Rate limited', 5)
                    time.sleep(5)
                    continue

                elif 'Cloudflare' in r.text:
                    self.logger.cloudflared(f'{ctoken} Cloudflare rate limited', 10)
                    time.sleep(10)
                    continue
                
                elif 'captcha_key' in r.text:
                    self.logger.hcaptcha(f'{ctoken} Hcaptcha required')

                elif 'You need to verify' in r.text:
                    self.logger.locked(f'{ctoken} Locked/Flagged')

                else:
                    error = self.logger.errordatabase(r.text)
                    self.logger.error(f'{ctoken}', error)
                    break

            except Exception as e:
                self.logger.error(f'{ctoken}', e)
                break

    def menu(self):
        self.ui.prep()
        
        # Get channels
        if self.ui.input('Load channels from file', bool):
            path = files.choosefile()
            if os.path.exists(path):
                with open(path, 'r') as f:
                    self.channels = [line.strip() for line in f.readlines() if line.strip()]
            else:
                self.logger.log('File does not exist')
                return
        else:
            while True:
                channel = self.ui.input('Channel ID (or "done" to finish)', str)
                if channel.lower() == 'done':
                    break
                self.channels.append(channel)

        if not self.channels:
            self.logger.log('No channels provided')
            return

        # Get messages
        if self.ui.input('Use messages from a file', bool):
            path = files.choosefile()
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    self.messages = f.read().splitlines()
            else:
                self.logger.log('File does not exist')
                self.messages = [self.ui.input('Message', str)]
        else:
            self.messages = [self.ui.input('Message', str)]

        self.delay = self.ui.delayinput()

        threading(
            func=self.spam,
            tokens=files.gettokens(),
            delay=self.delay,
        )