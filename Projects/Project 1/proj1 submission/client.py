import argparse
from sys import argv
import socket


class table_Entry:
    def __init__(self, hostname, IP_address, flag):
        self.hostname = hostname
        self.IP_address = IP_address
        self.flag = flag


# First we use the argparse package to parse the aruments
parser = argparse.ArgumentParser(description="""This is a very basic client program""")
parser.add_argument('-f', type=str, help='This is the source file with the hostname strings to be queried',
                    default='PROJI-HNS.txt', action='store', dest='in_file')
parser.add_argument('-o', type=str, help='This is the destination file for the results', default='RESOLVED.txt',
                    action='store', dest='out_file')
parser.add_argument('rsHostname', type=str, help='This is the domain name or ip address of the machine running the RS',
                    action='store')
parser.add_argument('rs_listenport', type=int, help='This is the port to connect to the rs server on', action='store')
parser.add_argument('ts_listenport', type=int, help='This is the port to connect to the ts server on', action='store')
args = parser.parse_args(argv[1:])

# attempting to connect to Root DNS server
try:
    client_sock_RS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[C]: Client->RS socket created")
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()
RS_server_addr = (args.rsHostname, args.rs_listenport)
client_sock_RS.connect(RS_server_addr)
# connected

TSconnection = False

# start queries from in_file
with open(args.out_file, 'w') as write_file:
    for line in open(args.in_file, 'r'):
        # trim leading and trailing whitespace from line
        line = line.strip()
        # now we write whatever the server tells us to the out_file
        if line:
            client_sock_RS.sendall(line.encode('utf-8'))
            answer = client_sock_RS.recv(512)
            answer = answer.decode('utf-8')
            #creates a list out of answer from RS
            parse_answer = answer.split()
            current_table_entry = table_Entry(parse_answer[0], parse_answer[1], parse_answer[2])
            #check for match, if flag is NS, must send query to TS
            if current_table_entry.flag == "NS":
                #never connected to TS, establish a connection
                if not TSconnection:
                    try:
                        client_sock_TS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        print("[C]: Client->TS socket created")
                    except socket.error as err:
                        print('socket open error: {} \n'.format(err))
                        exit()
                    TS_server_addr = (current_table_entry.hostname, args.ts_listenport)
                    client_sock_TS.connect(TS_server_addr)
                    TSconnection = True
                    #connected
                #at this point, connection to TS is established
                client_sock_TS.sendall(line.encode('utf-8'))
                response = client_sock_TS.recv(512)
                response = response.decode('utf-8')
                parse_response = response.split()
                current_table_entry.hostname = parse_response[0]
                current_table_entry.IP_address = parse_response[1]
                current_table_entry.flag = parse_response[2]
            #at this point, current table entry should be correct from RS or TS
            write_file.write(current_table_entry.hostname + ' ')
            write_file.write(current_table_entry.IP_address + ' ')
            if current_table_entry.flag == "Error:HOSTNOTFOUND":
                current_table_entry.flag = "Error:HOST NOT FOUND"
            write_file.write(current_table_entry.flag + '\n')

# close the sockets (note this will be visible to the other side)
client_sock_TS.close()
client_sock_RS.close()
exit()