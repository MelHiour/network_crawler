import pexpect
import concurrent.futures

devices = [i for i in range(32897, 32947)]
ids = [i for i in range(1,51)]

def provision(devices, ids, limit = 50):
    with concurrent.futures.ThreadPoolExecutor(max_workers=limit) as executor:
        executor.map(zero_provisioning, devices, ids)

def zero_provisioning(port, id):
    with pexpect.spawn('telnet 192.168.0.29 {}'.format(port)) as t:
        print('Provisioning R{} via port {}'.format(id, port))
        t.sendline()
        t.expect('no]:')
        t.sendline('no')
        t.expect('Press RETURN to get started!')
        t.sendline('\r\n')
        t.expect('[>#]')
        t.sendline('enable')
        t.expect('[>#]')
        t.sendline('conf t')
        t.expect('[>#]')
        t.sendline('no service config')
        t.expect('[>#]')
        t.sendline('hostname R{}'.format(id))
        t.expect('[>#]')
        t.sendline('interface e0/0')
        t.expect('[>#]')
        t.sendline('no shutdown')
        t.expect('[>#]')
        t.sendline('ip address 192.168.30.{} 255.255.255.0'.format(id))
        t.expect('[>#]')
        t.sendline('username melhiour secret melhiour')
        t.expect('[>#]')
        t.sendline('enable secret melhiour')
        t.expect('[>#]')
        t.sendline('ip route 0.0.0.0 0.0.0.0 192.168.30.254')
        t.expect('[>#]')
        t.sendline('line vty 0 4')
        t.expect('[>#]')
        t.sendline('login local')
        t.expect('[>#]')
        t.sendline('transport input ssh telnet')
        t.expect('[>#]')
        t.sendline('ip domain-name py.hi')
        t.expect('[>#]')
        t.sendline('crypto key generate rsa modulus 2048')
        t.expect('[>#]')
        t.sendline('end')
        t.expect('[>#]')
        t.sendline('wr')
        t.expect('[>#]')

provision(devices, ids)
    
