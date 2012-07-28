from model_sqlalchemy import *

if __name__ == "__main__":

	# Apparently have to do this here?
	# http://www.mail-archive.com/sqlalchemy@googlegroups.com/msg27358.html
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)

	# Create a session
	session = Session()

	user = User(name='curtis', email='curtis@collicutt.net')

	session.add(user)

	session.commit()

	curtis = session.query(User).filter_by(name='curtis').first()

	if curtis:
		print "user name is " + curtis.name
	else:
		print "no curtis object"


	reservation = Reservation(user_id=curtis.id)

	session.add(reservation)

	session.commit()

	edmath = Class(name="EDMATH 401")

	session.add(edmath)

	session.commit()

	curtis.classes.append(edmath)

	if reservation:
		print "created a reservation for curtis with id " + str(reservation.id)
	else:
		print "could not create reservation"