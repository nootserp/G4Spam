# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.logger import logger
from src.util.ui import ui
from src.util.files import files

class logonbrowser:
    def __init__(self):
        self.module = 'Log On Browser'
        self.logger = logger(self.module)
        self.ui = ui(self.module)

    def menu(self):
        self.ui.prep()
        tokens = files.gettokens()
        
        if not tokens:
            self.logger.log('No tokens found')
            return

        self.ui.createmenu([f'Token {i+1}: {self.ui.cut(token, 30, "...")}' for i, token in enumerate(tokens)])
        
        choice = self.ui.input('Select token to log in', int) - 1
        
        if choice < 0 or choice >= len(tokens):
            self.logger.log('Invalid choice')
            return

        selected_token = tokens[choice]
        
        # Create login script
        login_script = f"""
// Discord Token Login Script
// Paste this in the browser console on discord.com

(function() {{
    const token = "{selected_token}";
    
    function login(token) {{
        setInterval(() => {{
            document.body.appendChild(document.createElement('iframe')).contentWindow.localStorage.token = `"${{token}}"`;
        }}, 50);
        setTimeout(() => {{
            location.reload();
        }}, 2500);
    }}
    
    login(token);
}})();
"""
        
        # Save to file
        script_path = 'data/login_script.js'
        with open(script_path, 'w') as f:
            f.write(login_script)
        
        self.logger.log('Login script saved to data/login_script.js')
        self.logger.log('Instructions:')
        self.logger.log('1. Open discord.com in your browser')
        self.logger.log('2. Press F12 to open developer tools')
        self.logger.log('3. Go to Console tab')
        self.logger.log('4. Copy and paste the script from login_script.js')
        self.logger.log('5. Press Enter')
        
        # Open the file
        os.system(f'start {script_path}')