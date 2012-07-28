#!/bin/bash

#
# Delete/Stop all running openstack instances
# 

for s in `nova list | grep ACTIVE | cut -f 2 -d "|" | tr -d " "`; do 
	echo "nova deleting $s"
	nova delete $s
done
