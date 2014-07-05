#!/usr/bin/python
#
# Script looks in ~/.boto for EC2Connection info (keys, region, etc.)
#

import boto
from boto import ec2

# set up an empty list to hold the IPs
hosts = []

# connect to EC2 and get all of the instances
console = boto.ec2.EC2Connection()
reservations = console.get_all_instances()

# take a look at each instance
for reservation in reservations:
    for instance in reservation.instances:

        # skip any instances that are stopped; their IP comes up as 'None'
        if (instance.state == 'stopped'):
            continue

        hosts.append([instance.private_ip_address, '#', instance.tags['Name'], instance.public_dns_name])

# sort the list
hosts.sort()
print '[hosts]'

# print the IPs in nice columns
widths = [max(map(len, col)) for col in zip(*hosts)]

for row in hosts:
    print " ".join((val.ljust(width) for val, width in zip(row, widths)))