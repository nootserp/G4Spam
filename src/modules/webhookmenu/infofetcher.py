# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.logger import logger
from src.util.client import client
from src.util.ui import ui

class infofetcher:
    def __init__(self):
        self.module = 'Info Fetcher'
        self.logger = logger(self.module)
        self.ui = ui(self.module)

        self.webhook = None

    def fetch(self):
        try:
            cl = client()
            r = cl.sess.get(self.webhook)
            
            if r.status_code == 200:
                data = r.json()
                self.logger.succeded('Webhook valid')
                
                self.logger.log(f'Name » {data.get("name", "Unk")}')
                self.logger.log(f'ID » {data.get("id", "Unk")}')
                self.logger.log(f'Type » {data.get("type", "Unk")}')
                self.logger.log(f'Token » {data.get("token", "Unk")}')

                if 'channel_id' in data:
                    self.logger.log(f'Channel ID » {data["channel_id"]}')

                if 'guild_id' in data:
                    self.logger.log(f'Server ID » {data["guild_id"]}')
                    
                if data.get('avatar'):
                    self.logger.log(f'Avatar URL » https://cdn.discordapp.com/avatars/{data["id"]}/{data["avatar"]}.png')
                    
                if 'user' in data:
                    user = data['user']
                    user = dict(user)
                    self.logger.log(f'Creator » {user.get("username", "Unk")}')
                    self.logger.log(f'Creator ID » {user.get("id", "Unk")}')

                if 'application_id' in data:
                    self.logger.log(f'Application ID » {data["application_id"]}')
                    
                if 'source_guild' in data:
                    source = data['source_guild']
                    source = dict(source)
                    self.logger.log(f'Source Server » {source.get("name", "Unk")} ({source.get("id", "Unk")})')
                    
                if 'source_channel' in data:
                    source = data['source_channel']
                    source = dict(source)
                    self.logger.log(f'Source Channel » {source.get("name", "Unk")} ({source.get("id", "Unk")})')
                    
                self.logger.log(f'Webhook » {self.webhook}')
                
            elif r.status_code == 404:
                self.logger.error('Invalid webhook')
                
            elif 'retry_after' in r.text:
                limit = r.json().get('retry_after', 1.5)
                self.logger.ratelimited('Rate limited', limit)
                time.sleep(float(limit))
                self.fetch()
                
            elif 'Try again later' in r.text:
                self.logger.ratelimited('Rate limited', 5)
                time.sleep(5)
                self.fetch()
                
            elif 'Cloudflare' in r.text:
                self.logger.cloudflared('Cloudflare rate limited', 10)
                time.sleep(10)
                self.fetch()
                
            else:
                error = self.logger.errordatabase(r.text)
                self.logger.error('Failed to fetch info', error)
                
        except Exception as e:
            self.logger.error(f'Failed to fetch info', e)

    def menu(self):
        self.ui.prep()
        self.webhook = self.ui.input('Webhook', str)
            
        self.fetch()