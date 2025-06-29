# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.logger import logger
from src.util.ui import ui
ui = ui('Auto Update')

class autoupdate:
    def __init__(self):
        self.logger = logger('Auto Update')
        self.downloadurl = None
        self.releasedata = None

    def getlatestrelease(self):
        try:
            self.logger.log('Checking for updates')
            r = requests.get('https://api.github.com/repos/R3CI/G4Spam/releases/latest')
            if r.status_code == 200:
                self.releasedata = r.json()
                return True
            else:
                self.logger.error('Failed to check for updates', r.text)
                return False
        except Exception as e:
            self.logger.error('Failed to autoupdate', e)
            return False

    def downloadlatestrelease(self):
        try:
            self.logger.log('Downloading the update')
            r = requests.get(self.downloadurl)
            if r.status_code == 200:
                self.logger.log('Downloading is complete')
                return r.content
            else:
                self.logger.error('Failed to download update', r.text)
                return None
        except Exception as e:
            self.logger.error('Failed to download update', e)
            return None

    def extractzip(self, zipdata):
        try:
            self.logger.log('Extracting the files')
            tempdir = Path(tempfile.mkdtemp())
            zippath = tempdir / 'G4Spam-Update.zip'
            
            with open(zippath, 'wb') as f:
                f.write(zipdata)
            
            with zipfile.ZipFile(zippath, 'r') as zipf:
                zipf.extractall(tempdir)
            
            for item in tempdir.iterdir():
                if item.is_dir() and item.name.startswith('R3CI-G4Spam'):
                    self.logger.log(f'Update extracted to {item}')
                    return item
            
            self.logger.error('Failed to extract update')
            return None
        except Exception as e:
            self.logger.error('Failed to extract update', e)
            return None

    def syncfiles(self, sourcedir):
        try:
            self.logger.log('Syncing files')
            currentscript = Path(__file__).resolve()
            scriptupdated = False
            filecount = 0
            
            for root, dirs, files in os.walk(sourcedir):
                for file in files:
                    sourcefile = Path(root) / file
                    relpath = sourcefile.relative_to(sourcedir)
                    
                    targetfile = Path('.') / relpath
                    targetfile.parent.mkdir(parents=True, exist_ok=True)
                    
                    if targetfile.resolve() == currentscript:
                        scriptupdated = True
                        newscript = currentscript.with_suffix('.new')
                        shutil.copy2(sourcefile, newscript)
                        self.logger.log(f'Updated script {relpath}')
                    else:
                        shutil.copy2(sourcefile, targetfile)
                        self.logger.log(f'Updated file {relpath}')
                    
                    filecount += 1

            self.logger.log(f'Synced {filecount} files')

            if scriptupdated:
                self.updatescript()
            return True
        except Exception as e:
            self.logger.error('Failed to sync files', e)
            return False

    def updatescript(self):
        try:
            self.logger.log('Updating script')
            currentscript = Path(__file__).resolve()
            newscript = currentscript.with_suffix('.new')
            
            if newscript.exists():
                shutil.move(str(newscript), str(currentscript))
                os.chmod(currentscript, 0o755)
                self.logger.log('Updated script, restarting...')
                self.restartscript()
        except Exception as e:
            self.logger.error('Failed to update script', e)

    def restartscript(self):
        try:
            python = sys.executable
            script = Path(__file__).resolve()
            os.execv(python, [python, str(script)])
        except Exception as e:
            self.logger.error('Failed to restart script', e)

    def update(self):
        try:
            if not self.getlatestrelease():
                return False

            if not self.releasedata:
                self.logger.error('Failed to get release data')
                return False
            
            latestversion = self.releasedata.get('tag_name', '').lstrip('v')
            
            if not latestversion:
                self.logger.error('Could not determine latest version')
                return False
            
            if latestversion == version:
                self.logger.log(f'Already on latest version: {version}')
                return False
            
            tagname = self.releasedata.get('tag_name', 'Unk')
            releasename = self.releasedata.get('name', 'Unk')
            body = self.releasedata.get('body', 'No release notes')
            publishdate = self.releasedata.get('published_at', 'Unk')
            self.downloadurl = self.releasedata.get('zipball_url')

            self.logger.log('Update info')
            self.logger.log(f'Updating from {version} to {tagname}')
            self.logger.log(f'Release name {releasename}')
            self.logger.log(f'Published {publishdate}')
            self.logger.log('Release notes')
            self.logger.log(body)
            
            choice = ui.input('Update', bool)
            if not choice:
                self.logger.log('Update cancelled by user')
                return False
        
            if not self.downloadurl:
                self.logger.error('Failed to get download url')
                return False
            
            zipdata = self.downloadlatestrelease()
            if not zipdata:
                return False
            
            sourcedir = self.extractzip(zipdata)
            if not sourcedir:
                return False
            
            try:
                success = self.syncfiles(sourcedir)
                if success:
                    self.logger.log('Update completed successfully')
                else:
                    self.logger.error('Update failed during sync')
                return success
            finally:
                if sourcedir and sourcedir.parent.exists():
                    self.logger.log(f'Cleaning up {sourcedir.parent}')
                    shutil.rmtree(sourcedir.parent)
                    
        except Exception as e:
            self.logger.error('Failed to update', e)
            return False