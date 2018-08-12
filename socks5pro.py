import socket
import struct
import select

SOCKS_VERSION = 5

def server(socket,server,enfunc,defunc, username = "",password = "",spubkey = "",rprikey = ""):
		cert = establishanalyze(socket)
		print("The result for certification is "+ str(cert))
		if cert:
			respond = struct.pack("!BB",SOCKS_VERSION,2)
		else:
			respond = struct.pack("!BB",SOCKS_VERSION,0)	
		socket.send(enfunc(respond,spubkey))
		if (cert == False) or (cert and certnick(defunc(socket.recv(2),rprikey),socket,username,password)):
			data = defunc(socket.recv(8),rprikey)
			new_socket = dataconnect(data,socket,server)



def local(ssocket,enfunc,defunc,ADDRESS,PORT,username = "",password = "",spubkey = "",rprikey = ""):
    ssocket.send(b'\x05\x01\x02')
    method = ssocket.recv(2)
    print('Method message is'+ str(method))
    if(method[1] == 2):

    	ssocket.send(b'\x05'+bytes([len(username)])+username.encode("utf-8")+bytes([len(password)])+password.encode("utf-8"))
    	success = ssocket.recv(2)
    	print("login is " + str(success))
    	if not (success[1] == 0) :

    		return False
    print("Address is: "+str(ADDRESS)+" PORT is : "+str(PORT))
    ssocket.send(b'\x05\x01\x00\x01'+ADDRESS+struct.pack("!H",PORT))
    
    
    return True

def serverinitiation(a):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.bind(('',a))
    sock.listen(10)
    return sock

def clientinitiation(a = 0):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    if not (a == 0):
        sock.bind(('',a))
    return sock

def establishanalyze(socket):
	num_of_methods = socket.recv(2)[1]
	methods = socket.recv(num_of_methods)
	certificate = False
	for method in methods:
		if method == 2:
			certificate = True
			break
	return certificate



def certnick(m,socket,username,password):
	print("Total data is"+str(m))
	correct = False
	version = m[0]
	ulen = m[1]
	cusername = socket.recv(ulen).decode('utf-8')
	plen = struct.unpack("!B",socket.recv(1))[0]
	cpasswd = socket.recv(plen)
	print("The original data is "+ str(cpasswd))
	cpasswd = cpasswd.decode('utf-8')
	print("The username is "+str(cusername))
	print("The password is " + str(cpasswd))
	if (cusername == username) and (cpasswd == password):
		respond = struct.pack("!BB",SOCKS_VERSION,0)
		socket.send(respond)
		correct = True
		print('login success')
	print("certification result is "+ str(correct))
	return correct


 
def dataconnect(m,csocket,server):
	print("Dataconnect message is "+str(m) +" and the length is " + str(len(m)))
	address = str(m[4])+"."+str(m[5])+"."+str(m[6])+"."+str(m[7])
	port = csocket.recv(2)
	server.send(m[4:4+4]+port)
	bind_address = server.getsockname()
	send_address = socket.inet_aton(bind_address[0])
	send_port = struct.pack("!H",bind_address[1])
	send = b'\x05\x00\x00\x01'+send_address+send_port
	csocket.send(send)

def exchange_loop(client, remote,enfunc,defunc,spubkey = "",rprikey = ""):
    while True:
        r, w, e = select.select([client, remote], [], [])
        
        if client in r:
            data = defunc(client.recv(4096),rprikey)
            print("From Direction: LEFT")
            if remote.send(enfunc(data,spubkey)) <= 0:
            	break
            else:
                print("Send To Right")

        if remote in r:
            data = defunc(remote.recv(4096),rprikey)
            print("From Direction: RIGHT")
            if client.send(enfunc(data,spubkey)) <= 0:
                break
            else:
                print("Send To Left")    
