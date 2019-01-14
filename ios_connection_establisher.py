# -*- coding: utf-8 -*-

import yaml
from pprint import pprint
from netmiko import ConnectHandler 

def ios_connection_establisher(host, creds_file): 
	''' 
	Trying to establishing SSH connection.  
	
	Inputs:
	host – IP or name of SSH server 
	cder_file – yaml file with dictionary 
	--- 
	usernames: 
	 - username1 
	 - username2 
	password: 
	 - password1 
	 - password2 
	
	Output:
		ssh in enable (which is a connection) in case of success
		return 	
	''' 
	
	with open(creds_file) as file:
		creds = yaml.load(file)
	pprint(creds)
	for username in usernames:
		for password in passwords:
			pprint(device_params)
			device_params = {'device_type': 'cisco_ios', 
							'ip': host,
							'username': username,
							'password': password,
							'secret': password} 
			try:
				ssh = ConnectHandler(**device_params):
				ssh.enable()
				return ssh
			except:
				print('Host {} is not reachable'.format(host))
				
				
				
