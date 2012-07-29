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
	openstack_101 = session.query(Class).filter_by(name='OPENSTACK 101').first()
	cirrus = session.query(Image).filter_by(name='cirros-0.3.0-x86_64-uec').first()

	reservation = Reservation(user_id=student.id, class_id=openstack_101.id, image_id=cirrus.id)
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
	user = User(name='curtis', email='curtis@collicutt.net')
	session.add(user)
	session.commit()
	curtis = session.query(User).filter_by(name='curtis').first()

	if curtis:
		print "user name is " + curtis.name
	else:
		print "no curtis object"

	#
	# Add class
	# 
	edmath = Class(name="OPENSTACK 101")
	session.add(edmath)
	session.commit()

	#
	# Give curtis a class and a notification
	#
	curtis.classes.append(edmath)
	notification = Notification(user_id=curtis.id, message="test message for curtis", status="INFO")
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
	imagetype = ImageType(name='Minimal Linux', services=[ssh], os='Linux' )
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
	IMAGE = "7a372cf5-e42b-40b1-b7af-d9e1aab14a4b"
	image = Image(name='cirros-0.3.0-x86_64-uec', description='A very small test linux image', os_image_id=IMAGE, imagetype_id=imagetype.id, flavor_id=flavor.id)
	session.add(image)
	image.classes.append(edmath)
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
