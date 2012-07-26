from apscheduler.scheduler import Scheduler
from apscheduler.jobstores.shelve_store import ShelveJobStore
import datetime
from novaclient.v1_1 import client
from settings import *
from openstackrc import *
import time
import syslog
from model import Student, Reservation
from elixir import *

# Start the scheduler
sched = Scheduler()
sched.add_jobstore(ShelveJobStore('/tmp/hackavcl_jobs'), 'file')
sched.start()

# Create a nova connection
nova = client.Client(OS_USERNAME, OS_PASSWORD, OS_TENANT_NAME, OS_AUTH_URL, service_type="compute")

def is_resource_available(student, _class, image, start_time, reservation_length):
	# Stub
	
	#if len(nova.servers.list()) >= MAX_INSTANCES:
	#	syslog.syslog(syslog.LOG_ERR, 'Too many instances running')
	#	return False

	return True

def reservation_request(student,_class,image,start_time,reservation_length):

	# start_time is a datetime.datetime, might have to verify that
	# if time is now and it takes some time to get here now will have passed... :)

	resources = is_resource_available(student,_class,image,start_time,reservation_length)

	if resources:

		print "resources ok"

		# Create a reservation!

		reservation_name = student.name + '_' + _class.name + '_' + str(image.os_image_id)

		reservation = Reservation(student=student, \
			class_id=_class, \
			name=reservation_name)
		#	start_instance_job = start_instance_job.name, \
		#	stop_instance_job = stop_instance_job.name, \
		#	check_instance_job = check_instance_job.name, \
		#	warn_reservation_ending_job = warn_reservation_ending_job.name)

		if reservation:
			print "reservation seems ok"
			session.commit()
		else:
			return False
		
		# add 30 seconds onto start_time
		start_time = start_time + datetime.timedelta(seconds=30)

		# check instance at start time + 2 minutes
		check_time = start_time + datetime.timedelta(seconds=120)

		# use seconds instead of hours for stop time
		reservation_length_in_seconds = 60*60*reservation_length

		# kill the instance at start_time + x hours
		stop_time = start_time + datetime.timedelta(seconds=reservation_length_in_seconds)

		# Warn time is stop_time - 5 minutes (or 300 seconds)
		warn_time = start_time + datetime.timedelta(seconds=reservation_length_in_seconds - 300)

		#
		# Create each of the jobs and assign output into reservation object
		#

		start_instance_job = sched.add_date_job(start_instance, start_time, \
			name=reservation_name + '_start', args=[reservation])

		reservation.start_instance_job = start_instance_job.name

		check_instance_job = sched.add_date_job(check_instance, check_time, \
			name=reservation_name + '_check', args=[reservation])

		reservation.check_instance_job = check_instance_job.name

		warn_reservation_ending_job = sched.add_date_job(warn_reservation_ending, \
			check_time, name=reservation_name + '_warn', args=[image.os_image_id])

		reservation.warn_reservation_ending_job = warn_reservation_ending_job.name

		stop_instance_job = sched.add_date_job(stop_instance, stop_time, \
			name=reservation_name + '_stop', args=[reservation])

		reservation.stop_instance_job = stop_instance_job.name

		session.commit()

		print "jobs seem ok"
		return True

	# No resources
	return False


def start_instance(reservation):

    # Create a server
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

def stop_instance(instance_id):

	try:
		reservation = Reservation.query.filter_by(instance_id=unicode(instance_id)).one()
	except:
		reservation = None

	if reservation:
		reservation.delete()
		session.commit()

	# This doesn't seem to report success or failure back...
	nova.servers.delete(instance_id)
