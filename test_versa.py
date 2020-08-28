import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json
from multiprocessing import Process


def hit_to_controller(ii):
    urls = "https://10.133.228.15:9182/vnms/sdwan/workflow/orgs/org/"
    s=requests.Session()
    s.verify=False

    datas = {"versanms.sdwan-org-workflow": {"globalId":int(ii),
             "ikeAuthType":"psk",
             "orgName":"test{}".format(ii),
             "sharedControlPlane":False,
             "vrfs":[{"name":"test{}-LAN-VR".format(ii),
             "enableVPN":True,
             "description":"created by python script",
             "mode":"create",
             "id":int(ii)}],
             "controllers":["CTLR-TCL-IN-01-MUM","CTLR-TCL-IN-02-CHN"],"parentOrg":"TCL_Matrix_Lab"}
            }
    print(datas)
    headers1 = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    username = "ssp_user"
    password = "Tata@1234"
    xyz = s.post(url=urls,auth=(username,password),headers=headers1,data=json.dumps(datas))
    print(xyz)
    print(xyz.text)
    urls_deploy = "https://10.133.228.15:9182/vnms/sdwan/workflow/orgs/org/deploy/test{}".format(ii)
    print(urls_deploy)
    xyz = s.post(url=urls_deploy,auth=(username,password),headers=headers1)
    print(xyz)
    print(xyz.text)
    print("completed {}".format(ii))

if __name__ == '__main__':
    for ii in range(1,3):
        p = Process(target=hit_to_controller, args=(ii,))
        p.start()
        print("started {}".format(ii))
    print("Execution Completed")
