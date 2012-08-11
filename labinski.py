import bottle
from bottle import route, run, template, get, post, request, static_file, error, Bottle, redirect, abort, debug
from bottle.ext.sqlalchemy import SQLAlchemyPlugin
from novaapi import *
from model import *
from os import environ
import datetime
import logging
from tasks import *
from collections import namedtuple

#
# Bottle sqlalchemy
#
bottle.install(SQLAlchemyPlugin(engine, Base.metadata, create=True))

app = bottle.default_app()

#
# Functions
#

def check_login(db):
  
  name = request.environ.get('REMOTE_USER')

  if not name:
    return False

  student = db.query(User).filter_by(name=unicode(name)).first()

  if student:
    return student

  return False

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

  student = check_login(db)

  if student:
    classes = student.classes
  else:
    abort(401, "No student object")

  return template('index', classes=classes, name=student.name, is_admin=student.is_admin)



#********************************************************************
@route('/logout')
def logout():
 return template('logout')


#********************************************************************
@route('/reserve')
def reserve(db):

  student = check_login(db)

  if student:
    classes = student.classes
  else:
    abort(401, "No student object")

  return template('reserve', classes=classes, name=student.name, is_admin=student.is_admin)


#********************************************************************
@route('/reservations')
def reservations(db):

  student = check_login(db)

  if student:
    reservations = student.reservations
    reservations.reverse()
  else:
    abort(401, "No student object")

  return template('reservations', reservations=reservations, name=student.name, is_admin=student.is_admin)


#
# Make reservation
# 
#********************************************************************
@post('/reservation')
def reservation(db):

  student = check_login(db)

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
  start_time = datetime.datetime.utcnow()

  #
  # Get class
  #
  try:
    _class = db.query(Class).filter_by(name=unicode(class_name)).first()
  except:
    abort(401, "Class query failed")

  if not _class:
    abort(401, "Class was not selected")

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

  student = check_login(db)

  if student:
    reservations = student.reservations
  else:
    abort(401, "No student object")

  servers = []

  # Create a namedtuple to store the server info in
  Server = namedtuple('Server', ['name', 'console_url', 'ip'])

  for r in reservations:
    try:
      server = nova.servers.find(id=r.instance_id)
    except:
      server = None

    if server:
      # Take the first network to get the IP from
      try:
        network = server.addresses.keys()[0]
      except:
        network = None

      if network:
        try:
          # First IP from first network
          # Sometimes the instance will exist but not have an IP yet
          ip = server.addresses[network][0]['addr']
        except:
          ip = None
      else:
        ip = None

      name = server.name
      console_url = server.get_vnc_console('novnc')['console']['url']

      # create custom server object and append to list
      s = Server(name, console_url, ip)
      servers.append(s)


  return template('connections', servers=servers, reservations=reservations,
                   name=student.name, is_admin=student.is_admin)


#********************************************************************
@route('/images')
def show_images(db):

  student = check_login(db)

  if student:
    images = get_images(student)
  else:
    abort(401, "No student object")

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

  notification = Notification(user_id=student.id, message="Reservation with id " \
                              + str(id) + " was deleted", status="INFO" )
  db.add(notification)
  db.commit()  

  redirect('/reservations')


#********************************************************************
@route('/notifications')
def notifications(db):

  student = check_login(db)

  if student:
    notifications = student.notifications
    notifications.reverse()

  return template('notifications', notifications=notifications, name=student.name, 
                  is_admin=student.is_admin)

#
# ADMIN
# 

@route('/admin/listjobs')
def admin_listjobs(db):

  # In order to find the status of the job we need to use this
  from celery.result import AsyncResult

  student = check_login(db)

  if not student.is_admin:
    abort(401, "Not admin")

  inspector = celery.control.inspect()
  scheduled_jobs = inspector.scheduled()
  try:
    hostname = scheduled_jobs.keys()[0]
    scheduled_jobs = scheduled_jobs[hostname]
  except:
    scheduled_jobs = None

  jobs = []

  # Create a named tuple to put all the job data into
  Job = namedtuple('Job', ['eta', 'name', 'id', 'status'])

  if scheduled_jobs:
    for j in scheduled_jobs:
      eta = j['eta']
      name = j['request']['name']
      id = j['request']['id']
      try:
        result = AsyncResult(id)
      except:
        result = None

      if result:
        status = result.status
        job = Job(eta, name, id, status)
        jobs.append(job)
      else:
        # jobs is empty
        pass


  return template('admin_listjobs', jobs=jobs, name=student.name, is_admin=student.is_admin)


#
# Static 
#

@route('/bootstrap/css/<filename>')
def css_static(filename):
    return static_file(filename, root=ROOT_DIR + '/bootstrap/css')

@route('/bootstrap/js/<filename>')
def js_static(filename):
    return static_file(filename, root=ROOT_DIR + '/bootstrap/js')

@route('/bootstrap/img/<filename>')
def js_static(filename):
    return static_file(filename, root=ROOT_DIR + '/bootstrap/img')

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
    run(app, host=IP, port=80, reloader=True)

