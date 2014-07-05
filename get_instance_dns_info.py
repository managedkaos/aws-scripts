#!/usr/bin/python
#
# Script looks in ~/.boto for EC2Connection info (keys, region, etc.)
#
import boto
from boto import ec2

dns_info = []
dns_info.append(['ID', 'Private IP', 'Public DNS', 'Name'])

console = boto.ec2.EC2Connection()

reservations = console.get_all_instances()

for reservation in reservations:
    for instance in reservation.instances:
        dns_info.append([instance.id, instance.private_ip_address, instance.public_dns_name, instance.tags['Name']])

for row in dns_info:
    print("{: <11} {: <15} {: <50} {: <20}".format(*row))
