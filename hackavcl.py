#!/usr/bin/python2.6 python

import bottle
from bottle import route, run, template, get, post, request, static_file, error, Bottle, redirect
#import scheduler
from scheduler import *
from model import Student, Reservation, Class, Image
from modelapi import init_db
from settings import *
from beaker.middleware import SessionMiddleware
from os import environ


# Init the model database
init_db(DATABASE)

#app = Bottle.())

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': '/tmp',
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)


@bottle.route('/')
def slash():

    try:
      session = environ['beaker.session']
    except:
      redirect('/login')

    # Check to see if a value is in the session
    if not 'logged_in' in session:
        redirect('/login')

    student = Student.query.filter_by(name=unicode(name)).first()
    classes = student.classes

    return template('index', images=Image.query.all(), \
                    classes=classes)


@bottle.post('/login')
def login():

    name = request.forms.name
    password = request.forms.password
    #user = Session.query(User).filter_by(name=name,
    #                                         password=password).first()

    student = Student.query.filter_by(name=unicode(name)).first()

    if student:
        session['logged_in'] = True
        #session.save()
    else:
        error_msg = 'username ' + name + ' does not exist'
        return template('login', error_msg=error_msg)

    return template('login', error_msg=error_msg)

@bottle.route('/login')
def login():
    return template('login')

@bottle.route('/reserve')
def reserve():

  student = Student.query.filter_by(name=unicode(name)).one()
  classes = student.classes

  return template('reserve', classes=classes)
   

@bottle.route('/reservations')
def reservations():
  student = Student.query.filter_by(name=unicode(name)).one()
  reservations = student.reservations
  return template('reservations', reservations=reservations)
  

@bottle.post('/reservation')
def reservation():
  reservation_time = request.forms.reservation_time
  reservation_image_name = request.forms.reservation_image_name
  reservation_length = request.forms.reservation_length

  student = Student.query.filter_by(name=unicode(name)).one()

  # is_valid_student(name)
  # is_valid_image(student)
  # is_valid_reservation_time(time)

  server = create_instance(student,4)

  #return template('reservation', time=reservation_time, image_name=reservation_image_name, length=reservation_length)
  return redirect('/connections')

@bottle.route('/connections')
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

@bottle.route('/images')
def show_images():

  student = Student.query.filter_by(name=unicode(name)).one()
  classes = student.classes

  return template('show_images', classes=classes)


#
# Static 
#

@bottle.route('/bootstrap/css/<filename>')
def css_static(filename):
    return static_file(filename, root='/vagrant/hackavcl/bootstrap/css')

@bottle.route('/bootstrap/js/<filename>')
def js_static(filename):
    return static_file(filename, root='/vagrant/hackavcl/bootstrap/js')
