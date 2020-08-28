import paramiko
import time
import telnetlib
import sys

def login_into_sg(var_sg,inventory_loopback_ip,inventory_vlan_no,service_id):
    print(var_sg)
    vrf = []
    xyz = bytes()
    temp_var = int(0)
    remote=paramiko.SSHClient()
    remote.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote.connect("172.31.6.73", port=22, username="kmogili",password="Kish@1234",look_for_keys=False, allow_agent=False)
    shell = remote.invoke_shell()
    time.sleep(2)
    xyz = shell.recv(9999)
    time.sleep(1)
    while True:
        if xyz.endswith(b"@mumsnmp2$"):
            print(xyz)
            break
        else:
            shell.send("\r\n")
            shell.send("\r\n")
            shell.send("\r\n")
            shell.send("\r\n")
            shell.send("\r\n")
            xyz = shell.recv(9999)
            print(xyz)
################################################################################################
    print("sg name " + var_sg)
    shell.send("telnet {}\n".format(var_sg))
    username_promt = bytes()
    time.sleep(2)
    while True:
        username_promt = shell.recv(9999)
        print(username_promt)
        time.sleep(0.5)
        byte_data_user_prompt = str(username_promt)
        if username_promt.endswith(b'Username:'):
            shell.send("monoleth\n")
            time.sleep(0.8)
            shell.send("el!F0rP@Sq\n")
            time.sleep(0.8)
            username_promt = shell.recv(9999)
            break
        elif username_promt.endswith(b'Username: '):
            shell.send("monoleth\n")
            time.sleep(0.8)
            shell.send("el!F0rP@Sq\n")
            time.sleep(0.8)
            username_promt = shell.recv(9999)
            break
        elif username_promt.endswith(b'username:'):
            shell.send("monoleth\n")
            time.sleep(0.8)
            shell.send("el!F0rP@Sq\n")
            time.sleep(0.8)
            username_promt = shell.recv(9999)
            break
        elif username_promt.endswith(b'username: '):
            shell.send("monoleth\n")
            time.sleep(0.8)
            shell.send("el!F0rP@Sq\n")
            time.sleep(0.8)
            username_promt = shell.recv(9999)
            break
        elif ("node name or service name not known" in byte_data_user_prompt) or ("timeout expired!" in byte_data_user_prompt):
            print("DNS Entry not found")
            with open("Network_Issu.csv", "a") as dns_error:
                dns_error.write("{},{},{},{},{}\n".format(service_id,"NA",var_sg,"NA","DNS Entry not found"))
            temp_var = 1
            remote.close()
            break
        elif username_promt.endswith(b'Are you sure you want to continue connecting (yes/no)? '):
            shell.send("yes\n")
            time.sleep(0.8)
        else:
            print(username_promt)
            username_promt = shell.recv(9999)
            pass
    ###############################################################
    if temp_var == 1:
        pass
    else:
        shell.send("terminal length 0\n")
        time.sleep(1)
        print("terminal command fired")
        new_new = inventory_loopback_ip.split("\n")
        print(new_new[0])
        inventory_loopback_ip_new = new_new[0]
        sectione_var_nhrp = bytes()
        shell.send("sh ip bgp vpnv4 all {}/32 | section {}\r\n".format(new_new[0],new_new[0]))
        print("sh ip bgp vpnv4 all {}/32 | section {}\r\n".format(new_new[0],new_new[0]))
        time.sleep(2.5)
        sectione_var_nhrp = shell.recv(9999)
        sectione_var_nhrp_str = str(sectione_var_nhrp)
        print(sectione_var_nhrp_str)
        if "via vrf" in sectione_var_nhrp_str:
            section_list_var = sectione_var_nhrp_str.split("\\r\\n")
            loopack_ip_from_network_line = str()
            for section in section_list_var:
                if "via vrf" in section:
                    loopack_ip_from_network_line = section
                    print(section)
                else:
                    pass
            loopback_ip_1 = loopack_ip_from_network_line.strip()
            loopback_ip_2 = loopback_ip_1.split(" ")
            FINAL_LOOPBACK_IP_FROM_NETWORK = loopback_ip_2[0]
            print("hello ip")
            print(FINAL_LOOPBACK_IP_FROM_NETWORK)
            shell.send("show ip nhrp {}\r\n".format(FINAL_LOOPBACK_IP_FROM_NETWORK))
            time.sleep(3)
            nbha_from_nework = shell.recv(9999)
            nbha_from_nework_str = str(nbha_from_nework)
            nbha_from_nework_list = nbha_from_nework_str.split("\\r\\n")
            loopack_ip_from_network = str()
            for ishu_nbha in nbha_from_nework_list:
                print(ishu_nbha)
                if "NBMA" in ishu_nbha:
                    NBMA_public_ip = ishu_nbha
                    NBMA_public_ip_1 = NBMA_public_ip.strip()
                    loopack_ip_from_network = NBMA_public_ip_1.replace("NBMA address: ","")
                    print(loopack_ip_from_network)
                else:
                    pass
            print("final wala ip")
            print(loopack_ip_from_network)
            with open("Success_Cases.csv", "a") as network_data:
                network_data.write("{},{},{},{},{}\n".format(service_id,loopack_ip_from_network,var_sg,FINAL_LOOPBACK_IP_FROM_NETWORK,"Success"))
        else:
            with open("Failed_in_loopback.csv", "a") as network_data:
                comment = "unable to find loopback ip from 'sh ip bgp vpnv4 all {}/32 | section {} command".format(inventory_loopback_ip_new,inventory_loopback_ip_new)
                network_data.write("{},{},{}\n".format(service_id,var_sg,comment))
    time.sleep(1)
    print("connection closed")
    remote.close()
    time.sleep(1)

def ip_logic(pe_ip_new):
    xyz = pe_ip_new.split('.')
    last_octad = int(xyz[3])
    find_even_odd = int(int(last_octad)%2)
    if find_even_odd == 1:
        last_octad_add = (last_octad + 1)
    else:
        last_octad_add = (last_octad - 1)
    final_ip = str("{}.{}.{}.{}".format(xyz[0],xyz[1],xyz[2],last_octad_add))
    #print(final_ip)
    return final_ip

def find_inferface(interface_sg):
    xyz_1 = str(interface_sg)
    print(type(xyz_1))
    xyz = xyz_1.split(' ')
    interface_sg_final = xyz[0]
    return interface_sg_final

def find_vrf(vrf_str):
    new_vrf_list = vrf_str.split("forwarding ")
    return new_vrf_list[1]

def find_ip_from_vrf_output(list_line):
    ip_list_tem = str(list_line)
    ip_list_final = []
    ip_address = list()
    iplist = ip_list_tem.split("* ")
    for ii in iplist:
        if "from" in ii:
            ip_list_final.append(ii)
    abcd = str(ip_list_final)
    ip_address = abcd.split(",")
    ip_ip = ip_address[0].strip('["')
    return ip_ip

def filter_wan_ip(wan_ip):
    print(wan_ip)
    print(type(wan_ip))
    wan_ip_1 = wan_ip.replace("[", "")
    wan_ip_2 = wan_ip_1.replace("]", "")
    wan_ip_3 = wan_ip_2.replace("\"", "")
    wan_ip_4 = wan_ip_3.replace("\'", "")
    wan_ip_5 = wan_ip_4.replace(" ", "")
    return wan_ip_5