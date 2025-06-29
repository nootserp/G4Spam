# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.logger import logger
logger = logger('Config')

class config:
    def __init__(self):
        self.filename = 'config.ini'
        self.defaults = {
            'RPC': {
                'Enabled': (True, 'Make RPC visible'),
                'Show data': (True, 'Shows how many tokens and proxies you have loaded')
            },
            'Proxies': {
                'Enabled': (False, 'Enable proxy support')
            },
            'Solver': {
                'Enabled': (False, 'Enable solver'),
                'API Key': ('SOLVERAPIKEY', 'Your solver api key'),
                'Service': ('soon', 'Your solver service (freecap, vastcap)')
            },
        }
        self.config = {}
        self.load()
        
    def load(self):
        if not os.path.exists(self.filename):
            self.save()
            return

        self.config = {}
        with open(self.filename, 'r') as f:
            current_section = None
            for line in f:
                line = line.strip()
                if line.startswith('[') and line.endswith(']'):
                    current_section = line[1:-1]
                    self.config[current_section] = {}
                elif '=' in line:
                    key_value = line.split('//', 1)[0].strip()
                    key, value = map(str.strip, key_value.split('=', 1))
                    
                    if value == 'True':
                        value = True
                    elif value == 'False':
                        value = False
                    
                    self.config[current_section][key] = value

        self.validate()
        
    def validate(self):
        updated = False
        for section, values in self.defaults.items():
            if section not in self.config:
                self.config[section] = {}
                updated = True
            for key, (default, _) in values.items():
                if key not in self.config[section]:
                    self.config[section][key] = default
                    updated = True
                    
        if updated:
            self.save()
            
    def get(self, section, key, fallback=None):
        return self.config.get(section, {}).get(key, fallback)
        
    def set(self, section, key, value):
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        self.save()
        
    def remove(self, section, key=None):
        if key:
            self.config.get(section, {}).pop(key, None)
        else:
            self.config.pop(section, None)
        self.save()
        
    def save(self):
        with open(self.filename, 'w') as f:
            for section, values in self.defaults.items():
                f.write(f'\n[{section}]\n')
                for key, (default, comment) in values.items():
                    value = self.config.get(section, {}).get(key, default)
                    f.write(f'{key} = {value}  // {comment}\n')
    
    def check(self):
        if get.proxies.enabled():
            logger.log('Proxies are PAID ONLY switched them off in the config for you! Enter to continue')
            switch.proxies.enabled.false()
            input('')

        if get.solver.enabled():
            logger.log('Proxies are PAID ONLY switched them off in the config for you! Enter to continue')
            switch.proxies.enabled.false()
            input('')

class switch:
    class RPC:
        class enabled:
            def true():
                config().set('RPC', 'Enabled', True)
            
            def false():
                config().set('RPC', 'Enabled', False)

        class showdata:
            def true():
                config().set('RPC', 'Show data', True)
            
            def false():
                config().set('RPC', 'Show data', False)
    
    class proxies:
        class enabled:
            def true():
                config().set('Proxies', 'Enabled', True)
            
            def false():
                config().set('Proxies', 'Enabled', False)

    class solver:
        class enabled:
            def true():
                config().set('Solver', 'Enabled', True)
            
            def false():
                config().set('Solver', 'Enabled', False)
            
        class apikey:
            def set():
                config().set('Solver', 'API Key', None)
            
        class service:
            def set():
                config().set('Solver', 'Service', None)

class get:
    class RPC:
        def enabled():
            return config().get('RPC', 'Enabled', True)

        def showdata():
            return config().get('RPC', 'Show data', True)
    
    class proxies:
        def enabled():
            return config().get('Proxies', 'Enabled', False)

    class solver:
        def enabled():
            return config().get('Solver', 'Enabled', False)

        def apikey():
            return config().get('Solver', 'API Key', None)

        def service():
            return config().get('Solver', 'Service', None)
