
from apscheduler.scheduler import Scheduler
from apscheduler.jobstores.shelve_store import ShelveJobStore
from model import Notification, Reservation, Student, Image

# Start the scheduler
sched = Scheduler()
sched.add_jobstore(ShelveJobStore('/tmp/hackavcl_jobs'), 'file')
sched.start()

def add_reservation_jobs(reservation, start_time, reservation_length, image):

	# Add 30 seconds onto start_time
	start_time = start_time + datetime.timedelta(seconds=30)

	# Check instance at start time + 2 minutes
	check_time = start_time + datetime.timedelta(seconds=120)

	# Use seconds instead of hours for stop time (don't think minutes are an option)
	reservation_length_in_seconds = 60*60*reservation_length

	# Kill the instance at start_time + x hours
	stop_time = start_time + datetime.timedelta(seconds=reservation_length_in_seconds)

	# Warn time is stop_time - 5 minutes (or 300 seconds)
	warn_time = start_time + datetime.timedelta(seconds=reservation_length_in_seconds - 300)

	#
	# Create several jobs and assign job name into reservation object
	#

	# 1) Start the instance
	start_instance_job = sched.add_date_job(start_instance, start_time, \
		name=reservation_name + '_start', args=[reservation])

	reservation.start_instance_job = start_instance_job.name

	Notification(student, 'start_instance_job ' \
		+ start_instance_job.name \
		+ ' added for time ' + str(start_time))

	# 2) Make sure the instance is in a good state
	check_instance_job = sched.add_date_job(check_instance, check_time, \
		name=reservation_name + '_check', args=[reservation])

	reservation.check_instance_job = check_instance_job.name

	Notification(student, 'check_instance_job ' \
	    + check_instance_job.name \
	    + ' added for time ' +  str(check_time))

	# 3) Setup a job to warn the user 5 minutes before the instance is destroyed
	warn_reservation_ending_job = sched.add_date_job(warn_reservation_ending, \
		warn_time, name=reservation_name + '_warn', args=[image.os_image_id])

	reservation.warn_reservation_ending_job = warn_reservation_ending_job.name

	Notification(student, 'warn_reservation_ending_job ' \
	    + warn_reservation_ending_job.name \
		+ ' added for time ' + str(warn_time))

	# 4) Finally destroy the instance
	stop_instance_job = sched.add_date_job(stop_instance, stop_time, \
		name=reservation_name + '_stop', args=[reservation])

	reservation.stop_instance_job = stop_instance_job.name

	Notification(student, 'stop_instance_job ' \
		+ stop_instance_job.name \
		+ ' added for time ' + str(stop_time))

	session.commit()

	return True