import json
import pingparsing
from multiprocessing import Process

def ping_fun(ips,x):
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = "{}".format(ips)
    transmitter.count = 30
    result = transmitter.ping()
    xyz = json.dumps(ping_parser.parse(result).as_dict())
    xyz1 = json.loads(xyz)
    with open("output_ping.csv","a+") as output:
        output.write("{},{},{},{},{},{},{},{},{},{},{}\n".format(xyz1['destination'],xyz1['packet_transmit'],xyz1['packet_receive'],xyz1['packet_loss_count'],xyz1['packet_loss_rate'],xyz1['rtt_min'],xyz1['rtt_avg'],xyz1['rtt_max'],xyz1['rtt_mdev'],xyz1['packet_duplicate_count'],xyz1['packet_duplicate_rate'],))
    print("{},{},done\n".format(x, ips.strip()))


if __name__ == '__main__':
    with open("inventory.txt","r") as fi:
        file_data = fi.readlines()
        x = 0
        with open("output_ping.csv", "a+") as output:
            output.write("destination,packet_transmit,packet_receive,packet_loss_count,packet_loss_rate,rtt_min,rtt_avg,rtt_max,rtt_mdev,packet_duplicate_count,packet_duplicate_rate\n")
        for list_ips in file_data:
            x = x+1
            p = Process(target=ping_fun, args=(list_ips,x))
            p.start()
        print("completed1")
