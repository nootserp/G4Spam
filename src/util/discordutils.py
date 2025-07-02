# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.client import client
from src.util.logger import logger
logger = logger('Discord Utils')

class discordutils:
    def extractinv(invite):
        pattern = r'(?:(?:https?:\/\/)?(?:www\.)?(?:discord\.(?:gg|com)|discordapp\.com)\/(?:invite\/|channels\/@me\/)?)?([a-zA-Z0-9\-_]+)'
        
        match = re.search(pattern, invite, re.IGNORECASE)
        if match:
            return match.group(1)
        
        return invite
    
    def getid(token) :
        period = token.find('.')
        if period != -1: 
            cut = token[:period]
        return base64.b64decode(cut + '==').decode()
    
    def getsnowflake():
        return ((int(time.time() * 1000) - 1420070400000) << 22)
    
    def extractids(text):
        pattern = r'(?:https?:\/\/)?(?:www\.)?(?:discord\.com|discordapp\.com)\/channels(?:\/(@me|\d+))?(?:\/(\d+))?(?:\/(\d+))?'
        
        match = re.search(pattern, text, re.IGNORECASE)
        return {
            'server': match.group(1) if match else None,
            'channel': match.group(2) if match else None,
            'message': match.group(3) if match else None
        }
    
    def getreactions(tokens, channelid, messageid):
        logger_ = logger('Get Reactions')
        random.shuffle(tokens[:])

        reactions = []
        try:
            for token in tokens:
                cl = client(token)
                ctoken = ui().cut(token, 20, '...')

                for _ in range(2):
                    r = cl.sess.get(
                        f'https://discord.com/api/v9/channels/{channelid}/messages?limit=50',
                        headers=cl.headers
                    )

                    if r.status_code == 200:
                        logger_.succeded(f'{ctoken} Fetched reactions', False)
                        for message in r.json():
                            if message['id'] == messageid:
                                for reaction in message['reactions']:
                                    if not message['reactions']:
                                        return reactions

                                    emoji_name = reaction['emoji']['name']
                                    emoji_id = reaction['emoji']['id']
                                    count = reaction['count']
                                    reactions.append((emoji_name, emoji_id, count))
                                
                                return reactions

                    elif 'retry_after' in r.text:
                        limit = r.json().get('retry_after', 1.5)
                        logger_.ratelimited(f'{ctoken} Rate limited', limit, False)
                        time.sleep(float(limit))

                    elif 'Try again later' in r.text:
                        logger_.ratelimited(f'{ctoken} Rate limited', 5, False)
                        time.sleep(5)

                    elif 'Cloudflare' in r.text:
                        logger_.cloudflared(f'{ctoken} Cloudflare rate limited', 10, False)
                        time.sleep(10)
                    
                    elif 'captcha_key' in r.text:
                        logger_.hcaptcha(f'{ctoken} Hcaptcha required', False)

                    elif 'You need to verify' in r.text:
                        logger_.locked(f'{ctoken} Locked/Flagged', False)

                    else:
                        error = logger_.errordatabase(r.text)
                        logger_.error(f'{ctoken}', error, False)
                
                if reactions:
                    break
            
            logger_.error('Failed to fetch reactions', '', False)
            return reactions
            
        except Exception as e:
            logger_.error('Failed to fetch reactions', e, False)
            return reactions