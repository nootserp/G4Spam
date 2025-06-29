# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.logger import logger
from src.util.client import client
from src.util.ui import ui

class deleter:
    def __init__(self):
        self.module = 'Deleter'
        self.logger = logger(self.module)
        self.ui = ui(self.module)

        self.webhook = None

    def delete(self):
        try:
            cl = client()
            r = cl.sess.delete(self.webhook)
            
            if r.status_code == 204:
                self.logger.succeded('Deleted')
                
            elif r.status_code == 404:
                self.logger.error('Invalid webhook')
                
            elif 'retry_after' in r.text:
                limit = r.json().get('retry_after', 1.5)
                self.logger.ratelimited('Rate limited', limit)
                time.sleep(float(limit))
                self.delete()
                
            elif 'Try again later' in r.text:
                self.logger.ratelimited('Rate limited', 5)
                time.sleep(5)
                self.delete()
                
            elif 'Cloudflare' in r.text:
                self.logger.cloudflared('Cloudflare rate limited', 10)
                time.sleep(10)
                self.delete()
                
            else:
                error = self.logger.errordatabase(r.text)
                self.logger.error('Failed to fetch info', error)
                
        except Exception as e:
            self.logger.error(f'Failed to fetch info', e)

    def menu(self):
        self.ui.prep()
        self.webhook = self.ui.input('Webhook', str)
            
        self.delete()