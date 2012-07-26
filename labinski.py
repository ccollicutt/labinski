#!/usr/bin/python2.6 python
import bottle
from bottle import route, run, template, get, post, request, static_file, error, Bottle, redirect, abort
#import scheduler
from scheduler import *
from model import Student, Reservation, Class, Image
from modelapi import init_db
from settings import *
from beaker.middleware import SessionMiddleware
from os import environ

# Init the model database
init_db(DATABASE)

#
# Beaker middleware
#

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 600,
    'session.data_dir': '/tmp',
    'session.auto': True
}

app = SessionMiddleware(bottle.app(), session_opts)

#
# Functions
#

def check_login(beaker_session):
  
  if not 'logged_in' in beaker_session:
    abort(401, "Not logged in")

  name = beaker_session['name']

  student = Student.query.filter_by(name=unicode(name)).first()

  if student:
    return student

  return None

#
# Routes
# 

@bottle.route('/')
def slash():

  try:
    beaker_session = request.environ['beaker.session']
  except:
    redirect('/login')

  try:
    name = beaker_session['name']
  except:
    redirect('/login')

  student = check_login(beaker_session)

  if student:
    classes = student.classes
  else:
    abort(401, "No student object")

  return template('index', images=Image.query.all(), \
                    classes=classes)

@bottle.post('/login')
def login():

  name = request.forms.name
  password = request.forms.password

  try:
    student = Student.query.filter_by(name=unicode(name)).first()
  except:
    abort(401, "No student object in login")

  if student:
    beaker_session = request.environ['beaker.session']
    beaker_session['logged_in'] = True
    beaker_session['name'] = name
    redirect('/')
  else:
    error_msg = 'username or password not valid'
    return template('login', error_msg=error_msg)

  error_msg = 'Failed to find student'
  return template('login', error_msg=error_msg)

@bottle.route('/login')
def login():
  return template('login')

@bottle.route('/logout')
def logout():

  try:
    beaker_session = request.environ['beaker.session']
    student = check_login(beaker_session)
  except:
    redirect('/login')

  request.environ['beaker.session'].delete()
  redirect('/login')

@bottle.route('/reserve')
def reserve():

  try:
    beaker_session = request.environ['beaker.session']
  except:
    abort(401, "No session")

  try:
    name = beaker_session['name']
  except:
    abort(401, "No session name")

  student = check_login(beaker_session)

  if student:
    classes = student.classes
  else:
    abort(401, "No student object")

  return template('reserve', classes=classes)
   
@bottle.route('/reservations')
def reservations():
  try:
    beaker_session = request.environ['beaker.session']
  except:
    abort(401, "No session")

  try:
    name = beaker_session['name']
  except:
    abort(401, "No session name")

  student = check_login(beaker_session)

  if student:
    reservations = student.reservations
  else:
    abort(401, "No student object")

  return template('reservations', reservations=reservations)
  
@bottle.post('/reservation')
def reservation():

  try:
    beaker_session = request.environ['beaker.session']
  except:
    abort(401, "No session")

  try:
    name = beaker_session['name']
  except:
    abort(401, "No session name")

  student = check_login(beaker_session)

  try:
    reservation_time = request.forms.reservation_time
    reservation_image_name = request.forms.reservation_image_name
    reservation_length = request.forms.reservation_length
  except:
    abort(401, "Incomplete reservation post data")


  # is_valid_student(name)
  # is_valid_image(student)
  # is_valid_reservation_time(time)

  server = create_instance(student,4)

  #return template('reservation', time=reservation_time, image_name=reservation_image_name, length=reservation_length)
  return redirect('/connections')

@bottle.route('/connections')
def connections():

  try:
    beaker_session = request.environ['beaker.session']
  except:
    abort(401, "No session")

  try:
    name = beaker_session['name']
  except:
    abort(401, "No session name")

  student = check_login(beaker_session)

  if student:
    reservations = student.reservations
  else:
    abort(401, "No student object")

  servers = []

  for reservation in reservations:
    # reservation name = server id
    try:
      server = nova.servers.find(id=reservation.name)
    except:
      server = None
    if server:
      servers.append(server)

  return template('connections', servers=servers)

@bottle.route('/images')
def show_images():

  try:
    beaker_session = request.environ['beaker.session']
  except:
    abort(401, "No session")

  try:
    name = beaker_session['name']
  except:
    abort(401, "No session name")

  student = check_login(beaker_session)

  if student:
    classes = student.classes
  else:
    abort(401, "No student object")

  return template('show_images', classes=classes, name=student.name)

#
# Static 
#

@bottle.route('/bootstrap/css/<filename>')
def css_static(filename):
    return static_file(filename, root='/vagrant/labinski/bootstrap/css')

@bottle.route('/bootstrap/js/<filename>')
def js_static(filename):
    return static_file(filename, root='/vagrant/labinski/bootstrap/js')
