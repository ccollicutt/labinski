import labinski
from model import Student, Class, Reservation, Image
from novaapi import *
import datetime
from time import sleep

try:
	nova_images = nova.images.list()
except:
	print "can't connect to nova"

print "Nova Images"
print "==========="
print ""
for i in nova_images:
	print "    image name is " + i.name

print "=> Getting student..."
student = Student.query.filter_by(name=unicode('curtis')).first()

print "=> Getting class..."
edmath = Class.query.filter_by(name=unicode('EDMATH 502')).first()

print "=> Getting image..."
image = Image.query.filter_by(name=unicode('matlab')).first()

start_time = datetime.datetime.now()

print "=> Setting reservation...."
reservation = reservation_request(student=student, _class=edmath, image=image, start_time=start_time, reservation_length=1)

#reservation = True

if reservation:
	print "    ...success!"
else:
	print "    ....failure!"


print "=> Printing initial job values"
for r in student.reservations:
	print "    r id " + str(r.id)
	print "    r start: " + str(r.start_instance_job)
	print "    r check: " + str(r.check_instance_job)
	print "    r warn: " + str(r.warn_reservation_ending_job)
	print "    r stop: " + str(r.stop_instance_job)
	print "    r instance: " + str(r.instance_id)

print "=> sleeping 62 seconds to wait for instance_id of server..."
sleep(62)

print "=> Printing job values after intance creation..."
for r in student.reservations:
	print "    r id " + str(r.id)
	print "    r start: " + str(r.start_instance_job)
	print "    r check: " + str(r.check_instance_job)
	print "    r warn: " + str(r.warn_reservation_ending_job)
	print "    r stop: " + str(r.stop_instance_job)
	print "    r instance: " + str(r.instance_id)

print "=> Scheduled Jobs"
sched.print_jobs()
