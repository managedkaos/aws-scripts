#!/usr/bin/python
# Look in ~/.boto for EC2Connection info (keys, region, etc.)
import pprint
import boto 
from boto import ec2

printer = pprint.PrettyPrinter(indent=4)

console = boto.ec2.EC2Connection()

# get reservations to look at instances
reservations = console.get_all_instances()

# get volumes
volumes = console.get_all_volumes()

# get snapshots
snapshots = console.get_all_snapshots()

print "____Instance____"
for reservation in reservations:
    for instance in reservation.instances:
        printer.pprint( instance.__dict__ )
        break
    break

print "\n\n____Volume____"
for volume in volumes:
    printer.pprint( volume.__dict__ )
    break

print "\n\n____Snapshot____"
for snapshot in snapshots:
    printer.pprint( snapshot.__dict__ )
    break

