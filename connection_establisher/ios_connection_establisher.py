# -*- coding: utf-8 -*-

import yaml
import subprocess
from pprint import pprint
from tabulate import tabulate
import concurrent.futures
import netmiko 
import itertools

def ping_ip_address(ip):
    pinger = subprocess.run(['ping', '-c', '2', '-n', ip], stdout=subprocess.DEVNULL)
    if pinger.returncode == 0:
        return {'alive':ip}
    else:
        return {'dead':ip}

def ping_ip_threads(ips, limit=3, type = 'process'):
    if type == 'process': 
        with concurrent.futures.ProcessPoolExecutor(max_workers=limit) as executor:
            pinger_result = list(executor.map(ping_ip_address, ips))
    elif type == 'thread':
        with concurrent.futures.ThreadPoolExecutor(max_workers=limit) as executor:
            pinger_result = list(executor.map(ping_ip_address, ips))
    else:
        return ('Specify correct threading option. type = thread|process')
    ip_list = {'alive':[], 'dead':[]}
    for item in pinger_result:
        if 'alive' in item.keys():
            ip_list['alive'].append(item['alive'])
        else:
            ip_list['dead'].append(item['dead'])
    return ip_list

def connection_maker(host, creds, command_file):
    device_params = {'device_type': 'cisco_ios', 'ip': host, 'username': creds[0], 'password': creds[1],'secret': creds[1]}
    try:
        with netmiko.ConnectHandler(**device_params) as ssh:
            ssh.enable()
            result = ssh.send_config_from_file(command_file)
        reconfigured = host
    except netmiko.ssh_exception.NetMikoAuthenticationException:
        reconfigured = None
        pass
    return reconfigured

def connection_maker_threads(host, creds_file, command_file, limit = 3):
    with open(creds_file) as file:
        creds = yaml.load(file)
    creds_product = list(itertools.product(creds['usernames'], creds['passwords']))
    with concurrent.futures.ThreadPoolExecutor(max_workers=limit) as executor:
        grabber = list(executor.map(connection_maker, itertools.repeat(host), creds_product, itertools.repeat(command_file)))
    return grabber
        
def ios_connection_establisher(host, creds_file, command_file): 
    '''
    Trying to establish an SSH connection with single IP by different credentials with single thread.

    host = IP address
    
    creds_file:
        usernames:
        - melhiour
        - user1
        - user2
        passwords:
        - password1
        - password2
        - melhiour
    
    command_file:
        username user1 secret user1
        line vty 0
        login local 
    '''
    print('Unpacking {} file'.format(creds_file))
    with open(creds_file) as file:
        creds = yaml.load(file)
    exeption_counter = 1
    print('Starting for loops for usernames and passwords') 
    creds_product = list(itertools.product(creds['usernames'], creds['passwords']))
    for creds in creds_product:
        print('Connecting to {}'.format(host))
        print(creds)
        device_params = {'device_type': 'cisco_ios', 'ip': host, 'username': creds[0], 'password': creds[1],'secret': creds[1]}
        try:
            with netmiko.ConnectHandler(**device_params) as ssh:
                if ssh.check_config_mode():
                   print('Currently in enable mode')
                else:
                    print('Doing enable')
                    ssh.enable()
                print('Sending commands from {}'.format(command_file))
                result = ssh.send_config_from_file(command_file)
                print('The result of operations is:')
                pprint(result)
            reconfigured = host
            break
        except netmiko.ssh_exception.NetMikoAuthenticationException:
            print('NetMikoAuthenticationException accurs: {} time(s)'.format(exeption_counter))
            exeption_counter = exeption_counter + 1
            reconfigured = None
            pass
    return reconfigured

def devices_from_file(device_file):
    with open(device_file) as file:
        result = file.read().split('\n')
    return result[0:-1]

if __name__ == '__main__':
    devices = devices_from_file('devices')
    ip_list = ping_ip_threads(devices)
    with open('creds.yml') as file:
        creds = yaml.load(file)
    creds_product = list(itertools.product(creds['usernames'], creds['passwords']))
    result_list = []
    for ip in ip_list['alive']:
        result = connection_maker_threads(ip, 'creds.yml', 'commands')
        result_list.append(result)
    print(tabulate(result_list, headers = creds_product))
