import argparse
from sys import argv
import socket

parser = argparse.ArgumentParser(description="""This is a very basic root DNS server program""")
parser.add_argument('port', type=int, help='This is the port to connect to the server on',action='store')
args = parser.parse_args(argv[1:])

try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[S]: Server socket created")
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()

#attach server to port
server_addr = ('', args.port)
ss.bind(server_addr)
ss.listen(1)

#print server information
host = socket.gethostname()
print("[S]: Server host name is {}".format(host))
localhost_ip = (socket.gethostbyname(host))
print("[S]: Server IP address is {}".format(localhost_ip))

#accept a client
csockid, addr = ss.accept()
print("[S]: Got a connection request from a client at {}".format(addr))

found = False

with csockid:
    while True:
        #query is recieved from client
        query = csockid.recv(512)
        query = query.decode('utf-8')
        #print(query)
        if not query:
            break
        # must search for match in DNSRS table
        for line in open("PROJI-DNSRS.txt", 'r'):
            parse_line = line.split()
            if parse_line[0].lower() == query.lower():
                csockid.sendall(line.encode('utf-8'))
                found = True
                break
        #query not in table, must return TShostname
        if not found:
            for line in open("PROJI-DNSRS.txt", 'r'):
                parse_line = line.split()
                if parse_line[2] == "NS":
                    csockid.sendall(line.encode('utf-8'))
                    break
        #reset found for next query
        found = False

#close the server socket
ss.close()
exit()