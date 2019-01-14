from ncclient import manager

conn = manager.connect(host='192.168.0.23', port='830', username='netconf', password='Netconf!', timeout=10, device_params={'name':'junos'},hostkey_verify=False)

result = conn.command('show version', format='text')
conn.close_session()
print(result.xpath('output')[0].text)

