import sys
from elixir import *
from model import Student, Reservation, Class, ImageType, Flavor, Image
from modelapi import init_db
from hackavcl import app
from settings import *
from bottle import run, debug

init_db(DATABASE)

import socket
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def reset():
    ''' Reset database and recreates tables. '''
    #cleanup_all(drop_tables=True)
    drop_all()
    init()

def init():
    ''' Creates initial statuses '''
    create_all()
    ImageType(name='windows')
    ImageType(name='linux')
    Flavor(os_id=1)
    session.commit()

def add_student(name,email):
    Student(name=name, email=email)
    session.commit()

def add_image(name,os_image_id, flavor,type):
    Image(name=name, os_image_id=os_image_id, flavor=flavor,type=type)
    session.commit()

def add_flavor(os_id):
    Flavor(os_id=os_id)
    session.commit()

def add_class(name,image=""):
    Class(name=name)
    session.commit()

def load_test_data():
    add_student("curtis", "serverascode@gmail.com")
    f = Flavor.query.filter_by(os_id=1).one()
    t = ImageType.query.filter_by(name='linux').one()
    add_image(name="matlab", os_image_id=IMAGE, flavor=f, type=t)
    add_class("Math 101")

def runserver():
    ''' Starts development server. '''
    # Turn on debug
    debug(True)

    # Don't always want to run on local host when using vagrant to port forward
    eth0_ip = get_ip_address('eth0')

    # Reloader
    run(app, host=eth0_ip, port=8080, reloader=True)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'reset':
            reset()
        if sys.argv[1] == 'init':
            init()
        if sys.argv[1] == 'runserver':
            runserver()
        if sys.argv[1] == 'loadtestdata':
            load_test_data()
    if len(sys.argv) == 4:
	if sys.argv[1] == 'addstudent':
	    add_student(sys.argv[2], sys.argv[3])
	if sys.argv[1] == 'addimage':
	    add_image(sys.argv[2], sys.argv[3])
