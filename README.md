The Labinski
============

The Labinski is a virtual computer lab that runs on top of [OpenStack](http://www.openstack.org) using the python novaclient.

The Name
--------

Labinski means "lab in sky", ie. a virtual computer lab in the "cloud", where the cloud could be whatever you define it as. :)

Requirements
------------

* An OpenStack cloud (can be run inside a vm with [devstack](http://www.devstack.org))
* A database that is supported by SQLAlchemy
* python
    * Novaclient
    * Elixir, which requires SQLAlchemy
    * Bottle
    * Beaker
    * Others...see pip_freeze.txt

Usage
-----

* Create a database that supported by SQLALchemy

```
git checkout https://github.com/curtisgithub/labinski
cd labinski
```

* Edit the settings.py file
* Edit the openstackrc.py file

```
python manage.py reset
python manage.py loadtestdata
python manage.py runserver
````

* Open a web browswer and login to localhost:8080