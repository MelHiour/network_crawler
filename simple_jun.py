from ncclient import manager
from ncclient.xml_ import new_ele, sub_ele

conn = manager.connect(host='192.168.0.23', port='830', username='netconf', password='Netconf!', timeout=10, device_params={'name':'junos'},hostkey_verify=False)

conn.lock()
config = new_ele('system')
sub_ele(config, 'host-name').text = 'vmx_test'
sub_ele(config, 'domain-name').text = 'hinet'

conn.load_configuration(config=config)
conn.validate()
commit_config = conn.commit()
print(commit_config.tostring)

conn.unlock()

result = conn.command('show configuration system', format='text')
print(result.xpath('configuration-information/configuration-output')[0][0].text)
conn.close_session()

