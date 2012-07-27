#!/bin/bash

DIR=/vagrant/labinski

echo "This will delete all running nova instances, drop and create the db, reset and loadtestdata"
if ! sudo -u postgres dropdb hackavcl; then
	echo "couldn't dropdb"
	exit 1
fi
if ! sudo -u postgres createdb hackavcl; then
	echo "couldn't createdb"
	exit 1
fi

$DIR/bin/del.sh
$DIR/manage.py reset
$DIR/manage.py loadtestdata
