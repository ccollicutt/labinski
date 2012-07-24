#!/usr/bin/python2.6 python

from bottle import route, run, template, get, post, request, static_file, error, Bottle
#import scheduler
from scheduler import *
from model import Student, Reservation, Class, Image
from modelapi import init_db
from settings import *

# Init the model database
init_db(DATABASE)

app = Bottle()

#XXX FIX ME XXXX
name = "curtis"


@app.route('/')
def login():

    student = Student.query.filter_by(name=unicode(name)).one()
    classes = student.classes

    return template('index', images=Image.query.all(), \
                    classes=classes)

@app.route('/reserve')
def reserve():

  student = Student.query.filter_by(name=unicode(name)).one()
  classes = student.classes

  return template('reserve', classes=classes)
   

@app.route('/reservations')
def reservations():
  student = Student.query.filter_by(name=unicode(name)).one()
  reservations = student.reservations
  return template('reservations', reservations=reservations)
  

@app.post('/reservation')
def reservation():
  reservation_time = request.forms.reservation_time
  reservation_image_name = request.forms.reservation_image_name
  reservation_length = request.forms.reservation_length

  student = Student.query.filter_by(name=unicode(name)).one()

  # is_valid_student(name)
  # is_valid_image(student)
  # is_valid_reservation_time(time)

  server = create_instance(student,4)

  return template('reservation', time=reservation_time, image_name=reservation_image_name, length=reservation_length)

@app.route('/connections')
def connections():

  student = Student.query.filter_by(name=unicode(name)).one()

  reservations = student.reservations

  servers = []

  for reservation in student.reservations:
    # reservation name = server id
    try:
      server = nova.servers.find(id=reservation.name)
    except:
      server= None
    if server:
      servers.append(server)

  return template('connections', servers=servers)

@app.route('/images')
def show_images():

  student = Student.query.filter_by(name=unicode(name)).one()
  classes = student.classes

  return template('show_images', classes=classes)


#
# Static 
#

@app.route('/bootstrap/css/<filename>')
def css_static(filename):
    return static_file(filename, root='/vagrant/hackavcl/bootstrap/css')

@app.route('/bootstrap/js/<filename>')
def js_static(filename):
    return static_file(filename, root='/vagrant/hackavcl/bootstrap/js')
