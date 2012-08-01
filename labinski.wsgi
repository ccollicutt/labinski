#import os
# Change working directory so relative paths (and template lookup) work again
#os.chdir(os.path.dirname(__file__))

import sys
import logging
sys.path.append('/usr/share/labinski/')

from apscheduler.scheduler import Scheduler
#from apscheduler.jobstores.shelve_store import ShelveJobStore
from apscheduler.jobstores.sqlalchemy_store import SQLAlchemyJobStore

from settings import *

import bottle
from labinski_sqlalchemy import app as application
from model_sqlalchemy import *

#def main():

	# A must for mod_wsgi enironments
bottle.TEMPLATE_PATH.insert(0,'/usr/share/labinski/views/')

Base.metadata.create_all(engine)

# Start the scheduler
sched = Scheduler()
#sched.add_jobstore(ShelveJobStore('/tmp/hackavcl_jobs'), 'file')
# http://stackoverflow.com/questions/10104682/advance-python-scheduler-and-sqlalchemyjobstore
sched.add_jobstore(SQLAlchemyJobStore(url=JOBS_DATABASE, tablename='apscheduler_jobs'), 'default')
sched.start()

bottle.debug(True)

#if __name__ == '__main__':

try:
	#main()
	application = bottle.load_app('labinski_sqlalchemy:app')
finally:
	sched.shutdown()



