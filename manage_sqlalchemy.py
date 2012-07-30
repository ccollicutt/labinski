#!/usr/bin/python

import sys
from model_sqlalchemy import *
from novaapi import *
from bottle import run
from settings import *

def ipython():
	from IPython.Shell import IPShellEmbed

	Base.metadata.create_all(engine)
	session = Session()

	student = session.query(User).filter_by(name='curtis').first()
	_class = session.query(Class).filter_by(name='OPENSTACK 101').first()
	image = session.query(Image).filter_by(name='CentOS 6').first()

	reservation = Reservation(user_id=student.id, class_id=_class.id, image_id=image.id)
	session.add(reservation)
	session.commit()

	ipshell = IPShellEmbed()

	ipshell() 

def init():

	# Apparently have to do this here?
	# http://www.mail-archive.com/sqlalchemy@googlegroups.com/msg27358.html
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)

	# Create a session
	session = Session()

	#
	# Add user
	#

	users = ['curtis', 'barton']

	for u in users:
		user = User(name=u, email=u + '@doesntexist.com')
		session.add(user)
		session.commit()


	#
	# Add class
	# 
	_class = Class(name="OPENSTACK 101")
	session.add(_class)
	session.commit()

	#
	# Give curtis a class and a notification
	#
	for u in users:
		user = session.query(User).filter_by(name=u).first()
		user.classes.append(_class)
		notification = Notification(user_id=user.id, message='test message for ' + user.name, status="INFO")
		session.add(notification)
		session.commit()

	#
	# Add an imagetype and service
	#
	http = Service(name='http', port=80, description='the interewebs')
	session.add(http)
	session.commit()
	ssh = Service(name='ssh', port=22, description='the most secure network terminal')
	session.add(http)
	session.commit() 
	imagetype = ImageType(name='Centos 6 x86_64', services=[ssh], os='Linux' )
	session.add(imagetype)
	session.commit()

	#
	# Add flavor
	#
	flavor = Flavor(openstack_flavor_id=1)
	session.add(flavor)
	session.commit()

	#
	# Add an image
	#
	IMAGE = "92f2689c-b0cc-40f5-829d-098190e617ab"
	image = Image(name='CentOS 6', description='This is CentOS', os_image_id=IMAGE, imagetype_id=imagetype.id, flavor_id=flavor.id)
	session.add(image)
	image.classes.append(_class)
	session.commit()

	#
	# add reservation
	#
	#reservation = Reservation(user_id=curtis.id, class_id=edmath.id, image_id=image.id)
	#session.add(reservation)
	#session.commit()

	# Finally
	session.commit()

if __name__ == "__main__":

    if len(sys.argv) == 2:
        if sys.argv[1] == 'init':
            init()
        if sys.argv[1] == 'ipython':
        	ipython()
