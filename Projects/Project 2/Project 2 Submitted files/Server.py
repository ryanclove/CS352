import argparse
import socket
from sys import argv
import struct
import binascii

#temp host holder
Host = ''
#get the port from aguments given
parser = argparse.ArgumentParser(description="""This is a Server program""")
parser.add_argument('port', type=int, help='this is the port to connect to the server on', action='store')
args = parser.parse_args(argv[1:])
port = args.port

#try and create socket to connect to google DNS server
try:
    dns_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #in recitation
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()

#connect to google DNS server
dns_addr = ('8.8.8.8', 53)
dns_sock.connect(dns_addr)

#connect to client
try:
    server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.err as err:
    print('socket open error: {} \n'.format(err))

server_sock.bind(('',port))
server_sock.listen(1)
newSock, serverAddress = server_sock.accept()

#decode then send as UDP packet to google DNS server
def messager(url):
    split_url = url.split('.')
    answer = ""
    for section in split_url:
        answerLen = len(section)
        if len(section) < 10:
            answerLen = '0' + str(len(section))
        answer = answer + answerLen + ""
        for character in section:
            hexi = format(ord(character), "x")
            hexi = hexi.upper()
            answer = answer + hexi + ""

    answer = answer + "0000010001"
    message = "AAAA01000001000000000000" + answer
    return message

def Answer(newData):
    temp = ''
    ptr = newData
    finish = [ptr[i:i+32] for i in range(0, len(ptr), 32)]
    #might do a check for A type message here
    for section in finish:
        section = section[-8:]
        final = [section[i:i+2] for i in range(0, len(section), 2)]
        ans = ""
        for x in final:
            x = str(int(x, 16)) + '.'
            ans = ans + x + ''
        newAnswer = ans[:-1]
        temp = temp + ' '+ newAnswer + ','
    temp = temp[:-1]
    #print(Answer)
    return temp

#first while the client and google is connected
def send_message(message):
    #send answer back to client
    newSock.sendall(message.encode('utf-8'))
    pass

while True:
    #get host name from client
    client_message = newSock.recv(256).decode('utf-8')
    if(len(client_message) == 0):
        break
    dnsMessage = messager(client_message)

    #from https://routley.io/posts/hand-writing-dns-messages/
    dns_sock.sendto(binascii.unhexlify(dnsMessage), dns_addr)
    #then retrieve the answer from google DNS server and decode, was used from recitation
    udp_internet, addr = dns_sock.recvfrom(4096)

    respond = binascii.hexlify(udp_internet).decode('utf-8')
    print('response',respond)

    length = len(dnsMessage)
    respond = respond[length:]
    print('response', respond)
    #check the type of response we are receiving
    ipv4_size = respond[4:8]
    if ipv4_size != '0001':
        messageLen = respond[22:24]
        #use the size of the message that is NOT type 'A' to remove it from the full response
        messageLen = (int(messageLen, 16)* 2) + 24
        message = respond[messageLen:]
        message = Answer(message)
        message = ' other,' + message
        send_message(message)
    else:
        message = Answer(respond)
        send_message((message))

#disconnect from client and google DNS
server_sock.close()
exit()
