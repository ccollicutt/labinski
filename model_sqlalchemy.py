from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, Boolean, Sequence, UnicodeText, Unicode, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

DATABASE = 'postgresql://modtest:modtest@localhost/modtest'

Base = declarative_base()
engine = create_engine(DATABASE, echo=True)

#Session = sessionmaker(bind=engine)
# scoped_session is somehow a bit threadproof? Note flush and commit are false...
Session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))

# part of many to many for classes <=> users
classes_users_assoc = Table('classes_users', Base.metadata,
    Column('class_id', Integer, ForeignKey('classes.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
	name = Column(String(50))
	email = Column(String(50))
	# OneToMany parent -> child, user -> reservations
	reservations = relationship("Reservation", backref='user', cascade="all, delete, delete-orphan")
	# ManyToMany
	#h ttp://docs.sqlalchemy.org/en/rel_0_7/orm/tutorial.html#building-a-many-to-many-relationship
	classes = relationship('Class', secondary=classes_users_assoc, backref='users')


	#classes =
	#notifications =
	is_admin = Column(Boolean, default=False)

class Reservation(Base):
	__tablename__ = 'reservations'
	id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	#class_id = Column(Integer, ForeignKey('class.id'))

	#user = ManyToOne User
	#class_id = ManyToOne
	#image = ManyToOne image
	instance_id = Column(String(50))

	# These are the jobs created by reservation_request
	stop_instance_job = Column(UnicodeText)
	start_instance_job = Column(UnicodeText)
	warn_reservation_ending_job = Column(UnicodeText)
	check_instance_job = Column(UnicodeText)

class Class(Base):
	__tablename__ = 'classes'
	id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
	#user_id = Column(Integer, ForeignKey('user.id'))
	#reservations = relationship("Reservation", backref='user', cascade="all, delete, delete-orphan")

	name = Column(String(50))
	#images = ManyToMany('Image')
	#reservations = OneToMany('Reservation', cascade="all,delete-orphan")