#!/usr/bin/python2.6 python
import bottle
from bottle import route, run, template, get, post, request, static_file, error, Bottle, redirect, abort, debug
#import scheduler
from novaapi import *
from model import Student, Reservation, Class, Image, Notification
from modelapi import init_db
from settings import *
from beaker.middleware import SessionMiddleware
from os import environ
import datetime

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

def get_images(student):

  classes = student.classes
  images = []
  for c in classes:
    for i in c.images:
      images.append(i)

  # This is magic to remove duplicates
  # http://docs.python.org/faq/programming.html#how-do-you-remove-duplicates-from-a-list
  images = list(set(images))

  return images

#
# Routes
# 

@bottle.route('/')
def slash():

  try:
    beaker_session = request.environ['beaker.session']
  except:
    #redirect('/login')
    abort(401, "Failed beaker_session in slash")

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
  
#
# Make reservation
# 
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
    start_time = request.forms.start_time
    image_os_image_id = request.forms.image_os_image_id
    class_name = request.forms.class_name
    reservation_length = request.forms.reservation_length
  except:
    abort(401, "Incomplete reservation post data")

  # is_valid_student(name)
  # is_valid_image(student)
  # is_valid_reservation_time(time)

  #XXX FIX ME XXX - only used for testing
  start_time = datetime.datetime.now()

  #
  # Check class
  #
  try:
    _class = Class.query.filter_by(name=unicode(class_name)).first()
  except:
    abort(401, "Class query failed")

  if not _class:
    abort(401, "Class object was not returned")

  #
  # Check image
  # 
  try:
    image = Image.query.filter_by(os_image_id=unicode(image_os_image_id)).first()
  except:
    abort(401, "Image query failed")

  if not image:
    abort(401, "Image object was not returned")

  #
  # Check reservation_length
  #
  try:
    reservation_length = int(reservation_length)
  except:
    abort(401, "Could not convert reservation_length to integer")

  if reservation_length > 8:
    abort(402, "Reservation length too long")
  
  reservation = reservation_request(student=student, _class=_class, image=image, start_time=start_time, reservation_length=reservation_length)
  
  if reservation:
    redirect('/connections')
  else:
    abort(401, "Reservation failed")

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
      server = nova.servers.find(id=reservation.instance_id)
    except:
      server = None
    if server:
      servers.append(server)

  return template('connections', servers=servers, reservations=reservations)

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
    images = get_images(student)
  else:
    abort(401, "No student object")

  return template('show_images', images=images)

@bottle.route('/notifications')
def notifications():

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
    notifications = student.notifications
    notifications.reverse()

  return template('notifications', notifications=notifications)

#
# Static 
#

@bottle.route('/bootstrap/css/<filename>')
def css_static(filename):
    return static_file(filename, root=ROOT_DIR + '/bootstrap/css')

@bottle.route('/bootstrap/js/<filename>')
def js_static(filename):
    return static_file(filename, root=ROOT_DIR + '/bootstrap/js')

#
# Error pages
#
#@bottle.error(401)
#def error401(error):
#    return template('error401', error=error)

