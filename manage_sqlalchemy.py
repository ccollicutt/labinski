from model_sqlalchemy import *

if __name__ == "__main__":

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

	edmath = Class(name="EDMATH 401")

	session.add(edmath)

	session.commit()

	#
	# add reservation
	#

	reservation = Reservation(user_id=curtis.id, class_id=edmath.id)

	session.add(reservation)

	session.commit()

	#
	# Give curtis a class and a notification
	#

	curtis.classes.append(edmath)

	notification = Notification(user_id=curtis.id, message="test message for curtis", status="INFO")

	session.add(notification)

	session.commit()

	#
	# Add an image
	#

	IMAGE = "31cf939c-3be9-4fb4-9fb8-09a45b1d98ce"

	image = Image(name='Generic Linux', os_image_id=IMAGE)

	session.add(image)

	image.classes.append(edmath)

	session.commit()