#!/usr/bin/python
#
# Script looks in ~/.boto for EC2Connection info (keys, region, etc.)
#

import boto 
from boto import ec2

console = boto.ec2.EC2Connection()

volumes = console.get_all_volumes()

for volume in volumes:
    print volume # the unique ID of the volume, accessible by volume.id
    print 'Create: %s' % volume.create_time # The timestamp of when the volume was created.
    print 'Status: %s' % volume.status # The status of the volume.
    print 'Size: %s' % volume.size # The size (in GB) of the volume.
    print 'Snapshot ID: %s' % volume.snapshot_id # The ID of the snapshot this volume was created from, if applicable.
    print 'Attach Data: %s' % volume.attach_data # An AttachmentSet object.
    print 'Zone: %s' % volume.zone # The availability zone this volume is in.
    print 'Type: %s' % volume.type # The type of volume (standard or consistent-iops)
    print 'IOPS: %s' % volume.iops # If this volume is of type consistent-iops, this is the number of IOPS provisioned (10-300).
    print 'Tags:'
    print volume.tags # the tags associated with the volume
    print 'Snapshots:'
    print volume.snapshots() # print the snapshots of this volume SLOWS DOWN SCRIPT CONSIDERABLY!!!!
    print '------------------------'
