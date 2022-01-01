import socket
import select
import sys
import pickle
from _thread import *

'''
Constants
'''
def clientthread(conn, addr):
	conn.send(b"Welcome to this chatroom!")

	while True:
			try:
				message = conn.recv(2048)
				if message:
					print ("<" + addr[0] + "> " + message)

					# broadcast message to all
					message_to_send = "<" + addr[0] + "> " + message
					broadcast(message_to_send, conn)
				else:
					remove(conn)
			except:
				continue

def broadcast(message, connection):
	for clients in list_of_clients:
		if clients!=connection:
			try:
				clients.send(message)
			except:
				clients.close()
				remove(clients)

def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)

def start_a_server():
    sock = socket.socket()
    sock.bind((IP_address, Port))
    sock.listen()
    sock.setblocking(False)
    return sock, sock.getsockname
     
if __name__ == '__main__':
    peers = []
    list_of_clients = []


    if (len(sys.argv) in range(3,4)):
        print("Usage: python lab2.py my_ip, my_port, (host_ip: if you are not the host)")
        exit()

    if len(sys.argv) == 3:
        IP_address = str(sys.argv[1])
        Port = int(sys.argv[2])
        
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((IP_address, Port))
        server.listen(10)

        while True:
            print("Waiting for connection")
            conn, addr = server.accept()


            list_of_clients.append(conn)

            # prints the address of the user that just connected
            print (addr[0] + "has joined the chat")

            # creates and individual thread for every user
            # that connects
            start_new_thread(clientthread,(conn,addr))	

    if len(sys.argv) == 4:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        IP_address = str(sys.argv[1])
        Port = int(sys.argv[2])
        server.connect((IP_address, Port))

        sockets_list = [sys.stdin, server]
        read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

        for socks in read_sockets:
            if socks == server:
                message = socks.recv(2048)
                print (message)
            else:
                message_string = sys.stdin.readline()
                message = pickle.dumps(message_string)
                server.send(b'{message}')
                sys.stdout.write("<You>")
                sys.stdout.write(message)
                sys.stdout.flush()
        server.close()