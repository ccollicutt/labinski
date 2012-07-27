
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
syslog.syslog(syslog.LOG_ERR, 'novaapi omprted')


# Start the scheduler
sched = Scheduler()
#sched.add_jobstore(ShelveJobStore('/tmp/hackavcl_jobs'), 'file')
# http://stackoverflow.com/questions/10104682/advance-python-scheduler-and-sqlalchemyjobstore
sched.add_jobstore(SQLAlchemyJobStore(url=DATABASE, tablename='apscheduler_jobs'), 'default')

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

def check_instance(reservation):
	#stub
	return True

def warn_reservation_ending():
	# stub
	return True

def stop_instance(reservation):

	instance_id = reservation.instance_id
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
	reservation_length_in_seconds = 60*60*int(reservation_length)

	# Kill the instance at start_time + x hours
	stop_time = start_time + datetime.timedelta(seconds=reservation_length_in_seconds)

	# Warn time is stop_time - 5 minutes (or 300 seconds)
	warn_time = start_time + datetime.timedelta(seconds=reservation_length_in_seconds - 300)

	#
	# Create several jobs and assign job name into reservation object
	#

	job_name = 'student_' + student.name + '_class_' + reservation.class_id.name + '_reservation_id_' + str(reservation.id)

	# 1) Start the instance
	start_instance_job = sched.add_date_job(start_instance, start_time, \
		name=job_name + '_start', args=[reservation])

	reservation.start_instance_job = start_instance_job.name

	Notification(student=student, message='Instance for reservation ' + str(reservation.id) + ' will start at ' + str(start_time), status="INFO")


	# 2) Make sure the instance is in a good state
	check_instance_job = sched.add_date_job(check_instance, check_time, \
		name=job_name + '_check', args=[reservation])

	reservation.check_instance_job = check_instance_job.name

	Notification(student=student, message='Instance for reservation ' + str(reservation.id) + ' will be checked at ' + str(check_time), status="INFO")


	# 3) Setup a job to warn the user 5 minutes before the instance is destroyed
	warn_reservation_ending_job = sched.add_date_job(warn_reservation_ending, \
		warn_time, name=job_name + '_warn', args=[image.os_image_id])

	reservation.warn_reservation_ending_job = warn_reservation_ending_job.name

	Notification(student=student, message='User with reservation ' + str(reservation.id) + ' will be warned at ' + str(warn_time), status="INFO")


	# 4) Finally destroy the instance
	stop_instance_job = sched.add_date_job(stop_instance, stop_time, \
		name=job_name + '_stop', args=[reservation])

	reservation.stop_instance_job = stop_instance_job.name

	Notification(student=student, message='Instance for reservation ' + str(reservation.id) + ' will stop at ' + str(stop_time), status="INFO")


	session.commit()

	return True