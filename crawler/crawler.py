import yaml
import argparse
import time
from pprint import pprint
from tabulate import tabulate
import crawler_modules as cr

start = time.time()
parse_desc= '''
Crawler Script descritopn will be here...
'''
print('\n'+'='*32+'"Network crawler" script started'+'\n'+'='*32)

parser = argparse.ArgumentParser(description=parse_desc)

device_group = parser.add_mutually_exclusive_group(required=True)
device_group.add_argument('-d',
                    action='store', dest='device_file', help='Path to device file')
device_group.add_argument('-l',
                    action='store', dest='device_list', help='List of IP addresses (ex. "10.10.1.2,10.10.1.3")')

parser.add_argument('-c',
                    action='store', dest='creds_file', required=True, help='Path to file with credentials')
parser.add_argument('-r',
                    action='store', dest='command_file', required=True, help='Path to file with comamnds list to be executed')
parser.add_argument('-t',
                    action='store', dest='connect_threads', required=False, help='The amount of simultanious connection (30 by default)')
parser.add_argument('-p',
                    action='store', dest='ping_process', required=False, help='The amount of ping processes (30 by default)')

ping_group = parser.add_mutually_exclusive_group()
ping_group.add_argument('--ping',
                    action='store_true', dest='ping', help='Enable ping test (default)')
ping_group.add_argument('--no-ping',
                    action='store_false', dest='ping', help='Skip ping test')

debug_group = parser.add_mutually_exclusive_group()
debug_group.add_argument('--debug',
                    action='store_true', dest='debug', help='Enable debug.yml')
debug_group.add_argument('--no-debug',
                    action='store_false', dest='debug', help='Disable debug.yml (default)')

brief_group = parser.add_mutually_exclusive_group()
brief_group.add_argument('--brief',
                    action='store_true', dest='brief', help='Enable brief output with summary information')
brief_group.add_argument('--no-brief',
                    action='store_false', dest='brief', help='Returning output of commands per device (default)')

parser.set_defaults(ping = True, debug = False, brief = False, connect_threads = 30, ping_process = 30)
args = parser.parse_args()

print('DONE | Arguments parsed and validated')

if args.device_list:
    devices = [i for i in args.device_list.split(',')]
    print('DONE | Processing devices from provided list "{}"'.format(args.device_list))
elif args.device_file:
    devices = cr.devices_from_file(args.device_file)
    print('DONE | Processing devices from provided file "{}"'.format(args.device_file))

if not args.ping:
    print('INFO | Skipping ping check')
    ip_list = None
    result = cr.connect_and_send_parallel(devices, args.creds_file, args.command_file, limit=int(args.connect_threads))
else:
    ip_list = cr.ping_ip_addresses(devices, limit =int(args.ping_process))
    if ip_list['alive']:
        print('INFO | There are {} alive devices noticed... Processing...'.format(len(ip_list['alive'])))
        if ip_list['dead']:
            print('WARN | These devices are dead: {}'.format(ip_list['dead']))
        result = cr.connect_and_send_parallel(ip_list['alive'], args.creds_file, args.command_file, limit=int(args.connect_threads))
    else:
        print('WARN | All devices are dead...')

if not args.brief:
    print('INFO | The following commands have been sent\n')
    print(tabulate([(key,value) for items in result for key,value in items.items()], headers = ['IP', 'OUTPUT'], tablefmt='fancy_grid'))
else:
    print('INFO | Showing summary information\n')
    brief_view = []
    for items in result:
        for key,value in items.items():
            if not 'Timeout' in value:
                brief_view.append((key, 'Succeeded'))
            else:
                brief_view.append((key, value))
    for item in ip_list['dead']:
        brief_view.append((item, 'Skipped'))
    brief_view.sort(key=cr.ip_sort)
    print(tabulate(brief_view, headers = ['IP', 'STATUS'], tablefmt='rst'))

end = time.time()
exec_time = (end - start)
pprint('Execution time: {}'.format(exec_time))

if args.debug:
    print('INFO | Writing data to debug.yml')
    with open('debug.yml', 'w') as file:
        to_yaml = {'ARGS': args, 'PINGED_IPS': ip_list, 'DEVICES': devices, 'RESULT': result, 'TIME': [start, end, exec_time]}
        yaml.dump(to_yaml, file, default_flow_style=False)
