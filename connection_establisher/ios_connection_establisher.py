# -*- coding: utf-8 -*-

import yaml
import subprocess
from pprint import pprint
from concurrent.futures import ProcessPoolExecutor
import netmiko 

def ping_ip_address(ip):
    pinger = subprocess.run(['ping', '-c', '3', '-n', ip], stdout=subprocess.DEVNULL)
    if pinger.returncode == 0:
        return {'alive':ip}
    else:
        return {'dead':ip}

def ping_ip_threads(ips, limit=10):
    with ProcessPoolExecutor(max_workers=limit) as executor:
        pinger_result = list(executor.map(ping_ip_address, ips))
    ip_list = {'alive':[], 'dead':[]}
    for item in pinger_result:
        if 'alive' in item.keys():
            ip_list['alive'].append(item['alive'])
        else:
            ip_list['dead'].append(item['dead'])
    return ip_list

def ios_connection_establisher(host, creds_file): 
    with open(creds_file) as file:
        creds = yaml.load(file)
    for username in creds['usernames']:
        for password in creds['passwords']:
            device_params = {'device_type': 'cisco_ios', 'ip': host, 'username': username, 'password': password,'secret': password}
            try:
                ssh = netmiko.ConnectHandler(**device_params)
                ssh.enable()
                return ssh
            except netmiko.ssh_exception.NetMikoTimeoutException:
                print('Host {} is not reachable with {} and {}'.format(host, username, password))

def devices_from_file(device_file):
    with open(device_file) as file:
        result = file.read().split('\n')
        return result[0:-1]

if __name__ == '__main__':
    devices = devices_from_file('devices')
    pinger = ping_ip_threads(devices)
    print(pinger)
				
