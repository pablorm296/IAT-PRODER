activate_this = '/var/www/pabloreyes/IAT/src/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
sys.path.insert(0, '/var/www/pabloreyes/IAT/api')
from iatApi import app as application  # pylint: disable=import-error
