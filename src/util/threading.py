# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.logger import logger
from src.util.other import other
from curl_cffi import exceptions as curl_exceptions
from curl_cffi.curl import CurlError

class threading:
    def __init__(self, func, tokens=[], args=[], delay=0):
        self.log = logger('Threading')
        self.func = func
        self.tokens = tokens
        self.args = args
        self.delay = delay
        self.work()

    def work(self):
        try:
            threads = []
            for token in self.tokens:
                other.delay(self.delay)
                thread: threadinglib.Thread = threadinglib.Thread(target=self.func, args=(token, *self.args))
                threads.append(thread)
                thread.start()
            
            for thread in threads:
                thread.join()
                
        except CurlError as e:
            self.log.error('CurlError', str(e))

        except curl_exceptions.ConnectionError as e:
            self.log.error('Connection error', str(e))

        except curl_exceptions.HTTPError as e:
            self.log.error('HTTP error', str(e))

        except curl_exceptions.ReadTimeout as e:
            self.log.error('Read timeout', str(e))

        except curl_exceptions.Timeout as e:
            self.log.error('Timeout error', str(e))

        except curl_exceptions.TooManyRedirects as e:
            self.log.error('Too many redirects', str(e))

        except curl_exceptions.RequestException as e:
            self.log.error('Request exception', str(e))
        
        except Exception as e:
            self.log.error('Unexpected error', str(e))