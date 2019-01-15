import pexpect

devices = [i for i in range(32897, 32922)]

for port in devices:
    with pexpect.spawn('telnet 192.168.0.29 {}'.format(port)) as t:
        t.sendline()
        t.expect('no]:')
        print(t.before.decode('utf-8'))
        t.sendline('no')
        t.expect('Press RETURN to get started!')
        print(t.before.decode('utf-8'))
        t.sendline('\r\n')
        t.expect('[>#]')
        print(t.before.decode('utf-8'))
        t.sendline('enable')
        t.expect('[>#]')
        print(t.before.decode('utf-8'))
        t.sendline('conf t')
        t.expect('[>#]')
        print(t.before.decode('utf-8'))
        t.sendline('no service config')
        t.expect('[>#]')
        print(t.before.decode('utf-8'))
        t.sendline('interface e0/0')
        t.expect('[>#]')
        t.sendline('no shutdown')
        t.expect('[>#]')
        print(t.before.decode('utf-8'))
        t.sendline('ip address dhcp')
        t.expect('[>#]')
        print(t.before.decode('utf-8'))
        t.sendline('username melhiour secret melhiour')
        t.expect('[>#]')
        print(t.before.decode('utf-8'))
        t.sendline('line vty 0 4')
        t.expect('[>#]')
        print(t.before.decode('utf-8'))
        t.sendline('login local')
        t.expect('[>#]')
        print(t.before.decode('utf-8'))
        t.sendline('transport input ssh telnet')
        t.expect('[>#]')
        print(t.before.decode('utf-8'))
        t.sendline('end')
        t.expect('[>#]')
        print(t.before.decode('utf-8'))
        t.sendline('wr')
        t.expect('[>#]')
        print(t.before.decode('utf-8'))



    
