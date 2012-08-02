import sys
import logging
sys.path.append('/usr/share/labinski/')
from settings import *
import bottle
from labinski import app as application
from model import *

# A must for mod_wsgi enironments
bottle.TEMPLATE_PATH.insert(0,'/usr/share/labinski/views/')

Base.metadata.create_all(engine)
bottle.debug(True)

application = bottle.load_app('labinski:app')




