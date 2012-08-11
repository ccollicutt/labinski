The Labinski
============

The Labinski is a virtual computer lab that runs on top of [OpenStack](http://www.openstack.org) using the python novaclient.

The Name
--------

Labinski means "lab in sky", ie. a virtual computer lab in the "cloud."

Requirements
------------

* An OpenStack cloud (Not as hard to get as one might think: can be run inside a vm with [devstack](http://www.devstack.org))
* A database that is supported by SQLAlchemy (eg. postgres)
* python (developed on python 2.6.6 in CentOS 6)
    * Novaclient
    * Celery
    * Bottle
    * Others...see pip_freeze.txt

Usage
-----

* Create a database that is supported by SQLALchemy (ie. postgres/mysql)

```
git checkout https://github.com/curtisgithub/labinski
cd labinski
```

* Edit the settings.py file, make appropriate changes
* Edit/create the openstackrc.py file, make appropriate changes

```
python manage.py reset
python manage.py loadtestdata
python manage.py runserver
````

* Open a web browswer and login to localhost:8080