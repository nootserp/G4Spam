# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *

class other:
    def getrepostars():
        try:
            r = requests.get('https://api.github.com/repos/R3CI/G4Spam', timeout=5)
            return r.json().get('stargazers_count', 'Unk')
        except:
            return 'Unk'
   
    def addlaunch():
        try:
            requests.post(f'http://prem-eu1.bot-hosting.net:22100/launch/free', timeout=3)
        except:
            pass
    
    def getlaunches():
        try:
            r = requests.get(f'http://prem-eu1.bot-hosting.net:22100/launches/free', timeout=3)
            data = r.json()
            return str(data.get('count', 0))
        except:
            return '0'
    
    def delay(seconds):
        seconds = float(seconds)
        if seconds > 0:
            time.sleep(seconds)

    def cleanchoice(choice):
        choice = re.sub(r'[^a-zA-Z0-9><?&]', '', choice)
        choice = re.sub(r'0(?=\d)', '', choice)
        return choice
    
    def getstring(length):
        return ''.join(random.choices(string.digits, k=length))
    
    def getemoji(length):
        emoji_ranges = [
            (0x1F600, 0x1F64F),
            (0x1F300, 0x1F5FF),
            (0x1F680, 0x1F6FF),
            (0x1F700, 0x1F77F),
            (0x1F900, 0x1F9FF),
        ]
        emojis = [chr(code) for start, end in emoji_ranges for code in range(start, end + 1)]
        return ''.join(random.choices(emojis, k=length))

    def makepings(ids):
        return ' '.join(f'<@{i}>' for i in ids)