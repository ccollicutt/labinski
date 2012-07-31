from apscheduler.scheduler import Scheduler
from apscheduler.jobstores.sqlalchemy_store import SQLAlchemyJobStore
import datetime

JOBS_DATABASE = "postgresql://test_jobs:test_jobs@localhost/test_jobs"

# Start the scheduler
sched = Scheduler()
sched.add_jobstore(SQLAlchemyJobStore(url=JOBS_DATABASE, tablename='apscheduler_jobs'), 'default')
sched.start()

def print_reservation_id(reservation_id):
	print "====> Reservation id is " + str(reservation_id)


if __name__ == '__main__':
	 
	now = datetime.datetime.now()
	start_time =  now + datetime.timedelta(seconds=3)

	print "====> now is " + str(now)
	print "====> start_time is " + str(start_time)

	reservation_id = 1

	job_name = "print_reservation_id_" + str(reservation_id)

	start_instance_job = sched.add_date_job(print_reservation_id, start_time, \
		name=job_name + '_start', args=[reservation_id])

	print "====> Reservation id should print in 3 seconds..."
