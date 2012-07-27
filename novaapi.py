
#import datetime
from novaclient.v1_1 import client
from settings import *
from openstackrc import *
import time
import syslog
from model import Student, Reservation, Notification
from apscheduler.scheduler import Scheduler
#from apscheduler.jobstores.shelve_store import ShelveJobStore
from apscheduler.jobstores.sqlalchemy_store import SQLAlchemyJobStore

import datetime
from elixir import *

# Create a nova connection
nova = client.Client(OS_USERNAME, OS_PASSWORD, OS_TENANT_NAME, OS_AUTH_URL, service_type="compute")

# Start the scheduler
sched = Scheduler()
#sched.add_jobstore(ShelveJobStore('/tmp/hackavcl_jobs'), 'file')
# http://stackoverflow.com/questions/10104682/advance-python-scheduler-and-sqlalchemyjobstore
sched.add_jobstore(SQLAlchemyJobStore(url=DATABASE, tablename='jobs'), 'default')

sched.start()

def is_resource_available(student, _class, image, start_time, reservation_length):
	# Stub
	
	#if len(nova.servers.list()) >= MAX_INSTANCES:
	#	syslog.syslog(syslog.LOG_ERR, 'Too many instances running')
	#	return False

	return True

def reservation_request(student,_class,image,start_time,reservation_length):

	resources = is_resource_available(student,_class,image,start_time,reservation_length)

	reservation = Reservation(student=student, \
		class_id=_class, \
		image=image)

	if reservation:
		session.commit()
	else:
		return False

	if resources:
		add_reservation_jobs(student, reservation, start_time, reservation_length, image )
		return True
	else:
		reservation.delete()
		session.commit()

	# No resources
	return False

def start_instance(reservation):

    # Create a server
    # XXX FIX ME XXX IMAGE should be reservation.image_id etc
	server = nova.servers.create(flavor=FLAVOR,image=IMAGE,name=NAME)

	if server:
		reservation.instance_id = server.id
		session.commit()
		return True
	else:
		return False

def check_instance():
	#stub
	return True

def warn_reservation_ending():
	# stub
	return True

def stop_instance(reservation):

	reservation.delete()
	session.commit()

	# This doesn't seem to report success or failure back...
	nova.servers.delete(instance_id)

def add_reservation_jobs(student, reservation, start_time, reservation_length, image):

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

	reservation_name = student.name + '_' + reservation.class_id.name + '_' + reservation.image.os_image_id

	# 1) Start the instance
	start_instance_job = sched.add_date_job(start_instance, start_time, \
		name=reservation_name + '_start', args=[reservation])

	reservation.start_instance_job = start_instance_job.name

	Notification(student=student, message='start_instance_job ' \
		+ start_instance_job.name \
		+ ' added for time ' + str(start_time))

	# 2) Make sure the instance is in a good state
	check_instance_job = sched.add_date_job(check_instance, check_time, \
		name=reservation_name + '_check', args=[reservation])

	reservation.check_instance_job = check_instance_job.name

	Notification(student=student, message='check_instance_job ' \
	    + check_instance_job.name \
	    + ' added for time ' +  str(check_time))

	# 3) Setup a job to warn the user 5 minutes before the instance is destroyed
	warn_reservation_ending_job = sched.add_date_job(warn_reservation_ending, \
		warn_time, name=reservation_name + '_warn', args=[image.os_image_id])

	reservation.warn_reservation_ending_job = warn_reservation_ending_job.name

	Notification(student=student, message='warn_reservation_ending_job ' \
	    + warn_reservation_ending_job.name \
		+ ' added for time ' + str(warn_time))

	# 4) Finally destroy the instance
	stop_instance_job = sched.add_date_job(stop_instance, stop_time, \
		name=reservation_name + '_stop', args=[reservation])

	reservation.stop_instance_job = stop_instance_job.name

	Notification(student=student, message='stop_instance_job ' \
		+ stop_instance_job.name \
		+ ' added for time ' + str(stop_time))

	session.commit()

	return True