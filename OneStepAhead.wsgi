#!/var/www/html/OneStepAhead/linuxVenv/bin/env python3

activate_this = '/var/www/html/OneStepAhead/OneStepAhead/linuxVenv/bin/activate_this.py'
with open(activate_this) as file_:
	exec(file_.read(), dict(__file__=activate_this))
	
import sys
sys.path.insert(0, '/var/www/html/OneStepAhead/OneStepAhead')

from app import create_app
application = create_app(testing=False)
