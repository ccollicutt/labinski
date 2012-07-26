import labinski
from model import Student, Class, Reservation, Image
from novaapi import *
import datetime
from time import sleep

try:
	nova_images = nova.images.list()
except:
	print "can't connect to nova"

for i in nova_images:
	print "image name is " + i.name

student = Student.query.filter_by(name=unicode('curtis')).first()

edmath = Class.query.filter_by(name=unicode('EDMATH 502')).first()

image = Image.query.filter_by(name=unicode('matlab')).first()

start_time = datetime.datetime.now()

reservation = reservation_request(student=student, _class=edmath, image=image, start_time=start_time, reservation_length=4)

#reservation = True

if reservation:
	print "success!"
else:
	print "failure!"

for r in student.reservations:
	print "1 ======================="
	print "r name: " + str(r.name)
	print "r start: " + str(r.start_instance_job)
	print "r check: " + str(r.check_instance_job)
	print "r warn: " + str(r.warn_reservation_ending_job)
	print "r stop: " + str(r.stop_instance_job)
	print "r instance: " + str(r.instance_id)

print "sleeping 62..."
sleep(62)

for r in student.reservations:
	print "2 ======================="
	print "r name: " + str(r.name)
	print "r start: " + str(r.start_instance_job)
	print "r check: " + str(r.check_instance_job)
	print "r warn: " + str(r.warn_reservation_ending_job)
	print "r stop: " + str(r.stop_instance_job)
	print "r instance: " + str(r.instance_id)
