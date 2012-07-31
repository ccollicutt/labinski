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
<<<<<<< HEAD
	_class = session.query(Class).filter_by(name='OPENSTACK 101').first()
	image = session.query(Image).filter_by(name='CentOS 6').first()

	reservation = Reservation(user_id=student.id, class_id=_class.id, image_id=image.id)
=======
	openstack_101 = session.query(Class).filter_by(name='OPENSTACK 101').first()
	cirrus = session.query(Image).filter_by(name='cirros-0.3.0-x86_64-uec').first()

	reservation = Reservation(user_id=student.id, class_id=openstack_101.id, image_id=cirrus.id)
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823
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
<<<<<<< HEAD

	users = ['curtis', 'barton']

	for u in users:
		user = User(name=u, email=u + '@doesntexist.com')
		session.add(user)
		session.commit()

=======
	user = User(name='curtis', email='curtis@collicutt.net')
	session.add(user)
	session.commit()
	curtis = session.query(User).filter_by(name='curtis').first()

	if curtis:
		print "user name is " + curtis.name
	else:
		print "no curtis object"
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823

	#
	# Add class
	# 
<<<<<<< HEAD
	_class = Class(name="OPENSTACK 101")
	session.add(_class)
=======
	edmath = Class(name="OPENSTACK 101")
	session.add(edmath)
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823
	session.commit()

	#
	# Give curtis a class and a notification
	#
<<<<<<< HEAD
	for u in users:
		user = session.query(User).filter_by(name=u).first()
		user.classes.append(_class)
		notification = Notification(user_id=user.id, message='test message for ' + user.name, status="INFO")
		session.add(notification)
		session.commit()
=======
	curtis.classes.append(edmath)
	notification = Notification(user_id=curtis.id, message="test message for curtis", status="INFO")
	session.add(notification)
	session.commit()
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823

	#
	# Add an imagetype and service
	#
	http = Service(name='http', port=80, description='the interewebs')
	session.add(http)
	session.commit()
	ssh = Service(name='ssh', port=22, description='the most secure network terminal')
	session.add(http)
	session.commit() 
<<<<<<< HEAD
	imagetype = ImageType(name='Centos 6 x86_64', services=[ssh], os='Linux' )
=======
	imagetype = ImageType(name='Minimal Linux', services=[ssh], os='Linux' )
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823
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
<<<<<<< HEAD
	IMAGE = "92f2689c-b0cc-40f5-829d-098190e617ab"
	image = Image(name='CentOS 6', description='This is CentOS', os_image_id=IMAGE, imagetype_id=imagetype.id, flavor_id=flavor.id)
	session.add(image)
	image.classes.append(_class)
=======
	IMAGE = "7a372cf5-e42b-40b1-b7af-d9e1aab14a4b"
	image = Image(name='cirros-0.3.0-x86_64-uec', description='A very small test linux image', os_image_id=IMAGE, imagetype_id=imagetype.id, flavor_id=flavor.id)
	session.add(image)
	image.classes.append(edmath)
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823
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
