
import datetime
from novaclient.v1_1 import client
from settings import *
from openstackrc import *
import time
import syslog
from model import Student, Reservation, Notification
from elixir import *



# Create a nova connection
nova = client.Client(OS_USERNAME, OS_PASSWORD, OS_TENANT_NAME, OS_AUTH_URL, service_type="compute")

def is_resource_available(student, _class, image, start_time, reservation_length):
	# Stub
	
	#if len(nova.servers.list()) >= MAX_INSTANCES:
	#	syslog.syslog(syslog.LOG_ERR, 'Too many instances running')
	#	return False

	return True

def reservation_request(student,_class,image,start_time,reservation_length):

	resources = is_resource_available(student,_class,image,start_time,reservation_length)

	# Create an initial reservation to which we can add jobs and 
	# eventually the openstack instance_id
	reservation_name = student.name + '_' + _class.name + '_' + str(image.os_image_id)

	reservation = Reservation(student=student, \
		class_id=_class, \
		name=reservation_name, \
		image=image)

	if reservation:
		session.commit()
	else:
		return False

	if resources:
		add_reservation_jobs(reservation)
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
