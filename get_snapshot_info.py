#!/usr/bin/python

# Look in ~/.boto for EC2Connection info (keys, region, etc.)
import boto 
from boto import ec2

console = boto.ec2.EC2Connection()

snapshots = console.get_all_snapshots(owner='self')

for snapshot in snapshots:
    print snapshot
    print 'ID: %s' % snapshot.id # The unique ID of the volume.
    print 'Start Time: %s' % snapshot.start_time # The creation time?
    print 'Description: %s' % snapshot.description
    print 'Tags: %s' % snapshot.tags
    print 'Volume ID %s' % snapshot.volume_id
    print 'Volume Size: %s' % snapshot.volume_size
    print '------------------------'
