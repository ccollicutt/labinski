#import os
# Change working directory so relative paths (and template lookup) work again
#os.chdir(os.path.dirname(__file__))

import sys
import logging
sys.path.append('/usr/share/labinski/')

import bottle
from labinski_sqlalchemy import app
from model_sqlalchemy import *


# A must for mod_wsgi enironments
bottle.TEMPLATE_PATH.insert(0,'/usr/share/labinski/views/')


Base.metadata.create_all(engine)

bottle.debug(True)
application = bottle.load_app('labinski_sqlalchemy:app')
