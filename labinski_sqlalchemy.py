import bottle
from bottle import route, run, template, get, post, request, static_file, error, Bottle, redirect, abort, debug
from bottle.ext.sqlalchemy import SQLAlchemyPlugin
#import scheduler
from novaapi import *
from model_sqlalchemy import *
#from settings import *
<<<<<<< HEAD
=======
from beaker.middleware import SessionMiddleware
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823
from os import environ
import datetime
import logging


#
# Bottle sqlalchemy
#
bottle.install(SQLAlchemyPlugin(engine, Base.metadata, create=True))

<<<<<<< HEAD
app = bottle.default_app()
=======
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
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823

#
# Functions
#

<<<<<<< HEAD
def check_login(db):
  
  name = request.environ.get('REMOTE_USER')

  if not name:
    return False
=======
def check_login(beaker_session, db):
  
  if not 'logged_in' in beaker_session:
    abort(401, "Not logged in")

  name = beaker_session['name']
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823

  student = db.query(User).filter_by(name=unicode(name)).first()

  if student:
    return student

<<<<<<< HEAD
  return False
=======
  return None
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823

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
#********************************************************************
@route('/')
def slash(db):

<<<<<<< HEAD
  student = check_login(db)
=======
  try:
    beaker_session = request.environ['beaker.session']
  except:
    #redirect('/login')
    abort(401, "Failed beaker_session in slash")

  try:
    name = beaker_session['name']
  except:
    logging.debug('======> slash has no beaker_session name')
    redirect('/login')

  student = check_login(beaker_session, db)
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823

  if student:
    classes = student.classes
  else:
    abort(401, "No student object")

<<<<<<< HEAD
  return template('index', classes=classes, name=student.name, is_admin=student.is_admin)


=======
  return template('index', images=db.query(Image).all(), \
                    classes=classes)

#********************************************************************
@post('/login')
def login(db):

  logging.debug('======> in login form')
  name = request.forms.name
  password = request.forms.password

  try:
    student = db.query(User).filter_by(name=unicode(name)).first()
  except:
    abort(401, "No student object in login")

  logging.debug('======> past student query')

  if student:
    beaker_session = request.environ['beaker.session']
    beaker_session['logged_in'] = True
    beaker_session['name'] = name
    logging.debug('======> about to redirect to slash')

    redirect('/')
  else:
    error_msg = 'username or password not valid'
    return template('login', error_msg=error_msg)

  logging.debug('======> bottom of login func')
  error_msg = 'Failed to find student'
  return template('login', error_msg=error_msg)

@route('/login')
def login():
  return template('login')
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823

#********************************************************************
@route('/logout')
def logout():
<<<<<<< HEAD
 return template('logout')
=======

  try:
    beaker_session = request.environ['beaker.session']
    student = check_login(beaker_session)
  except:
    redirect('/login')

  request.environ['beaker.session'].delete()
  redirect('/login')
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823

#********************************************************************
@route('/reserve')
def reserve(db):

<<<<<<< HEAD
  student = check_login(db)
=======
  try:
    beaker_session = request.environ['beaker.session']
  except:
    abort(401, "No session")

  try:
    name = beaker_session['name']
  except:
    abort(401, "No session name")

  student = check_login(beaker_session, db)
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823

  if student:
    classes = student.classes
  else:
    abort(401, "No student object")

<<<<<<< HEAD
  return template('reserve', classes=classes, name=student.name, is_admin=student.is_admin)
=======
  return template('reserve', classes=classes)
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823

#********************************************************************
@route('/reservations')
def reservations(db):
<<<<<<< HEAD

  student = check_login(db)
=======
  try:
    beaker_session = request.environ['beaker.session']
  except:
    abort(401, "No session")

  try:
    name = beaker_session['name']
  except:
    abort(401, "No session name")

  student = check_login(beaker_session, db)
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823

  if student:
    reservations = student.reservations
    reservations.reverse()
  else:
    abort(401, "No student object")

<<<<<<< HEAD
  return template('reservations', reservations=reservations, name=student.name, is_admin=student.is_admin)
=======
  return template('reservations', reservations=reservations)
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823

#
# Make reservation
# 
#********************************************************************
@post('/reservation')
def reservation(db):

<<<<<<< HEAD
  student = check_login(db)
=======
  try:
    beaker_session = request.environ['beaker.session']
  except:
    abort(401, "No session")

  try:
    name = beaker_session['name']
  except:
    abort(401, "No session name")

  student = check_login(beaker_session, db)
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823

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
  # Get class
  #
  try:
    _class = db.query(Class).filter_by(name=unicode(class_name)).first()
  except:
    abort(401, "Class query failed")

  if not _class:
<<<<<<< HEAD
    abort(401, "Class was not selected")
=======
    abort(401, "Class object was not returned")
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823

  #
  # Get image
  # 
  try:
    image = db.query(Image).filter_by(os_image_id=unicode(image_os_image_id)).first()
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

  logging.debug('****** About to create reservation ***********')
  reservation = Reservation(user_id=student.id, class_id=_class.id, image_id=image.id)
  db.add(reservation)
  db.commit()


  resources = is_resource_available(student=student, 
									_class=_class, 
									image=image, 
									start_time=start_time, 
									reservation_length=reservation_length)

  if resources:
	add_reservation_jobs(student, reservation, start_time, reservation_length, image, db)
  else:
  	db.delete(reservation)
  	db.commit()
	abort(401, "No resources for that time")

 
  
  db.commit()

  redirect('/reservations')

#********************************************************************
@route('/connections')
def connections(db):

<<<<<<< HEAD
  student = check_login(db)
=======
  try:
    beaker_session = request.environ['beaker.session']
  except:
    abort(401, "No session")

  try:
    name = beaker_session['name']
  except:
    abort(401, "No session name")

  student = check_login(beaker_session, db)
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823

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

<<<<<<< HEAD
  return template('connections', servers=servers, reservations=reservations, name=student.name, is_admin=student.is_admin)
=======
  return template('connections', servers=servers, reservations=reservations)
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823

#********************************************************************
@route('/images')
def show_images(db):

<<<<<<< HEAD
  student = check_login(db)
=======
  try:
    beaker_session = request.environ['beaker.session']
  except:
    abort(401, "No session")

  try:
    name = beaker_session['name']
  except:
    abort(401, "No session name")

  student = check_login(beaker_session, db)
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823

  if student:
    images = get_images(student)
  else:
    abort(401, "No student object")

<<<<<<< HEAD
  return template('show_images', images=images, name=student.name, is_admin=student.is_admin)

@route ('/delete/reservation/<id:int>')
def delete_instance(id, db):

  assert isinstance(id, int)

  student = check_login(db)

  reservation = db.query(Reservation).filter_by(id=id).first()

  if not reservation:
    abort(401, 'Reservation does not exist')

  if not reservation.user.name == student.name:
    abort(401, "Cannot delete a reservation that is not yours")

  try:
    server = nova.servers.find(id=reservation.instance_id)
  except:
    server = None

  if server:
    try:
      nova.servers.delete(reservation.instance_id)
    except:
      abort(401, "Could not delete instance")

  try:
    db.delete(reservation)
    db.commit()
  except:
    abort(401, "Could not delete reservation")

  notification = Notification(user_id=student.id, message="Reservation with id " + str(id) + " was deleted", status="INFO" )
  db.add(notification)
  db.commit()  

  redirect('/reservations')


#********************************************************************
@route('/notifications')
def notifications(db):

  student = check_login(db)
=======
  return template('show_images', images=images)

#********************************************************************
@route('/notifications')
def notifications(db):

  try:
    beaker_session = request.environ['beaker.session']
  except:
    abort(401, "No session")

  try:
    name = beaker_session['name']
  except:
    abort(401, "No session name")

  student = check_login(beaker_session, db)
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823

  if student:
    notifications = student.notifications
    notifications.reverse()

<<<<<<< HEAD
  return template('notifications', notifications=notifications, name=student.name, is_admin=student.is_admin)

#
# ADMIN
# 

@route('/admin/listjobs')
def admin_listjobs(db):

  student = check_login(db)

  if not student.is_admin:
    abort(401, "Not admin")

  jobs = sched.get_jobs()

  return template('admin_listjobs', jobs=jobs, name=student.name, is_admin=student.is_admin)
=======
  return template('notifications', notifications=notifications)
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823

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

    logging.basicConfig(level=logging.DEBUG)
    logging.debug('Started')
    
    bottle.debug(True)
<<<<<<< HEAD
    run(app, host='10.0.4.5', port=80, reloader=True)
=======
    run(app, host='192.168.33.10', reloader=True)
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823
