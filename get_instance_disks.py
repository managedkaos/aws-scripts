#!/usr/bin/python
#
# Script looks in ~/.boto for EC2Connection info (keys, region, etc.)
#

import json
import boto
from boto import ec2

console = boto.ec2.EC2Connection()

reservations = console.get_all_instances()

for reservation in reservations:
    for instance in reservation.instances:
        disks = []
        for disk in instance.block_device_mapping:
            disks.append(disk)

        print json.dumps({
                             "instance-name": instance.tags['Name'],
                             "instance-id": instance.id,
                             "disk count": len(disks),
                             "disks": disks
                         }, sort_keys=False, indent=4)