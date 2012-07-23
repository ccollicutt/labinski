#!/usr/bin/python2.6 python

from bottle import route, run, template, get, post, request, static_file, error, Bottle
from scheduler import *

app = Bottle()

@app.route('/')
def login():
    return template('index.tpl')

@post('/reserve')
def reserve():
   name = request.forms.get('name')
   image = request.forms.get('image')
   time_span = request.forms.get('time_span')
       
   # create instance
   #original instance = create_instance(image,time_span)
   instance = create_instance(name,time_span)   
   ip = instance.addresses['private'][0]['addr']
   instance_id = str(instance.id)
   url = instance.get_vnc_console('novnc')['console']['url']
   #instance_id = 'instance 1'
   if ip != '':
      return template('info_template', name=name, ip=ip, url=url,instance_id=instance_id)
   else:
      message = "Instance does not be reserved successfully, please contact admin"
      return template('error_template', message=message)
   
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
