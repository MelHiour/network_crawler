# -*- coding: utf-8 -*-

import yaml
from pprint import pprint
import netmiko 

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
        return result

if __name__ == '__main__':
    result = devices_from_file('devices')
    #result = ios_connection_establisher('192.168.0.24', 'creds.yml')
    print(result)
				
