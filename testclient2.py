import socket
import select
import socks5pro
import struct

def enfunc(data,key):
    return data

def defunc(data,key):
    return data
	
username = 'username'
password = 'password'

local = socks5pro.serverinitiation(9011)
server = socks5pro.clientinitiation(0)
client,junk = local.accept()
server.connect(("127.0.0.1",9000))
socks5pro.server(client,server,enfunc,defunc)
socks5pro.exchange_loop(client,server,enfunc,defunc)


