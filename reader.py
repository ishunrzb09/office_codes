import datetime
import os
import shutil
import newip


def main_function():
    list_of_vpn_gateway = ['CLIEnterCommandsResults-INCHNACVPN01.txt', 'CLIEnterCommandsResults-INCHNACVPN02.txt', 'CLIEnterCommandsResults-INP44ACVPN01A_SEC.txt', 'CLIEnterCommandsResults-INP44ACVPN01A.txt','CLIEnterCommandsResults-USWV1VPN02.txt','CLIEnterCommandsResults-ukl78vpn01a.txt']
    current_time = datetime.datetime.now()
    new_time=current_time.strftime("%Y:%m:%d:%H:%M")
    for vpn_box_name in list_of_vpn_gateway:
        print(new_time)
        issue_count = int(0)
        success_count = int(0)
        temp_data_for_total_count = list()
        if os.path.exists('/Users/gauravsingh/Desktop/mail_files/input_data_from_server/{}'.format(vpn_box_name)):
            with open('/Users/gauravsingh/Desktop/mail_files/input_data_from_server/{}'.format(vpn_box_name), 'rb') as fhdl:
                raw_email = fhdl.read()
        else:
            continue
        str_email_data = str(raw_email)
        list_data_mail = str_email_data.split("\\r\\n")
        for xyz in list_data_mail:
            if xyz.startswith("Username:"):
                temp_data_for_total_count.append(xyz)
            else:
                pass
        total_calls = len(temp_data_for_total_count)
        for ii in list_data_mail:
            if ii.startswith("Username:"):
                row_data = ii
                splited_data = row_data.split("|")
                checked_minuts = check_minutes(splited_data[10])
                if checked_minuts <= 30:
                    issue_count = issue_count+1
                    final_vpn_name,final_username_ste,final_tg_ste,final_ip_ste,final_login_ste,final_duration_ste,public_ip = filter_actual_data(vpn_box_name,splited_data[0],splited_data[2],splited_data[3],splited_data[9],splited_data[10],splited_data[4])
                    ip_details_raw = newip.ip_details(public_ip)
                    with open('/Users/gauravsingh/Desktop/mail_files/bad_session_data/bad_session.csv', 'a+') as output_file:
                        output_file.write("{},{},{},{},{},{},{},{},{}\n".format(final_vpn_name,new_time,final_username_ste,final_tg_ste,final_ip_ste, final_login_ste, final_duration_ste,public_ip,ip_details_raw))
                else:
                    success_count = success_count+1
                    final_vpn_name, final_username_ste, final_tg_ste, final_ip_ste, final_login_ste, final_duration_ste,public_ip = filter_actual_data(vpn_box_name, splited_data[0], splited_data[2], splited_data[3], splited_data[9], splited_data[10],splited_data[4])
                    ip_details_raw = newip.ip_details(public_ip)
                    with open('/Users/gauravsingh/Desktop/mail_files/good_session_data/good_session.csv', 'a+') as output_file:
                        output_file.write("{},{},{},{},{},{},{},{},{}\n".format(final_vpn_name,new_time,final_username_ste,final_tg_ste,final_ip_ste, final_login_ste, final_duration_ste,public_ip,ip_details_raw))
            else:
                pass

        print("proceed time==>{}--->>>total calls==>{},issue call=={},success call==>{}".format(new_time,total_calls,issue_count,success_count))
        with open('/Users/gauravsingh/Desktop/mail_files/count_of_session/outut_data.csv', 'a+') as output_file:
            output_file.write("{},{},{},{},{}\n".format(final_vpn_name,new_time,total_calls,issue_count,success_count))
        destnation_file = (new_time+"_"+vpn_box_name)
        move_files(vpn_box_name,destnation_file)

def move_files(src_file_name,dest_file_name):
    shutil.move('/Users/gauravsingh/Desktop/mail_files/input_data_from_server/{}'.format(src_file_name),'/Users/gauravsingh/Desktop/mail_files/proceed_files/{}.txt'.format(dest_file_name))

def check_minutes(minutes_in_string):
    find_values = minutes_in_string.split("Duration: ")
    if 'd' in find_values[1]:
        temp_day = find_values[1].split("d ")
        day = temp_day[0]
        temp_time = temp_day[1].split(":")
        hrs = temp_time[0].strip('h')
        minutes = temp_time[1].strip('m')
        final_minuts = int(((((int(day))*24)*60)+((int(hrs))*60)+(int(minutes))))
        return final_minuts

    else:
        temp_time_alue = str(find_values[1])
        temp_time = temp_time_alue.split(":")
        hrs = temp_time[0].strip('h')
        minutes = temp_time[1].strip('m')
        final_minuts= int((((int(hrs)) * 60) + (int(minutes))))
        return final_minuts

def filter_actual_data(vpn_gateway_name,username,tunnen_group,ip_addr,login_time,duration,public_ip):
    temp_vpn_str = vpn_gateway_name.split('-')
    temp1_vpn_str = temp_vpn_str[1].split('.')
    final_vpn_name = temp1_vpn_str[0]
##########################################################################################
    temp_username_str = username.split(':')
    temp1_username_str = temp_username_str[1].strip()
    final_username_ste = temp1_username_str
###########################################################################################
    temp_tg_str = tunnen_group.split(':')
    temp1_tg_str = temp_tg_str[1].strip()
    final_tg_ste = temp1_tg_str
############################################################################################
    temp_ip_str = ip_addr.split(':')
    temp1_ip_str = temp_ip_str[1].strip()
    final_ip_ste = temp1_ip_str
############################################################################################
    temp_login_str = login_time.split('Time:')
    temp1_login_str = temp_login_str[1].strip()
    final_login_ste = temp1_login_str
############################################################################################
    temp_duration_str = duration.split('ion:')
    temp1_duration_str = temp_duration_str[1].strip()
    final_duration_ste = temp1_duration_str
#########################################################
    return_public_ip = public_ip.split(':')
    final_public_ip = return_public_ip[1]

    return final_vpn_name,final_username_ste,final_tg_ste,final_ip_ste,final_login_ste,final_duration_ste,final_public_ip

if __name__ == '__main__':
    main_function()
