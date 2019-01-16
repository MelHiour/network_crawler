import argparse
from pprint import pprint
import crawler_modules as cr

devices = cr.devices_from_file('data/devices')
ip_list = cr.ping_ip_addresses(devices)
result = cr.connect_and_send_parallel(ip_list['alive'], 'data/creds.yml', 'data/commands')
pprint(result)
