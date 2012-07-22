#!/usr/bin/python2.6 python

from bottle import route, run, template, get, post,request,static_file,error
#import novainterface 
from novainterface import callnova
from scheduler import *

@get('/')
def login():
    return template('login_template')



@post('/login')
def login_submit():
    name     = request.forms.get('name')
    password = request.forms.get('password')
    print name, password
    existed = check_login(name,password)
    if existed:
      #reservation = check_instance(name)
      student = Student.query.filter_by(name=unicode(name)).one()
      if student.reservation :# show instance if yesa
         #student = Student.query.filter_by(name=unicode(name)).one()
         instance_id = student.reservation
         syslog.syslog(syslog.LOG_ERR, 'In if instance, before find server')
	 server = nova.servers.find(id=instance_id) 
         syslog.syslog(syslog.LOG_ERR, 'In if instance, after find server')
         ip = server.addresses['private'][0]['addr']
         url = server.get_vnc_console('novnc')['console']['url']
	 return template('info_template',name=name, ip=ip, url=url,instance_id=instance_id)
      else: # reserve instance if no
         return template('reserve_template',name=name)
    else:
        message=name+" does not exist"
        return template('error_template',message=message)

@post('/logout')
def logout():
  name = request.forms.get('name')
  print name
  return template('login_template')

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
@route('/bootstrap/css/<filename>')
def css_static(filename):
    return static_file(filename, root='/home/admin/hackavcl/bootstrap/css')

@route('/bootstrap/js/<filename>')
def js_static(filename):
    return static_file(filename, root='/home/admin/hackavcl/bootstrap/js')

#********Private Functions***********************

# create instance
def create_instance(name,time_span):
   server_info = callnova(name,time_span)
   return server_info

# check the login information
def check_login(name,password):
  for s in Student.query.all():
    if s.name == name :
       existed = True #check_user()
    else:
       existed = False
  return existed

# check whether the student has the instance or not
# name: student name
def check_instance(name):
   student = Student.query.filter_by(name=unicode(name)).one()
   #has_instance = student.reservation
   if student.reservation:
      return False 
   else:
      return True
#   return student

# instance_id: instance id
def terminate_instance(instance_id):
  kill_instance(instance_id)  
  success = 1#TODO terminate instance
  return success

run(host='10.0.2.15', port=8080)
