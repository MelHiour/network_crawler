import yaml
import subprocess
import concurrent.futures
import netmiko
import itertools
from halo import Halo

dots = {"interval": 200,
        "frames": [
            ".   ",
            "..  ",
            "... ",
            "....",
            " ...",
            "  ..",
            "   .",
            "    "]}
            
def split_ip(ip):
    return tuple(int(part) for part in ip.split('.'))

def ip_sort(item):
    return split_ip(item[0])

def devices_from_file(device_file):
    with open(device_file) as file:
        result = file.read().split('\n')
    return result[0:-1]

def ping_ip_address(ip):
    pinger = subprocess.run(['ping', '-c', '2', '-n', ip], stdout=subprocess.DEVNULL)
    if pinger.returncode == 0:
        return {'alive':ip}
    else:
        return {'dead':ip}

def ping_ip_addresses(ips, limit = 30):
    with Halo(text=' | Pinging devices...', spinner=dots) as spinner:
        with concurrent.futures.ProcessPoolExecutor(max_workers=limit) as executor:
            pinger_result = list(executor.map(ping_ip_address, ips))
    spinner.stop_and_persist('DONE')
    ip_list = {'alive':[], 'dead':[]}
    for item in pinger_result:
        if 'alive' in item.keys():
            ip_list['alive'].append(item['alive'])
        else:
            ip_list['dead'].append(item['dead'])
    return ip_list

def connect_and_send(host, creds_file, command_file):
    with open(creds_file) as file:
        creds = yaml.load(file)
    creds_product = list(itertools.product(creds['usernames'], creds['passwords']))
    output = {}
    for creds in creds_product:
        device_params = {'device_type': 'cisco_ios',
                        'ip': host,
                        'username': creds[0],
                        'password': creds[1],
                        'secret': creds[1],
                        'timeout': 10}
        try:
            with netmiko.ConnectHandler(**device_params) as ssh:
                ssh.enable()
                result = ssh.send_config_from_file(command_file)
            output[host] = result
            break
        except netmiko.ssh_exception.NetMikoAuthenticationException:
            pass
        except netmiko.ssh_exception.NetMikoTimeoutException:
            output[host] = 'Timeout'
            break
    return output

def connect_and_send_serial(hosts, creds_file, command_file):
    result_list = []
    for host in hosts:
        result = connect_and_send(host, creds_file, command_file)
        result_list.append(result)
    return result_list

def connect_and_send_parallel(hosts, creds_file, command_file, limit = 30):
    with Halo(text='| Connecting to devices and sending commands...', spinner=dots) as spinner:
        with concurrent.futures.ThreadPoolExecutor(max_workers=limit) as executor:
            grabber = list(executor.map(connect_and_send,
                                        hosts,
                                        itertools.repeat(creds_file),
                                        itertools.repeat(command_file)))
        spinner.stop_and_persist('DONE')
    return grabber
