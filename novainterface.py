import re,glob,operator,string,sys
import novaclient
from novaclient.v1_1 import client
import scheduler
from scheduler import *
import os

def callnova(name, reservation_length):
 	student = Student.query.filter_by(name=unicode(name)).one()
	server = create_instance(student,reservation_length)
	#usrinfo = str(name)+'.'+ip_address+'.info'
	#cmd0 = 'echo Reservation Legnth : '+ str(reservation_length) + '> userinfo'
	#os.system(cmd0)

	return server
