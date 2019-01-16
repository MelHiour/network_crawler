import argparse
from pprint import pprint
import crawler_modules as cr

parser = argparse.ArgumentParser(description="Crawler")
parser.add_argument('--devices',
                    action='store', dest='device_file', required=True, help='Path to device file')
parser.add_argument('--creds',
                    action='store', dest='creds_file', required=True, help='Path to file with credentials')
parser.add_argument('--commands',
                    action='store', dest='command_file', required=True, help='Path to file with comamnds list to be executed')
parser.add_argument('--no-ping',
                    action='store_false', dest='ping', help='Skip ping test')
parser.set_defaults(ping = True)
args = parser.parse_args()

devices = cr.devices_from_file(args.device_file)
ip_list = cr.ping_ip_addresses(devices)
result = cr.connect_and_send_parallel(ip_list['alive'], creds_file, command_file)
pprint(result)
