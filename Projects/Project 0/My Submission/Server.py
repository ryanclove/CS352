import argparse
from sys import argv
import socket

parser = argparse.ArgumentParser(description="""This is a very basic client program""")
parser.add_argument('-f', type=str, help='This is the source file for the strings to reverse', default='source_strings.txt',action='store', dest='in_file')
parser.add_argument('-o', type=str, help='This is the destination file for the reversed strings', default='results.txt',action='store', dest='out_file')
parser.add_argument('port', type=int, help='This is the port to connect to the server on',action='store')
args = parser.parse_args(argv[1:])

try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[s]: Server socket created")
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()

server_addr = ('', args.port)
ss.bind(server_addr)
ss.listen(1) #listening for one client, no threading, just one client

#print server info (optional)
host = socket.gethostname()
print("[S]: Server host name is {}".format(host))
localhost_ip = (socket.gethostbyname(host))
print("[S]: Server IP address is {}".format(localhost_ip))

#accept a client
csockid, addr = ss.accept()
print("[S]: Got a connection request from a client as {}".format(addr))

#send a intro message to the client, this is for the connection
with csockid:
    while True:
        data = csockid.recv(512)  #recieve info from client socket
        data = data.decode('utf-8')
        in_file = open("source_strings.txt", "r") #adapted this from reader
        in_pair = open("Pairs.txt", "r")
        srcList = []
        pairsDic = {}
        str = ""
        for lines in in_file:
            lines = lines.strip()
            srcList.append(lines)
        for line in in_pair:
            line = line.strip()
            pair = line.split(":")
            pairsDic[pair[0]] = pair[1]
        for acronym in srcList:
                if acronym in pairsDic:
                    str += pairsDic[acronym] + "\n"
                if acronym not in pairsDic:
                    str += "NOT FOUND" + "\n"
        data = str
        csockid.sendall(data.encode('utf-8')) #is having a brokenpipe error, but does send back to client

        if not data:
            break

#close the server socket
ss.close()
exit()
