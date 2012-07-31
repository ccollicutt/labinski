
#import datetime
from novaclient.v1_1 import client
from settings import *
from openstackrc import *
import time
import syslog
from model_sqlalchemy import *
from apscheduler.scheduler import Scheduler
#from apscheduler.jobstores.shelve_store import ShelveJobStore
from apscheduler.jobstores.sqlalchemy_store import SQLAlchemyJobStore
import logging
import datetime
from elixir import *

# Create a nova connection
nova = client.Client(OS_USERNAME, OS_PASSWORD, OS_TENANT_NAME, OS_AUTH_URL, service_type="compute")

# Start the scheduler
sched = Scheduler()
#sched.add_jobstore(ShelveJobStore('/tmp/hackavcl_jobs'), 'file')
# http://stackoverflow.com/questions/10104682/advance-python-scheduler-and-sqlalchemyjobstore
sched.add_jobstore(SQLAlchemyJobStore(url=JOBS_DATABASE, tablename='apscheduler_jobs'), 'default')
sched.start()

def is_resource_available(student, _class, image, start_time, reservation_length):
	# Stub
	
	if len(nova.servers.list()) >= MAX_INSTANCES:
		logging.debug('Nova instances is less than MAX_INSTANCES')
		return False

	return True

def start_instance(reservation_id):

	db = Session()
	reservation = db.query(Reservation).filter_by(id=reservation_id).first()
	# Get the db for this session
	#db = Session.object_session(reservation)


    # Create a server
    # XXX FIX ME XXX IMAGE should be reservation.image_id etc
	server = nova.servers.create(flavor=reservation.images.flavors.openstack_flavor_id,
								 image=reservation.images.os_image_id,
								 name=reservation.images.name)

	if server:
		reservation.instance_id = server.id
		db.commit()
		return True
	else:
		return False

def check_instance(reservation):
	#stub
	return True

def warn_reservation_ending():
	# stub
	return True

def stop_instance(reservation):

	db = Session()

	instance_id = reservation.instance_id
	# XXX FIX ME XXX
	#db.delete(reservation)
	#db.commit()

	# This doesn't seem to report success or failure back...
	nova.servers.delete(instance_id)

def add_reservation_jobs(student, reservation, start_time, reservation_length, image, db):

	# Add 30 seconds onto start_time
	start_time = start_time + datetime.timedelta(seconds=30)

	# Check instance at start time + 2 minutes
	check_time = start_time + datetime.timedelta(seconds=120)

	# Use seconds instead of hours for stop time (don't think minutes are an option)
	reservation_length_in_seconds = 60*60*int(reservation_length)

	# Kill the instance at start_time + x hours
	stop_time = start_time + datetime.timedelta(seconds=reservation_length_in_seconds)

	# Warn time is stop_time - 5 minutes (or 300 seconds)
	warn_time = start_time + datetime.timedelta(seconds=reservation_length_in_seconds - 300)

	#
	# Create several jobs and assign job name into reservation object
	#

	job_name = 'student_' + student.name + '_class_' + reservation.classes.name + '_reservation_id_' + str(reservation.id)

	# 1) Start the instance
	start_instance_job = sched.add_date_job(start_instance, start_time, \
		name=job_name + '_start', args=[reservation.id])

	reservation.start_instance_job = start_instance_job.name

	notification = Notification(user_id=student.id, message='Instance for reservation ' + str(reservation.id) + ' will start at ' + str(start_time), status="INFO")
	db.add(notification)
	db.commit()

	# 2) Make sure the instance is in a good state
	check_instance_job = sched.add_date_job(check_instance, check_time, \
		name=job_name + '_check', args=[reservation])

	reservation.check_instance_job = check_instance_job.name

	notification = Notification(user_id=student.id, message='Instance for reservation ' + str(reservation.id) + ' will be checked at ' + str(check_time), status="INFO")
	db.add(notification)
	db.commit()

	# 3) Setup a job to warn the user 5 minutes before the instance is destroyed
	warn_reservation_ending_job = sched.add_date_job(warn_reservation_ending, \
		warn_time, name=job_name + '_warn', args=[image.os_image_id])

	reservation.warn_reservation_ending_job = warn_reservation_ending_job.name

	notification = Notification(user_id=student.id, message='User with reservation ' + str(reservation.id) + ' will be warned at ' + str(warn_time), status="INFO")
	db.add(notification)
	db.commit()

	# 4) Finally destroy the instance
	#    - XXX FIX ME XXX Note this job needs the db to delete the reservation as well
	stop_instance_job = sched.add_date_job(stop_instance, stop_time, \
		name=job_name + '_stop', args=[reservation])

	reservation.stop_instance_job = stop_instance_job.name

	notification = Notification(user_id=student.id, message='Instance for reservation ' + str(reservation.id) + ' will stop at ' + str(stop_time), status="INFO")
	db.add(notification)
	db.commit()

	return True