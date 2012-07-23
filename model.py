# coding: utf-8

#XXX Apparently you're not suppsoed to import *?
#    - http://www.blog.pythonlibrary.org/2010/11/25/sqlalchemy-a-simple-tutorial-for-elixir/
from elixir import *

class Student(Entity):
    name = Field(UnicodeText, primary_key=True)
    email = Field(UnicodeText, primary_key=True)
    reservation = Field(UnicodeText)
    #reservation = ManyToOne('Reservation')
    # classes

class Reservation(Entity):
    os_instance_id = Field(UnicodeText, primary_key=True)
    #start_time = Field(UnicodeText, primary_key=True)
    #stop_time = Field(UnicodeText, primary_key=True)
    #kill_job = Field(UnicodeText, primary_key=True)
    #notify_job = Field(UnicodeText, primary_key=True)

class Class(Entity):
    name = Field(Unicode(10), primary_key=True)
    images = OneToMany('Image', cascade='all, delete-orphan')
    # students

class ImageType(Entity):
    name = Field(UnicodeText, required=True)

class Flavor(Entity):
    os_id = Field(Integer, required=True)

class Image(Entity):
    os_image_id = Field(UnicodeText, primary_key=True)
    name = Field(UnicodeText, primary_key=True)
    description = Field(UnicodeText, required=True) 
    flavor = ManyToOne('Flavor', required=True) 
    image_type = ManyToOne('ImageType', required=True)
    class_id = ManyToOne('Class')

