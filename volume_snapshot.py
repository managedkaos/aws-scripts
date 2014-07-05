#!/usr/bin/python
#
# Script looks in ~/.boto for EC2Connection info (keys, region, etc.)
#

import boto
from boto import ec2

import sys
import time
import datetime
import argparse
import logging
from sys import argv

# set up command line arguments
parser = argparse.ArgumentParser(prog="volume_snapshot.py",
                                 description="A script to create snapshots of EC2 volumes.")

# volumes entered singly or as a list are stored in args.volumes
parser.add_argument('volumes',
                    metavar='vol',
                    nargs='*',
                    help='ID of the volume to use for the snapshot. In vol-abcd1234 format')

# --all = processes all volumes in the console
parser.add_argument('--all',
                    dest='all_volumes',
                    action='store_true',
                    help='Creates snapshots for all volumes listed in the console.')

# --daily = set up daily snapshot
parser.add_argument('--daily',
                    dest='daily',
                    action='store_true',
                    help='Creates a snapshot and tags it with DAILY.')

# --weekly = set up weekly snapshot
parser.add_argument('--weekly',
                    dest='weekly',
                    action='store_true',
                    help='Creates a snapshot and tags it with WEEKLY.')

# --rotate = delete expired snapshots
parser.add_argument('--rotate',
                    dest='rotate',
                    action='store_true',
                    help='Removes any expired snapshots. Mutually exclusive with snapshot creation.')

# --verbose = turn on logging at the INFO level; errors will always be printed.
parser.add_argument('--verbose',
                    dest='verbose',
                    action='store_true',
                    help="Let's the script print the volume ID and the snapshot description as they are processed.")

# process command line arguments
args = parser.parse_args()

# if there are no volumes AND the '--all' switch wasn't used, stop processing
if (len(args.volumes) == 0) and (args.all_volumes is False):
    print "\nNothing to snapshot. Specify a volume or use the --all switch or use --help.\n"
    print 'One volume      : ' + argv[0] + ' vol-0a123456'
    print 'List of volumes : ' + argv[0] + ' vol-0b123456 vol-0c123456 vol-d1234567 vol-e1234567'
    print 'All volumes     : ' + argv[0] + ' --all'
    exit(1)

# if configure logging based on verbose argument
if args.verbose:
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %I:%M:%S %p')
else:
    logging.basicConfig(level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %I:%M:%S %p')

# create a connection to the ec2 console
try:
    console = boto.ec2.EC2Connection()

except Exception, e:
    logging.error('Failed to connect to EC2 console.')
    sys.exit(e)

# get the volumes
if len(args.volumes) > 0:

    # if volumes were specified on the command line, try to process them
    logging.info('Processing %s', args.volumes)

    try:
        volumes = console.get_all_volumes(volume_ids=args.volumes)

    except Exception, e:
        logging.error('Failed to get volumes. %s', e)
        sys.exit(e)

elif args.all_volumes:

    # if the --all switch was used, then try to process all volumes
    logging.info('Processing all volumes.')

    try:
        volumes = console.get_all_volumes()

    except Exception, e:
        logging.error('Failed to get volumes.')
        sys.exit(e)

logging.info('Number of volumes to process: %s', len(volumes))

# loop over the volumes
for volume in volumes:
    logging.info('%s: Processing...', volume.id)

    if args.daily or args.weekly:
        logging.info('%s: Setting daily expiration: %s', volume.id, args.daily)
        logging.info('%s: Setting weekly expiration: %s', volume.id, args.weekly)

        # tag the volume with the name and ID of the instance it is attached to, in 3 steps:
        # 1) get the reservation for the instance that has attachment data for this volume
        try:
            reservations = console.get_all_instances(volume.attach_data.instance_id)
        except:
            logging.error('%s: Failed to get instance %s', volume.id, volume.attach_data.instance_id)

        # 2) pull the instance out of the reservation
        for reservation in reservations:
            for instance in reservation.instances:

                try:
                    # 3) create the tag using the instance object's properties
                    console.create_tags([volume.id], {'Name': instance.tags['Name']})
                    console.create_tags([volume.id], {'Attached Instance Name': instance.tags['Name']})
                    console.create_tags([volume.id], {'Attached Instance ID': instance.id})
                except:
                    logging.error('%s: Could not tag volume.', volume.id)

        # create a new snapshot, stamp it with name, date, and time 
        stamp = time.strftime("%Y-%b-%d %H:%M:%S %Z", time.localtime()) + '; ' + instance.tags['Name'] + '; ' + \
                instance.id + '; ' + volume.id

        logging.info('%s: Snapshot stamp = "%s"', volume.id, stamp)

        try:
            this_snapshot = console.create_snapshot(volume.id, stamp)

        except Exception, e:
            logging.error('%s: Failed to create snapshot. %s', volume.id, e)
            sys.exit(e)

        # tag the snapshot with the volume and instance info
        try:
            console.create_tags([this_snapshot.id], {'Name': instance.tags['Name']})
            console.create_tags([this_snapshot.id], {'Parent Volume': volume.id})
            console.create_tags([this_snapshot.id], {'Attached Instance Name': instance.tags['Name']})
            console.create_tags([this_snapshot.id], {'Attached Instance ID': instance.id})

        # if we can't tag this snapshot, bail to the next because everything after here is tagging
        except:
            logging.error('%s: Could not tag snapshot. %s', volume.id, this_snapshot.id)
            continue

        ############### daily, weekly, and rotate processing starts here #######################

        # if daily or weekly snapshot is turned on, set the date and tag
        if args.daily:
            expiration_date = datetime.datetime.now() + datetime.timedelta(days=1)
            expiration_tag = 'Daily'

        elif args.weekly:
            expiration_date = datetime.datetime.now() + datetime.timedelta(days=7)
            expiration_tag = 'Weekly'

        # ...tag this snapshot and set the expiration
        console.create_tags([this_snapshot.id], {'Expiration Tag': expiration_tag})
        console.create_tags([this_snapshot.id], {'Expiration': expiration_date})
        logging.info('%s: Snapshot %s will expire on %s', volume.id, this_snapshot.id, expiration_date)

    # if rotate is turned on...
    elif args.rotate:
        logging.info('%s: Checking snapshots for expiration...', volume.id)

        # ...get all the snapshots for this volume...
        snapshots = volume.snapshots()

        # ... and take a look at each one
        for snapshot in snapshots:
            logging.info('%s: Processing snapshot %s', volume.id, snapshot.id)

            # try to get the snapshot expiration date...
            try:
                expiration = datetime.datetime.strptime(snapshot.tags['Expiration'], '%Y-%m-%d %H:%M:%S.%f')
                logging.info('%s: Snapshot %s is set to expire on %s', volume.id, snapshot.id, expiration)

            # go on to the next snapshot if there is no expiration date
            except:
                logging.warn('%s: Snapshot %s has no expiration date. Skipping!', volume.id, snapshot.id)
                continue

            # if the snapshot is expired...
            if expiration < datetime.datetime.now():

                # ...try to delete it
                try:
                    logging.info('%s: Snapshot %s expired.  Attempting to delete...', volume.id, snapshot.id)
                    console.delete_snapshot(snapshot.id)
                    logging.info('%s: Snapshot %s deletion was successful! :D', volume.id, snapshot.id)

                except Exception, e:
                    logging.error('%s: Snapshot %s deletion failed. :(', volume.id, snapshot.id)
            else:
                    logging.info('%s: Snapshot %s is still fresh! :D', volume.id, snapshot.id)