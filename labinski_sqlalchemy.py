import bottle
from bottle import route, run, template, get, post, request, static_file, error, Bottle, redirect, abort, debug
from bottle.ext.sqlalchemy import SQLAlchemyPlugin
#import scheduler
from novaapi import *
from model_sqlalchemy import *
#from settings import *
from beaker.middleware import SessionMiddleware
from os import environ
import datetime

#
# Bottle sqlalchemy
#
bottle.install(SQLAlchemyPlugin(engine, Base.metadata, create=True))

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

def check_login(beaker_session, db):
  
  if not 'logged_in' in beaker_session:
    abort(401, "Not logged in")

  name = beaker_session['name']

  student = db.query(User).filter_by(name=unicode(name)).first()

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

@route('/')
def slash(db):

  try:
    beaker_session = request.environ['beaker.session']
  except:
    #redirect('/login')
    abort(401, "Failed beaker_session in slash")

  try:
    name = beaker_session['name']
  except:
    redirect('/login')

  student = check_login(beaker_session, db)

  if student:
    classes = student.classes
  else:
    abort(401, "No student object")

  return template('index', images=db.query(Image).all(), \
                    classes=classes)

@post('/login')
def login(db):

  name = request.forms.name
  password = request.forms.password

  try:
    student = db.query(User).filter_by(name=unicode(name)).first()
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

@route('/login')
def login():
  return template('login')

@route('/logout')
def logout():

  try:
    beaker_session = request.environ['beaker.session']
    student = check_login(beaker_session)
  except:
    redirect('/login')

  request.environ['beaker.session'].delete()
  redirect('/login')

@route('/reserve')
def reserve(db):

  try:
    beaker_session = request.environ['beaker.session']
  except:
    abort(401, "No session")

  try:
    name = beaker_session['name']
  except:
    abort(401, "No session name")

  student = check_login(beaker_session, db)

  if student:
    classes = student.classes
  else:
    abort(401, "No student object")

  return template('reserve', classes=classes)

@route('/reservations')
def reservations(db):
  try:
    beaker_session = request.environ['beaker.session']
  except:
    abort(401, "No session")

  try:
    name = beaker_session['name']
  except:
    abort(401, "No session name")

  student = check_login(beaker_session, db)

  if student:
    reservations = student.reservations
  else:
    abort(401, "No student object")

  return template('reservations', reservations=reservations)

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

if __name__ == '__main__':
	    # Apparently have to do this here?
    # http://www.mail-archive.com/sqlalchemy@googlegroups.com/msg27358.html
    Base.metadata.create_all(engine)
    
    bottle.debug(True)
    run(app, host='192.168.33.10', reloader=True)
