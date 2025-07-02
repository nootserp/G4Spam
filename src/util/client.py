# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.logger import logger
from src.util.apibypassing import apibypassing
from src.util.curlwrapper import curlwrapper
logger = logger('Client')
apibypassing = apibypassing()

logger.log(f'Latest info fingerprint={apibypassing.fingerprint} client_build={apibypassing.clientbuild}', True)

tempsess = curlwrapper.Session(impersonate=apibypassing.fingerprint)
cookie = apibypassing.getcookie(apibypassing.headers, tempsess)
logger.log(f'Got discord info', True)

class client:
    # Full client bypassing in paid only bc of skiddies 👍👍👍👍
    def __init__(self, token=None):
        self.sess = curlwrapper.Session(impersonate=apibypassing.fingerprint)
        self.launchid = str(uuid.uuid4())
        self.wssessid = str(uuid.uuid4())
        self.sess.cookies.update(cookie)

        self.headers = copy.deepcopy(apibypassing.headers)
        self.headers['authorization'] = token

        xsuper = copy.deepcopy(apibypassing.xsuper)
        xsuper['client_launch_id'] = self.launchid
        xsuper['client_heartbeat_session_id'] = self.wssessid
        xsuper = apibypassing.encode(xsuper)
        self.headers['x-super-properties'] = xsuper

        