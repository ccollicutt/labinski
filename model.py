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
    student = ManyToOne('Student')
    class_id = ManyToOne('Class')
    name = Field(UnicodeText, primary_key=True)


class Class(Entity):
    name = Field(Unicode(10), primary_key=True)
    images = ManyToMany('Image')
    students = ManyToMany('Student')
    reservations = OneToMany('Reservation', cascade="all,delete-orphan")

class ImageType(Entity):
    """
    Eg. Windows, Linux...
    """
    name = Field(UnicodeText, required=True)

class Flavor(Entity):
    os_id = Field(Integer, required=True)

class Image(Entity):
    os_image_id = Field(UnicodeText, primary_key=True)
    name = Field(UnicodeText, primary_key=True)
    description = Field(UnicodeText, required=True) 
    flavor = ManyToOne('Flavor', required=True) 
    image_type = ManyToOne('ImageType', required=True)
    class_id = ManyToMany('Class')

class Notification(Entity):
    student = ManyToOne('Student')
    message = Field(UnicodeText, required=True)
    # Should maybe be an entity?
    status = Field(Unicode(10)) 
    time = Field(DateTime, default=datetime.datetime.now)   
