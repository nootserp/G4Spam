# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.logger import logger
from src.util.client import client
from src.util.ui import ui

class spammer:
    def __init__(self):
        self.module = 'Spammer'
        self.logger = logger(self.module)
        self.ui = ui(self.module)

        self.webhook = None
        self.message = None

    def spam(self):
        while True:
            try:
                cl = client()
                r = cl.sess.post(
                    self.webhook,
                    json={
                        'content': self.message
                    }
                )
                
                if r.status_code == 204:
                    self.logger.succeded('Sent message')
                    
                elif r.status_code == 404:
                    self.logger.error('Invalid webhook')
                    break
                    
                elif 'retry_after' in r.text:
                    limit = r.json().get('retry_after', 1.5)
                    self.logger.ratelimited('Rate limited', limit)
                    time.sleep(float(limit))
                    continue
                    
                elif 'Try again later' in r.text:
                    self.logger.ratelimited('Rate limited', 5)
                    time.sleep(5)
                    continue
                    
                elif 'Cloudflare' in r.text:
                    self.logger.cloudflared('Cloudflare rate limited', 10)
                    time.sleep(10)
                    continue
                    
                else:
                    error = self.logger.errordatabase(r.text)
                    self.logger.error('Failed to send', error)
                    break
                    
            except Exception as e:
                self.logger.error(f'Failed to send', e)
                break

    def menu(self):
        self.ui.prep()
        self.webhook = self.ui.input('Webhook', str)
        self.message = self.ui.input('Message', str)

        self.spam()