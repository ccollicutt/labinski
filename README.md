The Labinski
============

The Labinski is a virtual computer lab that runs on top of OpenStack using the python novaclient.

The Name
--------

Labinski means "lab in sky", ie. a virtual computer lab in the "cloud.""

Requirements
------------

* An OpenStack cloud (can be run inside a vm with devstack)
* A database that is supported by SQLAlchemy
* python
** Novaclient
** Elixir, which requires SQLAlchemy
** Bottle
** Beaker

Usage
-----

Create a database that supported by SQLALchemy
git checkout https://github.com/curtisgithub/labinski
cd labinski
Edit the settings.py file
Edit the openstackrc.py file
python manage.py reset
python manage.py loadtestdata
python manage.py runserver
login to localhost:8080