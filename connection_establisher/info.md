Goals:
    • Find an appropriate credentials and send some commands for IOS devices. 
    • Multithreading/multiprocessing option
    • Create a device list with unique credentials 
    • Securely get a connection to device

Needed:
1. File with devices
2. File with credentials

Steps:
1. Get list of devices from file by devices_from_file
    input:  device file
    output: device list
2. Ping all devices by ping_ip_address(linear) or ping_ip_threads(multiprocessing)
    input:  ip or ip list
    output: available ip or ip list 
