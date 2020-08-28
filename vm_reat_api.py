import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

s=requests.Session()
s.verify=False

username = 'administrator@vcenter.ishu.com'
password = 'ishuNRZB@1810'

s.post('https://192.168.1.65/rest/com/vmware/cis/session',auth=(username,password))

vms=s.get('https://192.168.1.65/rest/vcenter/vm')
dict_data = vms.json()
for ii in dict_data['value']:
    print(ii)


