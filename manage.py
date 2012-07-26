import sys
from elixir import *
from model import Student, Reservation, Class, ImageType, Flavor, Image, Notification, Service
from modelapi import init_db
from labinski import app
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

    Service(name="ssh", port="22")
    Service(name="rdp", port="3389")
    Service(name="http", port="80")

    session.commit()

    rdp_connection = Service.query.filter_by(name=unicode('rdp')).first()
    ssh_connection = Service.query.filter_by(name=unicode('ssh')).first()
    http_connection = Service.query.filter_by(name=unicode('http')).first()

    linux_services = []
    linux_services.append(ssh_connection)
    linux_services.append(http_connection)

    ImageType(name='Generic Windows',os="Windows", services=[rdp_connection])
    ImageType(name='Generic Linux', os="Linux", services=linux_services)
    Flavor(os_id=1)
    session.commit()

def add_student(name,email,_class=None):
    if not _class:
        Student(name=name, email=email)
    else:
        Student(name=name, email=email, classes=[_class])

    session.commit()

def add_image(name,os_image_id, flavor,image_type,description):
    Image(name=name, os_image_id=os_image_id, flavor=flavor,image_type=image_type,description=description)
    session.commit()

def add_flavor(os_id):
    Flavor(os_id=os_id)
    session.commit()

def add_class(name):
    Class(name=name)
    session.commit()

def add_notification(message,status,name=None):
    
    if name:
        student = Student.query.filter_by(name=unicode(name)).first()
        Notification(student=student,message=message,status=status)
    else:
        Notification(message=message)

def load_test_data():

    f = Flavor.query.filter_by(os_id=1).one()
    windows = ImageType.query.filter_by(name=unicode('Generic Windows')).first()
    linux = ImageType.query.filter_by(name=unicode('Generic Linux')).first()

    if not windows:
        print "couldn't get windows"

    # Using the IMAGE from settings.py for now...
    add_image(name="matlab", os_image_id=IMAGE, flavor=f, image_type=linux, description="This image has matlab version 7.56 which allows for the math usages")
    # Image cirros-0.3.0-x86_64-uec-ramdisk
    add_image(name="photoshop", os_image_id="647abf63-fd95-42a7-a744-e1885f8d5c16", flavor=f, image_type=windows, description="This image has photoblops R456 for the blogginz")
    
    # Add a math class
    matlab_image = Image.query.filter_by(name=unicode('matlab')).first()
    education_image = Image.query.filter_by(name=unicode('photoshop')).first()

    # Add classes
    add_class(name="Math 101")
    add_class(name="EDTECH 401")
    add_class(name="EDMATH 502")

    # Get classes
    math_class = Class.query.filter_by(name=unicode('Math 101')).first()
    education_class = Class.query.filter_by(name=unicode('EDTECH 401')).first()
    edmath_class = Class.query.filter_by(name=unicode('EDMATH 502')).first()

    # Add images
    math_class.images.append(matlab_image)
    education_class.images.append(education_image)
    edmath_class.images.append(education_image)
    edmath_class.images.append(matlab_image)


    # Add students
    add_student(name="curtis", email="serverascode@gmail.com", _class=math_class)
    curtis = Student.query.filter_by(name=unicode('curtis')).first()
    curtis.classes.append(education_class)
    curtis.classes.append(edmath_class)

    add_notification(name='curtis', message='Some warning message', status="WARNING")
    add_notification(name='curtis', message='Some error message', status="ERROR")


    # Add a student without a class
    add_student("test", "test@example.com")

    session.commit()


def runserver():
    ''' Starts development server. '''
    # Turn on debug
    debug(True)

    # Don't always want to run on local host when using vagrant to port forward
    eth1_ip = get_ip_address('eth1')

    # Reloader
    run(app, host=eth1_ip, port=8080, reloader=True)
    #run(app, host="127.0.0.1", port=8080, reloader=True)

# XXX FIX ME - Do proper arguments XXX
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
    if len(sys.argv) == 5:
        if sys.argv[1] == 'addimage':
            add_image(sys.argv[2], sys.argv[3], sys.argv[4])

