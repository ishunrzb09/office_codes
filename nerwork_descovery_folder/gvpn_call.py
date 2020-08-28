import paramiko
import time
import login_sg
import os
from multiprocessing import Process


with open("inventory_data.txt","r") as file:
	inventory_data = file.readlines()
	for inventory_data_list in inventory_data:
		os.system("rm -f .ssh/known_hosts")
		direct_sgsg = str()
		xyz = inventory_data_list.split(",")
		print(xyz[0])
		print(xyz[1])
		print(xyz[2])
		print(xyz[3])
		service_id = xyz[0]
		pe_ip_address = xyz[1]
		inventory_port_no_full = xyz[2]
		inventory_loopback_ip = xyz[3]
		#inventory_vlan_no_temp =  inventory_port_no_full.split(":")
		#inventory_port_no = inventory_vlan_no_temp[0].strip()
		#inventory_vlan_no = inventory_vlan_no_temp[1].strip()
#def first_fun(service_id,pe_ip_address,inventory_port_no_full,inventory_loopback_ip):
		remote=paramiko.SSHClient()
		remote.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		remote.connect("172.31.6.73", port=22, username="kmogili",password="Tata@1234",look_for_keys=False, allow_agent=False)
		xyz = bytes()
		shell = remote.invoke_shell()
		time.sleep(0.5)
		xyz = shell.recv(9999)
		time.sleep(0.5)
		password_promt = bytes()
		while True:
			if xyz.endswith(b"@mumsnmp2$"):
				print(xyz)
				break
			else:
				print(xyz)
				shell.send("\r\n")
				shell.send("\r\n")
				shell.send("\r\n")
				shell.send("\r\n")
				shell.send("\r\n")
				time.sleep(0.5)
				xyz = shell.recv(9999)
#########################################################################################################################
		try:
			shell.send("rm -f .ssh/known_hosts\n")
			time.sleep(0.5)
			shell.send("ssh -l monoleth {}".format(pe_ip_address))
			time.sleep(2)
			shell.send("\r\n")
			password_promt = shell.recv(9999)
			while True:
				print(password_promt)
				time.sleep(0.5)
				if password_promt.endswith(b'password: '):
					shell.send("el!F0rP@Sq\n")
					time.sleep(0.8)
					break
				elif password_promt.endswith(b"Password: "):
					shell.send("el!F0rP@Sq\n")
					time.sleep(0.8)
					break
				elif password_promt.endswith(b"Password:"):
					shell.send("el!F0rP@Sq\n")
					time.sleep(0.8)
					break
				elif password_promt.endswith(b"password:"):
					shell.send("el!F0rP@Sq\n")
					time.sleep(0.8)
					break
				elif password_promt.endswith(b"continue connecting (yes/no)? "):
					print("inside yes/no")
					time.sleep(0.5)
					shell.send("yes\r\n")
					time.sleep(0.2)
					password_promt = shell.recv(9999)
					time.sleep(0.8)
				else:
					print(password_promt)
					password_promt = shell.recv(9999)
					print("else")
					print(password_promt)
		except:
			with open("error_finding_details.csv", "a") as network_data:
					remark = 'timedout'.format(service_id)
					network_data.write("{},{},{},{}\n".format(service_id,pe_ip_address,inventory_port_no_full,remark))
			print("An exception occurred")
			#continue
		print("out of try block")
		output_logs = bytes()
		while True:
			print("in side while")
			print(output_logs)
			if output_logs.endswith(b'# '):
				print("break")
				break
			elif output_logs.endswith(b'#'):
				print("break")
				break
			else:
				output_logs = shell.recv(9999)
				time.sleep(0.5)
		str_out = str(output_logs)
		str_out_1 = str_out.split("\\r\\n")
		data_logs = []
		for ii in str_out_1:
			if '#' in ii:
				print(ii)
				direct_sgsg = ii
			else:
				pass
		if "SG" in direct_sgsg:
			# pe_ip_new_1 = pe_ip_address
			# final_sg_var = direct_sgsg.split('#')
			# res = login_sg.login_into_sg(final_sg_var[0],inventory_loopback_ip,inventory_vlan_no,service_id)
			pass
		else:
			data_logs = list()
			data_logs_port = list()
			shell.send('admin display-config | match "{}" context all\n'.format(service_id))
			output_logs_1 = shell.recv(9999)
			while True:
				if output_logs_1.endswith(b"# "):
					break
				else:
					time.sleep(0.1)
					output_logs_1 = shell.recv(9999)
					data_logs.append(output_logs_1)
			str_data_logs = str(data_logs)
			list_data_logs = str_data_logs.split("\\r\\n")
			#############################################################################################################
			for gaurav in list_data_logs:
				print(gaurav)
			if len(list_data_logs) <= 2:
				service_id_status = False
			else:
				service_id_status = True

			shell.send('admin display-config | match "{}" context all\n'.format(inventory_port_no_full))
			output_logs_1_port = shell.recv(9999)
			print(output_logs_1_port)
			while True:
				if output_logs_1_port.endswith(b"# "):
					print(output_logs_1_port)
					break
				else:
					time.sleep(0.1)
					#print("while")
					#print(output_logs_1_port)
					output_logs_1_port = shell.recv(9999)
					data_logs_port.append(output_logs_1_port)
			print("out side while")
			str_data_logs_port = str(data_logs_port)
			list_data_logs_port = str_data_logs_port.split("\\r\\n")
			for gaurav1 in list_data_logs_port:
				print(gaurav1)
			if len(list_data_logs_port) <= 2:
				port_no_status = False
			else:
				port_no_status = True
##############################################################################################################
			if ((service_id_status == False) and (port_no_status == False)):
				with open("error_finding_details.csv", "a") as network_data:
					remark = 'Details not found from both service_id and inventory_port_no command'.format(service_id)
					network_data.write("{},{},{},{}\n".format(service_id,pe_ip_address,inventory_port_no_full,remark))
			elif ((port_no_status == True) and (service_id_status == False)):
				with open("error_finding_details.csv", "a") as network_data:
						remark = 'Details not found from service_id command'.format(service_id)
						network_data.write("{},{},{},{}\n".format(service_id,pe_ip_address,inventory_port_no_full,remark))	
			elif ((port_no_status == False) and (service_id_status == True)):
				with open("error_finding_details.csv", "a") as network_data:
						remark = 'Details not found from port_no command'.format(service_id)
						network_data.write("{},{},{},{}\n".format(service_id,pe_ip_address,inventory_port_no_full,remark))	
			elif ((port_no_status == True) and (service_id_status == True)):
				with open("error_finding_details.csv", "a") as network_data:
						remark = 'able to find details from both service_id and inventory_port_no command'.format(service_id)
						network_data.write("{},{},{},{}\n".format(service_id,pe_ip_address,inventory_port_no_full,remark))
			else:
				with open("error_finding_details.csv", "a") as network_data:
						remark = 'unable to handle error'.format(service_id)
						network_data.write("{},{},{},{}\n".format(service_id,pe_ip_address,inventory_port_no_full,remark))
			remote.close()

# if __name__ == "__main__": 
# 	with open("inventory_data.txt","r") as file:
# 		inventory_data = file.readlines()
# 	for inventory_data_list in inventory_data:
# 		os.system("rm -f .ssh/known_hosts")
# 		direct_sgsg = str()
# 		xyz = inventory_data_list.split(",")
# 		print(xyz[0])
# 		print(xyz[1])
# 		print(xyz[2])
# 		print(xyz[3])
# 		service_id = xyz[0]
# 		pe_ip_address = xyz[1]
# 		inventory_port_no_full = xyz[2]
# 		inventory_loopback_ip = xyz[3]
# 		# inventory_vlan_no_temp =  inventory_port_no_full.split(":")
# 		# inventory_port_no = inventory_vlan_no_temp[0].strip()
# 		# inventory_vlan_no = inventory_vlan_no_temp[1].strip()
# 		p = Process(target=first_fun, args=(service_id,pe_ip_address,inventory_port_no_full,inventory_loopback_ip))
# 		p.start()
# 	print(completed)

