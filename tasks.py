from celery import Celery
from novaapi import nova
from model import *
from settings import *
import datetime
from model import Notification

celery = Celery()
celery.config_from_object('celeryconfig')

def is_resource_available(student, _class, image, start_time, reservation_length):
	
	db = Session()

	if len(nova.servers.list()) >= MAX_INSTANCES:
		notification = Notification(user_id=student.id, \
			message='Too many instances running to start a new reservation', \
			status="ERROR")
		db.add(notification)
		db.commit()
		return False

	return True

@celery.task
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

@celery.task
def check_instance(reservation_id):
	#stub
	return True

@celery.task
def warn_reservation_ending(reservation_id):
	# stub
	return True

@celery.task
def stop_instance(reservation_id):

	db = Session()

	reservation = db.query(Reservation).filter_by(id=reservation_id).first()
	instance_id = reservation.instance_id

	db.delete(reservation)
	db.commit()

	# This doesn't seem to report success or failure back...
	try:
		nova.servers.delete(instance_id)
	except:
		return False

	return True

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

	# 1) Start the instance
	start_instance_job = start_instance.apply_async([reservation.id], eta=start_time)

	reservation.start_instance_job = start_instance_job.id

	notification = Notification(user_id=student.id, message='Instance for reservation ' + str(reservation.id) + ' will start at ' + str(start_time), status="INFO")
	db.add(notification)
	db.commit()

	# 2) Make sure the instance is in a good state
	check_instance_job = check_instance.apply_async([reservation.id], eta=check_time)

	reservation.check_instance_job = check_instance_job.id

	notification = Notification(user_id=student.id, message='Instance for reservation ' + str(reservation.id) + ' will be checked at ' + str(check_time), status="INFO")
	db.add(notification)
	db.commit()

	# 3) Setup a job to warn the user 5 minutes before the instance is destroyed
	warn_reservation_ending_job = warn_reservation_ending.apply_async([reservation.id], eta=warn_time)

	reservation.warn_reservation_ending_job = warn_reservation_ending_job.id

	notification = Notification(user_id=student.id, message='User with reservation ' + str(reservation.id) + ' will be warned at ' + str(warn_time), status="INFO")
	db.add(notification)
	db.commit()

	# 4) Finally destroy the instance
	#    - XXX FIX ME XXX Note this job needs the db to delete the reservation as well
	stop_instance_job = stop_instance.apply_async([reservation.id], eta=stop_time)

	reservation.stop_instance_job = stop_instance_job.id

	notification = Notification(user_id=student.id, message='Instance for reservation ' + str(reservation.id) + ' will stop at ' + str(stop_time), status="INFO")
	db.add(notification)
	db.commit()

	return True