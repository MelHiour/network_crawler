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

def ping_ip_threads(ips, type = 'process'):
    if type == 'process':
        with concurrent.futures.ProcessPoolExecutor(max_workers=len(ips)) as executor:
            pinger_result = list(executor.map(ping_ip_address, ips))
    elif type == 'thread':
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(ips)) as executor:
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
    print('Tryin {}, {} on {}'.format(creds[0], creds[1], host))
    try:
        with netmiko.ConnectHandler(**device_params) as ssh:
            ssh.enable()
            result = ssh.send_config_from_file(command_file)
        reconfigured = host
    except netmiko.ssh_exception.NetMikoAuthenticationException:
        reconfigured = None
        pass
    except netmiko.ssh_exception.NetMikoTimeoutException:
        reconfigured = None
        pass
    return reconfigured

def connection_maker_threads(host, creds_file, command_file):
    with open(creds_file) as file:
        creds = yaml.load(file)
    creds_product = list(itertools.product(creds['usernames'], creds['passwords']))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        grabber = list(executor.map(connection_maker, itertools.repeat(host), creds_product, itertools.repeat(command_file)))
    return grabber

def connection_maker_threads2(hosts, creds_file, command_file):
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        grabber = list(executor.map(ios_connection_establisher, hosts, itertools.repeat(creds_file), itertools.repeat(command_file)))
    return grabber

def ios_connection_establisher(host, creds_file, command_file):
    with open(creds_file) as file:
        creds = yaml.load(file)
    creds_product = list(itertools.product(creds['usernames'], creds['passwords']))
    output = {}
    for creds in creds_product:
        device_params = {'device_type': 'cisco_ios', 'ip': host, 'username': creds[0], 'password': creds[1],'secret': creds[1]}
        try:
            with netmiko.ConnectHandler(**device_params) as ssh:
                ssh.enable()
                result = ssh.send_config_from_file(command_file)
            output[host] = result
            break
        except netmiko.ssh_exception.NetMikoAuthenticationException:
            pass
    return output

def devices_from_file(device_file):
    with open(device_file) as file:
        result = file.read().split('\n')
    return result[0:-1]

if __name__ == '__main__':
    devices = devices_from_file('devices')
    ip_list = ping_ip_threads(devices)
    result = connection_maker_threads2(ip_list['alive'], 'creds.yml', 'commands')
    pprint(result)
