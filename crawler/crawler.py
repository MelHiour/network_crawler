import argparse
from pprint import pprint
import crawler_modules as cr

parser = argparse.ArgumentParser(description="Crawler")
device_group = parser.add_mutually_exclusive_group()
device_group.add_argument('-d', '--devices',
                    action='store', dest='device_file', help='Path to device file')
device_group.add_argument('-l', '--list',
                    action='store', dest='device_list', help='List of IP addresses')
ping_group = parser.add_mutually_exclusive_group()
ping_group.add_argument('--ping',
                    action='store_true', dest='ping', help='Enable ping test(default)')
ping_group.add_argument('--no-ping',
                    action='store_false', dest='ping', help='Skip ping test')
parser.add_argument('-c', '--creds',
                    action='store', dest='creds_file', required=True, help='Path to file with credentials')
parser.add_argument('-r', '--commands',
                    action='store', dest='command_file', required=True, help='Path to file with comamnds list to be executed')
parser.set_defaults(ping = True)
args = parser.parse_args()

if args.device_list:
    devices = [i for i in args.device_list.split(',')]
else:
    devices = cr.devices_from_file(args.device_file)
ßif not args.ping:
    result = cr.connect_and_send_parallel(devices, args.creds_file, args.command_file)
else:
    ip_list = cr.ping_ip_addresses(devices)
    result = cr.connect_and_send_parallel(ip_list['alive'], args.creds_file, args.command_file)
pprint(result)
