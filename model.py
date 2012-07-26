# coding: utf-8

#XXX Apparently you're not suppsoed to import *?
#    - http://www.blog.pythonlibrary.org/2010/11/25/sqlalchemy-a-simple-tutorial-for-elixir/
from elixir import *
import datetime

class Student(Entity):
    name = Field(UnicodeText, primary_key=True)
    email = Field(UnicodeText, primary_key=True)
    reservations = OneToMany('Reservation', cascade="all,delete-orphan")
    classes = ManyToMany('Class')
    notifications = OneToMany('Notification', cascade="all,delete-orphan")
    is_admin = Field(Boolean, default=False)

class Reservation(Entity):
    student = ManyToOne('Student', required=True)
    class_id = ManyToOne('Class', required=True)
    image = ManyToOne('Image', required=True)
    instance_id = Field(UnicodeText)

    # These are the jobs created by reservation_request
    stop_instance_job = Field(UnicodeText)
    start_instance_job = Field(UnicodeText)
    warn_reservation_ending_job = Field(UnicodeText)
    check_instance_job = Field(UnicodeText)

    # This is for eventually natting...
    # forwarded_port(Integer)
    # If it's always one computer per student, then each reservation
    # can have a password
    # password

class Class(Entity):
    name = Field(Unicode(10), primary_key=True)
    images = ManyToMany('Image')
    students = ManyToMany('Student')
    reservations = OneToMany('Reservation', cascade="all,delete-orphan")

class Image(Entity):
    os_image_id = Field(UnicodeText, primary_key=True)
    name = Field(UnicodeText, primary_key=True)
    description = Field(UnicodeText, required=True) 
    flavor = ManyToOne('Flavor', required=True) 
    class_id = ManyToMany('Class')
    reservations = OneToMany('Reservation')
    image_type = ManyToOne('ImageType', required=True)
    # each image will have a username that the student will login with
    #user_name

class ImageType(Entity):
    """
    Eg. Windows, Linux...
    """
    name = Field(UnicodeText, required=True)
    # Prob should be an OSType
    os = Field(UnicodeText, required=True)
    services = OneToMany('Service')

class Service(Entity):
    port = Field(Integer, required=True)
    name = Field(UnicodeText, required=True)
    description = Field(UnicodeText)
    image_type = ManyToOne('ImageType')

class Flavor(Entity):
    os_id = Field(Integer, required=True)

class Notification(Entity):
    student = ManyToOne('Student')
    message = Field(UnicodeText, required=True)
    # Should maybe be an entity?
    status = Field(Unicode(10)) 
    time = Field(DateTime, default=datetime.datetime.now)   
