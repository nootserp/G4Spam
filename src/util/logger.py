# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *

class logger:
    def __init__(self, module='Logger'):
        self.module = module

    def gettimestamp(self):
        timestamp = dt.now().strftime('%H:%M:%S')
        return timestamp

    def log(self, text, ts=False):
        if ts:
            ts = f'{co.main}[{co.reset}{self.gettimestamp()}{co.main}] '
        else:
            ts = ''
        print(f'{ts}{co.main}[{co.reset}{self.module}{co.main}] {co.main}[{co.reset}{text}{co.main}]{co.reset}')

    def succeded(self, text, ts=True):
        if ts:
            ts = f'{co.main}[{co.reset}{self.gettimestamp()}{co.main}] '
        else:
            ts = ''

        print(f'{ts}{co.main}[{co.reset}{self.module}{co.main}] {co.main}[{co.green}{text}{co.main}]{co.reset}')

    def ratelimited(self, text, fortime=0, ts=True):
        if fortime == 0:
            endstr = ''
        else:
            endstr = f'{co.main}[{co.yellow}{fortime}{co.main}]{co.reset}'

        if ts:
            ts = f'{co.main}[{co.reset}{self.gettimestamp()}{co.main}] '
        else:
            ts = ''

        print(f'{ts}{co.main}[{co.reset}{self.module}{co.main}] {co.main}[{co.yellow}{text}{co.main}] {endstr}{co.reset}')

    def cloudflared(self, text, fortime=0, ts=True):
        if fortime == 0:
            endstr = ''
        else:
            endstr = f'{co.main}[{co.orange}{fortime}{co.main}]{co.reset}'

        if ts:
            ts = f'{co.main}[{co.reset}{self.gettimestamp()}{co.main}] '
        else:
            ts = ''

        print(f'{ts}{co.main}[{co.reset}{self.module}{co.main}] {co.main}[{co.orange}{text}{co.main}] {endstr}{co.reset}')

    def locked(self, text, ts=True):
        if ts:
            ts = f'{co.main}[{co.reset}{self.gettimestamp()}{co.main}] '
        else:
            ts = ''

        print(f'{ts}{co.main}[{co.reset}{self.module}{co.main}] {co.main}[{co.darkred}{text}{co.main}]{co.reset}')

    def hcaptcha(self, text, ts=True):
        if ts:
            ts = f'{co.main}[{co.reset}{self.gettimestamp()}{co.main}] '
        else:
            ts = ''

        print(f'{ts}{co.main}[{co.reset}{self.module}{co.main}] {co.main}[{co.cyan}{text}{co.main}]{co.reset}')

    def error(self, text, error='', ts=True):
        if error == '':
            endstr = ''
        else:
            endstr = f'{co.main}[{co.red}{error}{co.main}]{co.reset}'

        if ts:
            ts = f'{co.main}[{co.reset}{self.gettimestamp()}{co.main}] '
        else:
            ts = ''

        print(f'{ts}{co.main}[{co.reset}{self.module}{co.main}] {co.main}[{co.red}{text}{co.main}] {endstr}{co.reset}')

    # Full error database in paid only bc os skiddies 👍👍👍👍👍👍👍👍👍👍
    def errordatabase(self, text):
        db = {
            '10014': 'Unknown emoji',
            '30010': 'Max reactions on message',
            '40007': 'Banned token',
            '40002': 'Locked token',
            '50109': 'Invalid JSON',
            '200000': 'Automod flagged',
            '50007': 'Action not allowed',
            '50008': 'Unable to send',
            '50001': 'No access/Not inside',
            '50013': 'Missing permissions',
            '50024': 'Cant do that on this channel',
            '80003': 'Cant self friend',
            '50168': 'Not in a VC',
            '20028': 'Limited',
            '340013': 'Muted/Acces to send messages limited by server',
            '401: Unauthorized': 'Invalid token/Lock invalided token',
            'Cloudflare': 'Cloudflare',
            'captcha_key': 'Hcaptcha',
            'Unauthorized': 'Invalid token/Lock invalided token',
            'retry_after': 'Limited',
            'You need to verify': 'Locked token',
            'Cannot send messages to this user': 'Disabled DMS',
            'You are being blocked from accessing our API': 'API BAN',
            'Unknown Invite': 'Unknown Invite',
            '150009': 'Alerdy a member (no need to verify)',
            '50055': 'Invalid server',
            '50009': 'Verification too high (server requires PV, EV or being in server for 10 mins)',
            '50035': 'Invalid JSON',
            'Unknown Guild': 'Not in server',
        }

        for key in db.keys():
            if key in text:
                return db[key]

        return text