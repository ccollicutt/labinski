from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, Boolean, Sequence, UnicodeText, Unicode, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
# Need the db name
from settings import DATABASE

#DATABASE = 'postgresql://modtest:modtest@localhost/modtest'

Base = declarative_base()
#engine = create_engine(DATABASE, echo=True)
engine = create_engine(DATABASE, echo=False)


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
# classes <=> images
classes_images_assoc = Table('classes_images', Base.metadata,
    Column('class_id', Integer, ForeignKey('classes.id')),
    Column('image_id', Integer, ForeignKey('images.id'))
)
# imagetypes <=> services
imagetypes_services_assoc = Table('imagetypes_service', Base.metadata,
    Column('imagetype_id', Integer, ForeignKey('imagetypes.id')),
    Column('service_id', Integer, ForeignKey('services.id'))
)

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
	name = Column(String(50), nullable=False)
	email = Column(String(50))
	# OneToMany parent -> child, user -> reservations
	reservations = relationship("Reservation", backref='user', cascade="all, delete, delete-orphan")
	# ManyToMany
	# - http://docs.sqlalchemy.org/en/rel_0_7/orm/tutorial.html#building-a-many-to-many-relationship
	classes = relationship('Class', secondary=classes_users_assoc, backref='users')
	notifications = relationship('Notification', backref='users', cascade="all, delete, delete-orphan")
	is_admin = Column(Boolean, default=False)

class Reservation(Base):
	__tablename__ = 'reservations'
	id = Column(Integer, Sequence('reservation_id_seq'), primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	image_id = Column(Integer, ForeignKey('images.id'), nullable=False)
	class_id = Column(Integer, ForeignKey('classes.id'), nullable=False)
	# OpenStack instance id
	instance_id = Column(String(50))

	# These are the jobs created by reservation_request
	stop_instance_job = Column(UnicodeText)
	start_instance_job = Column(UnicodeText)
	warn_reservation_ending_job = Column(UnicodeText)
	check_instance_job = Column(UnicodeText)

class Class(Base):
	__tablename__ = 'classes'
	id = Column(Integer, Sequence('class_id_seq'), primary_key=True)
	name = Column(String(50), nullable=False)
	reservations = relationship("Reservation", backref='classes', cascade="all, delete, delete-orphan")

class Image(Base):
	__tablename__= 'images'
	id = Column(Integer, Sequence('image_id_seq'), primary_key=True)
	name = Column(String(50), nullable=False)
	description = Column(UnicodeText, nullable=False)
	imagetype_id = Column(Integer, ForeignKey('imagetypes.id'), nullable=False)
	# ManyToMany Images <=> Classes 
	# os = OpenStack
	os_image_id = Column(String(50), nullable=False)
	flavor_id = Column(Integer, ForeignKey('flavors.id'), nullable=False)
	classes = relationship('Class', secondary=classes_images_assoc, backref='images')
	reservations = relationship("Reservation", backref='images', cascade="all, delete, delete-orphan")


class Notification(Base):
	__tablename__ = 'notifications'
	id = Column(Integer, Sequence('notification_id_seq'), primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	message = Column(UnicodeText, nullable=False)
	status = Column(String(10), nullable=False)

class Service(Base):
	__tablename__ = 'services'
	id = Column(Integer, Sequence('service_id_seq'), primary_key=True)
	# Guess someday this might have to be a port range
	port = Column(Integer, nullable=False)
	name = Column(String(50), nullable=False)
	description = Column(UnicodeText)

class ImageType(Base):
	__tablename__ = 'imagetypes'
	id = Column(Integer, Sequence('imagetypes_id_seq'), primary_key=True)
	name = Column(String(50), nullable=False)
	# os = operating system
	os = Column(String(50), nullable=False)
	services = relationship('Service', secondary=imagetypes_services_assoc, backref='imagestypes')
	# An ImageType can have many images associated, but an Image can only have one ImageType
	images = relationship('Image', backref='imagetypes', cascade="all, delete, delete-orphan")

# OpenStack Flavor
class Flavor(Base):
	__tablename__ = 'flavors'
	id = Column(Integer, Sequence('flavors_id_seq'), primary_key=True)
	openstack_flavor_id = Column(Integer, nullable=False)
	images = relationship('Image', backref='flavors', cascade="all, delete, delete-orphan")

# OS
#class OS


