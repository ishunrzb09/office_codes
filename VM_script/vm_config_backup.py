import paramiko
import time
import os

#########################################################################################################################
def get_config():
    remote = paramiko.SSHClient()
    remote.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote.connect("192.168.1.55", 22, username="root", password="ishunrzb0912", look_for_keys=False,allow_agent=False)
    xyz = bytes()
    shell = remote.invoke_shell()
    time.sleep(0.5)
    xyz = shell.recv(9999)
    time.sleep(0.5)
    while True:
        if xyz.endswith(b":~] "):
            print(xyz)
            break
        else:
            shell.send("\r\n")
            time.sleep(0.5)
            xyz = shell.recv(9999)
    #########################################################################################################################

    shell.send("vim-cmd hostsvc/firmware/sync_config\n")
    time.sleep(0.1)
    first_command_output = shell.recv(9999)
    while True:
        if first_command_output.endswith(b":~] "):
            break
        else:
            first_command_output = shell.recv(9999)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    shell.send("vim-cmd hostsvc/firmware/backup_config\n")
    time.sleep(10)
    second_command_output = shell.recv(9999)
    while True:
        if second_command_output.endswith(b":~] "):
            print("first")
            break
        else:
            time.sleep(10)
            second_command_output = shell.recv(9999)
            print("second")
    link_for_download = str(second_command_output)
    list_link = link_for_download.split("\\r\\n")
    print(list_link)
    for x in list_link:
        if "Bundle can be downloaded at" in x:
            link_var_for_download = x
        else:
            pass
    final_link = link_var_for_download.split("Bundle can be downloaded at : ")
    final_link_to_download = str(final_link[1])
    file_name = final_link_to_download.split("/")
    for data in file_name:
        if ("-" in data) and (".tgz" not in data):
            final_file_name = data
        else:
            pass
    #print(final_file_name)
    sss = final_link_to_download.replace("*","192.168.1.55")
    xyz = os.system("wget {} --no-check-certificate\n".format(sss))
    print(sss)
    print(xyz)




if __name__ == '__main__':
    esxi_ip_addr = input("Please Enter ESXI IP address:- ")
    esxi_username = input("Please Enter ESXI Username:- ")
    esxi_password = input("Please Enter ESXi Password:- ")
    esxi_port_no = input("Please Enter ESXI SSH Port No:- ")
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    get_config(esxi_ip_addr,esxi_username,esxi_password,esxi_port_no)
    get_config()