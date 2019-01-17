import argparse
from pprint import pprint
import crawler_modules as cr
parse_desc= '''
Crawler Script descritopn will be here...
'''

parser = argparse.ArgumentParser(description=parse_desc)
device_group = parser.add_mutually_exclusive_group(required=True)
device_group.add_argument('-d',
                    action='store', dest='device_file', help='Path to device file')
device_group.add_argument('-l',
                    action='store', dest='device_list', help='List of IP addresses (ex. "10.10.1.2,10.10.1.3")')
ping_group = parser.add_mutually_exclusive_group()
ping_group.add_argument('--ping',
                    action='store_true', dest='ping', help='Enable ping test(default)')
ping_group.add_argument('--no-ping',
                    action='store_false', dest='ping', help='Skip ping test')
parser.add_argument('-c',
                    action='store', dest='creds_file', required=True, help='Path to file with credentials')
parser.add_argument('-r',
                    action='store', dest='command_file', required=True, help='Path to file with comamnds list to be executed')
parser.set_defaults(ping = True)
args = parser.parse_args()

if args.device_list:
    devices = [i for i in args.device_list.split(',')]
elif args.device_file:
    devices = cr.devices_from_file(args.device_file)
print(devices)
if not args.ping:
    result = cr.connect_and_send_parallel(devices, args.creds_file, args.command_file)
else:
    ip_list = cr.ping_ip_addresses(devices)
    print(ip_list)
    result = cr.connect_and_send_parallel(ip_list['alive'], args.creds_file, args.command_file)
pprint(result)
