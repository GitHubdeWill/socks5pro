import socket
import select
import socks5pro
import struct
username = 'username'
password = 'password'

serversocket = socks5pro.serverinitiation(9000)
inputs = [serversocket]

def enfunc(data,key):
    return data

def defunc(data,key):
    return data


def server():
    r, w, e = select.select(inputs,[],[])
    while True:
        for event in inputs:
            if event == serversocket:
                clientsocket, clientname = event.accept()
                inputs.append(clientsocket)
                print("One socket comes,it is" + str(clientname))
            elif event == clientsocket:
                address = clientsocket.recv(6)
                new_socket = socks5pro.clientinitiation(0)
                ip = str(address[0])+"."+str(address[1])+"."+str(address[2])+"."+str(address[3])
                port = struct.unpack("!H",address[4:6])[0]
                print("The ip is: "+ip)
                print("The port is: "+ str(port))
                new_socket.connect((ip,port))
                socks5pro.exchange_loop(clientsocket,new_socket,enfunc,defunc)
server()