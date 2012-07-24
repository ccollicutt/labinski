#!/usr/bin/python2.6 python

from bottle import route, run, template, get, post, request, static_file, error, Bottle
import scheduler
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
   

#@app.route('/reservations'):
#  pass

@app.post('/reservation')
def reservation():
  reservation_time = request.forms.reservation_time
  reservation_image_name = request.forms.reservation_image_name
  reservation_length = request.forms.reservation_length

  return template('reservation', time=reservation_time, image_name=reservation_image_name, length=reservation_length)



@app.route('/images')
def show_images():

  student = Student.query.filter_by(name=unicode(name)).one()
  classes = student.classes

  return template('show_images', classes=classes)

@post('/release')
def release():
  name = request.forms.get('name')
  student = Student.query.filter_by(name=unicode(name)).one()
  instance_id = student.reservation
  #instance_id = request.forms.get('instance_id')
  print "release the instance: ", instance_id
  success = terminate_instance(instance_id)
  if success:
    return template('reserve_template',name=name)
  else:
    message=instance_id + " release failed!"
    return tempalte('error_template',message=message)

@error(404)
def error404(error):
    return template('error_template', message=error)

#*********static files*************************
@app.route('/bootstrap/css/<filename>')
def css_static(filename):
    return static_file(filename, root='/vagrant/hackavcl/bootstrap/css')

@app.route('/bootstrap/js/<filename>')
def js_static(filename):
    return static_file(filename, root='/vagrant/hackavcl/bootstrap/js')
