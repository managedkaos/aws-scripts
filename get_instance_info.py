#!/usr/bin/python
#
# Script looks in ~/.boto for EC2Connection info (keys, region, etc.)
#
import boto
from boto import ec2

console = boto.ec2.EC2Connection()

reservations = console.get_all_instances()

for reservation in reservations:
    for instance in reservation.instances:
        print 'ID %s' % instance.id
        for tag in instance.tags:
            print "Tag: %s %s" % (tag, instance.tags[tag])

        print 'ami_launch_index %s' % instance.ami_launch_index
        print 'architecture %s' % instance.architecture
        print 'block_device_mapping %s' % instance.block_device_mapping
        print 'ebs_optimized %s' % instance.ebs_optimized
        print 'groups %s' % instance.groups
        print 'groups %s' % instance.groups
        print 'hypervisor %s' % instance.hypervisor
        print 'image_id %s' % instance.image_id
        print 'instance_profile %s' % instance.instance_profile
        print 'instance_type %s' % instance.instance_type
        print 'interfaces %s' % instance.interfaces
        print 'ip_address %s' % instance.ip_address
        print 'kernel %s' % instance.kernel
        print 'key_name %s' % instance.key_name
        print 'launch_time %s' % instance.launch_time
        print 'monitored %s' % instance.monitored
        print 'monitoring_state %s' % instance.monitoring_state
        print 'placement %s' % instance.placement
        print 'placement_group %s' % instance.placement_group
        print 'placement_tenancy %s' % instance.placement_tenancy
        print 'platform %s' % instance.platform
        print 'previous_state %s' % instance.previous_state
        print 'previous_state_code %s' % instance.previous_state_code
        print 'private_dns_name %s' % instance.private_dns_name
        print 'private_ip_address %s' % instance.private_ip_address
        print 'product_codes %s' % instance.product_codes
        print 'public_dns_name %s' % instance.public_dns_name
        print 'ramdisk %s' % instance.ramdisk
        print 'root_device_name %s' % instance.root_device_name
        print 'root_device_type %s' % instance.root_device_type
        print 'spot_instance_request_id %s' % instance.spot_instance_request_id
        print 'state %s' % instance.state
        print 'state_code %s' % instance.state_code
        print 'state_reason %s' % instance.state_reason
        print 'subnet_id %s' % instance.subnet_id
        print 'virtualization_type %s' % instance.virtualization_type
        print 'vpc_id %s' % instance.vpc_id
        print '================================================'