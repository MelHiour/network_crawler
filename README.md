## Network crawler

A small script with a big name.
How to send several commands to some devices if you do not know exact credential pair? This script is responding to this challenge.

### Usage
```
$ python crawler.py -h
usage: crawler.py [-h] (-d DEVICE_FILE | -l DEVICE_LIST) -c CREDS_FILE -r
                  COMMAND_FILE [-t CONNECT_THREADS] [-p PING_PROCESS]
                  [--ping | --no-ping] [--debug | --no-debug]
                  [--brief | --no-brief]


optional arguments:
  -h, --help          show this help message and exit
  -d DEVICE_FILE      Path to device file
  -l DEVICE_LIST      List of IP addresses (ex. "10.10.1.2, 10.10.1.3")
  -c CREDS_FILE       Path to file with credentials
  -r COMMAND_FILE     Path to file with comamnds list to be executed
  -t CONNECT_THREADS  The amount of simultanious SSH connections (30 by default)
  -p PING_PROCESS     The amount of ping processes (30 by default)
  --ping              Enable ping test (default)
  --no-ping           Skip ping test
  --debug             Enable debug.yml
  --no-debug          Disable debug.yml (default)
  --brief             Enable brief output with summary information
  --no-brief          Returning output of commands per device (default)
```

### Catalog structure

### Execution examples
Try to exhaust the list of credentials data/creds.yml on all devices from file data/devices and run commands specified in data/commands 
```
python crawler.py -d data/devices -c data/creds.yml -r data/commads
```

Specify the list of devices insted of file.
```
python crawler.py -l "192.168.0.1, 192.168.0.2" -c data/creds.yml -r data/commads
```

Same as above but excluding ping check.
```
python crawler.py -l "192.168.0.1, 192.168.0.2" -c data/creds.yml -r data/commads --no-ping
```

Brief output instead of full output table.
```
python crawler.py -l "192.168.0.1, 192.168.0.2" -c data/creds.yml -r data/commads --no-ping --brief
```

Creating debug.yml file with some usefull information (could be easily parsed) 
```
python crawler.py -l "192.168.0.1, 192.168.0.2" -c data/creds.yml -r data/commads --no-ping --brief
```

### Requirments
1. The script is currently supporting only Cisco IOS devices.

### Limitation
