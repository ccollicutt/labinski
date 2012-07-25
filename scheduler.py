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

sched = Scheduler()
sched.add_jobstore(ShelveJobStore('/tmp/hackavcl_jobs'), 'file')
sched.start()

nova = client.Client(OS_USERNAME, OS_PASSWORD, OS_TENANT_NAME, OS_AUTH_URL, service_type="compute")

def create_instance(student,reservation_length):

	if len(nova.servers.list()) >= MAX_INSTANCES:
		syslog.syslog(syslog.LOG_ERR, 'Too many instances running')
		return False
    
    # Create a server
	server = nova.servers.create(flavor=FLAVOR,image=IMAGE,name=NAME)
	if server:
		syslog.syslog(syslog.LOG_ERR, 'New server ID is ' + str(server.id))
		time.sleep(10)	
		syslog.syslog(syslog.LOG_ERR, 'about to set student reservation')
		session.commit()
		syslog.syslog(syslog.LOG_ERR, 'just set student reservation')
		syslog.syslog(syslog.LOG_ERR, 'Server IP address for ' + str(server.id) + ' is ' + server.addresses['private'][0]['addr'])
	else:
		syslog.syslog(syslog.LOG_ERR, 'Server creation failed')
		return False

	now = datetime.datetime.now()
	#later = now + datetime.timedelta(hours=reservation_length)
	# XXX FIXME XXX
	later = now + datetime.timedelta(seconds=30*int(reservation_length))
 	syslog.syslog(syslog.LOG_ERR, 'Server creation time for ' + str(server.id) + ' is ' + str(now))
 	syslog.syslog(syslog.LOG_ERR, 'Server destruction time for ' + str(server.id) + ' is ' + str(later))
	# Schedule the server for deletion later
	job = sched.add_date_job(kill_instance, later, name=server.id, args=[server.id])
	if job:
 		syslog.syslog(syslog.LOG_ERR, 'Kill job for server ' + str(server.id) + ' is ' + str(job))
 		reservation = Reservation(name=server.id)
 		student.reservations.append(reservation)
 		session.commit()
		return server
	else:
 		syslog.syslog(syslog.LOG_ERR, 'Server destruction job for ' + str(server.id) + ' failed')
		return False

#def kill_instance_job(instance_id):
#	kill_instance(instance_id)

def kill_instance(instance_id):

	try:
		reservation = Reservation.query.filter_by(name=instance_id).one()
	except:
		reservation = None

	if reservation:
		reservation.delete()
		session.commit()

	# This doesn't seem to report success or failure back...
	nova.servers.delete(instance_id)
