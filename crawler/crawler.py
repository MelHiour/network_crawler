import argparse
from pprint import pprint
import crawler_modules

devices = devices_from_file('data/devices')
ip_list = ping_ip_threads(devices)
result = connection_maker_threads2(ip_list['alive'], 'data/creds.yml', 'data/commands')
pprint(result)
