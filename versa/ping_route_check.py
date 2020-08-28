import requests
import json
import smtplib
import time
import paramiko


post_url = 'http://10.81.80.13:8000/webhook/'
basicAuthCredentials = ('Administrator', 'Admin@321@#')
header= {"Content-Type": "application/json",
"Accept" :  "application/json", }
url = "https://100.64.14.23:9182/api/config/nms/provider/appliances/appliance"
response = requests.get(url,auth=basicAuthCredentials,headers = header ,verify=False)
y=json.loads(response.text)
x=json.dumps(y)
print(type(y))

ip_list = []

for data in y['appliance']:
	for new_data, values in data.items():
		if 'ip-address' in new_data:
			ip_list.append(values)

remote=paramiko.SSHClient()
remote.set_missing_host_key_policy(paramiko.AutoAddPolicy())
remote.connect("10.81.80.221", port=22, username="admin",password="versa123",look_for_keys=False, allow_agent=False)    
shell = remote.invoke_shell()
time.sleep(1)
xyz = shell.recv(9999)
print(xyz)
for ip in ip_list:
	shell.send("ssh admin@%s" % (ip))
	shell.send('\r\n')
	time.sleep(1)
	password_prompt = shell.recv(9999)
	print(password_prompt)
	while True:
		if password_prompt.endswith(b"password: "):
			shell.send('versa123\r\n')
			time.sleep(1)
			break
		elif password_prompt.endswith(b"password:"):
			shell.send('versa123\r\n')
			time.sleep(1)
			break
		if password_prompt.endswith(b"continue connecting (yes/no)? "):
			shell.send('yes')
			shell.send('\n')
			time.sleep(1)
		else:
			password_prompt = shell.recv(9999)
			time.sleep(1)
	shell.send('cli\r\n')
	time.sleep(1)
	cli_prompt = shell.recv(9999)
	time.sleep(1)
	print(cli_prompt)
	time.sleep(1)
	print("outside")
	for ping_ip_list in ip_list:
		print("inside")
		shell.send('ping %s routing-instance Dev_OPS-Control-VR' % (ping_ip_list))
		shell.send('\r\n')
		print('ping %s routing-instance Dev_OPS-Control-VR' % (ping_ip_list))
		time.sleep(10)
		ping_response = shell.recv(9999)
		time.sleep(1)
		while True:
			print("inside while")
			print(ping_response)
			break
	print("outside while")
	print(ping_response)
	time.sleep(1)
	print("first exit command")
	shell.send("exit")
	time.sleep(1)
	shell.send("\r\n")
	time.sleep(1)
	cli_prompt = shell.recv(9999)
	time.sleep(1)
	print(cli_prompt)
	print("third exit command")
	shell.send("exit")
	time.sleep(1)
	shell.send("\r\n")
	time.sleep(1)
	cli_prompt = shell.recv(9999)
	time.sleep(1)
	print(cli_prompt)
	print("third exit command")
	shell.send("exit")
	time.sleep(1)
	shell.send("\r\n")
	time.sleep(1)
	cli_prompt = shell.recv(9999)
	time.sleep(1)
	print(cli_prompt)

print("task completed... yahoo..!!!")
