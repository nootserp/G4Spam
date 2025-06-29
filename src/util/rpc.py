# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.files import files
from src.util.config import get

class RPC:
    def __init__(self):
        try:
            if get.RPC.enabled():
                if get.RPC.showdata():
                    smalltext = f'Tokens - {len(files.gettokens())} Proxies - {len(files.getproxies())}'
                else:
                    smalltext = f'Tokens - Private | Proxies - Private'
                self.client_id = '1383168674277363784'
                self.rpc = Presence(self.client_id)
                self.rpc.connect()
                self.rpc.update(
                    state='discord.gg/spamming',
                    details=f'discord.gg/spamming - github.com/R3CI/G4Spam',
                    start=time.time(),
                    large_image='smalllogorounded',
                    large_text='discord.gg/spamming',
                    small_image='folder',
                    small_text=smalltext,
                    buttons=[
                        {'label': 'Join Discord', 'url': 'https://discord.gg/spamming'},
                        {'label': 'Get G4Spam for FREE', 'url': 'https://github.com/R3CI/G4Spam'}
                    ]
                )
        except Exception as e:
            pass

    def update(self, details):
        try:
            if get.RPC.enabled():
                if get.RPC.showdata():
                    smalltext = f'Tokens - {len(files.gettokens())} Proxies - {len(files.getproxies())}'
                else:
                    smalltext = f'Tokens - Private | Proxies - Private'
                self.rpc.update(
                    state=f'Simply the best',
                    details=details,
                    start=time.time(),
                    large_image='smalllogorounded',
                    large_text='discord.gg/spamming',
                    small_image='folder',
                    small_text=smalltext,
                    buttons=[
                        {'label': 'Join Discord', 'url': 'https://discord.gg/spamming'},
                        {'label': 'Get G4Spam for FREE', 'url': 'https://github.com/R3CI/G4Spam'}
                    ]

                )
        except Exception as e:
            pass

RPC = RPC()