import pexpect

devices = [i for i in range(32897, 32922)]

for port in devices:
    with pexpect.spawn('telnet 192.168.0.29 {}'.format(port)) as t:
        t.sendline('\r\n')        
        t.expect('[>#]')
        print(t.before.decode('utf-8'))
        t.sendline('enable')
        t.expect('[>#]')
        print(t.before.decode('utf-8'))
        t.sendline('wr erase')
        t.expect('confirm]')
        print(t.before.decode('utf-8'))
        t.sendline('\r\n')
        t.expect('[>#]')
        print(t.before.decode('utf-8'))
        t.sendline('reload')
        t.expect('confirm]')
        print(t.before.decode('utf-8'))
        t.sendline('\r\n')
