from apscheduler.scheduler import Scheduler
import datetime
from novaclient.v1_1 import client
from settings import *
from openstackrc import *
import time
import syslog

sched = Scheduler()
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
		student.reservation = unicode(server.id)
		session.commit()
		syslog.syslog(syslog.LOG_ERR, 'just set student reservation')
		#ips = server.addresses 
		#ip = ips['private'][0]['addr']
		syslog.syslog(syslog.LOG_ERR, 'Server IP address for ' + str(server.id) + ' is ' + server.addresses['private'][0]['addr'])
	else:
		syslog.syslog(syslog.LOG_ERR, 'Server creation failed')
		return False

	now = datetime.datetime.now()
	#later = now + datetime.timedelta(hours=reservation_length)
	# XXX FIXME XXX
	later = now + datetime.timedelta(seconds=60*int(reservation_length))
 	syslog.syslog(syslog.LOG_ERR, 'Server creation time for ' + str(server.id) + ' is ' + str(now))
 	syslog.syslog(syslog.LOG_ERR, 'Server destruction time for ' + str(server.id) + ' is ' + str(later))
	# Schedule the server for deletion later
	job = sched.add_date_job(kill_instance, later, [server.id])
	if job:
 		syslog.syslog(syslog.LOG_ERR, 'Kill job for server ' + str(server.id) + ' is ' + str(job))
		return server
	else:
 		syslog.syslog(syslog.LOG_ERR, 'Server destruction job for ' + str(server.id) + ' failed')
		return False

def kill_instance(instance_id):
 	#syslog.syslog(syslog.LOG_ERR, 'Server ' + str(server.id) + ' is about to be destroyed')
	# Find the student by the reservation server.id
	student = Student.query.filter_by(reservation=unicode(instance_id)).one()
	# And set it to none
	if student:
        	student.reservation = None
		session.commit()
	nova.servers.delete(instance_id)
	
