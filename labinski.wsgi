#import os
# Change working directory so relative paths (and template lookup) work again
#os.chdir(os.path.dirname(__file__))

import sys
<<<<<<< HEAD
import logging
sys.path.append('/usr/share/labinski/')
=======
sys.path.append('/vagrant/labinski/')
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823

import bottle
from labinski_sqlalchemy import app
from model_sqlalchemy import *


# A must for mod_wsgi enironments
<<<<<<< HEAD
bottle.TEMPLATE_PATH.insert(0,'/usr/share/labinski/views/')
=======
bottle.TEMPLATE_PATH.insert(0,'/vagrant/labinski/views/')
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823


Base.metadata.create_all(engine)

bottle.debug(True)
<<<<<<< HEAD
application = bottle.load_app('labinski_sqlalchemy:app')
=======
application = bottle.load_app('labinski_sqlalchemy:app')
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823
