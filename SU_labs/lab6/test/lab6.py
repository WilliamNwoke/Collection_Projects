"""
CPSC 5520, Seattle University
This is free and unencumbered software released into the public domain.
:Authors: Uchena
:Didn't use pickle because of extra bytes at the end of it
"""

import socket
import select
import errno
import sys

def chat_handler(node_sock):
    '''
        Function to receive chat from nodes
    '''
    try:
        chat_header = node_sock.recv(BUF_SZ)
        if not len(chat_header):
            return False
        chat_length = int(chat_header.decode('utf-8').strip())
        return {'header': chat_header, 'data': node_sock.recv(chat_length)}
    except:
        return False
        


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('Usage: python3 lab6.py host_port, [command: server or client => |lower case| ]') 
        exit()

    BUF_SZ = 10
    Host_IP = '127.0.0.1'
    Host_Port = int(sys.argv[1])


    # Server Code
    if str(sys.argv[2]) == 'server':
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((Host_IP, Host_Port))
        server_socket.listen()
        sockets_list = [server_socket]
        nodes = {}

        print(f'Listening => Host: {Host_IP}. Port: {Host_Port}')

        while True:
            read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
            for known_node_socket in read_sockets:
                if known_node_socket == server_socket:
                    node_sock, client_address = server_socket.accept()
                    user = chat_handler(node_sock)

                    if user is False:
                        continue

                    sockets_list.append(node_sock)
                    nodes[node_sock] = user
                    print(f"{user['data'].decode('utf-8')} connected")
                else:
                    chat = chat_handler(known_node_socket)
                    if chat is False:
                        print('{} Has left'.format(nodes[known_node_socket]['data'].decode('utf-8')))

                        sockets_list.remove(known_node_socket)
                        del nodes[known_node_socket]
                        continue

                    node = nodes[known_node_socket]
                    for node_sock in nodes:
                        if node_sock != known_node_socket:
                            node_sock.send(node['header'] + node['data'] + chat['header'] + chat['data'])

            for known_node_socket in exception_sockets:
                sockets_list.remove(known_node_socket)
                del nodes[known_node_socket]
    
    
    # Client
    if sys.argv[2] == 'client':

        friendly_name = input("Username: ")

        node_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        node_sock.connect((Host_IP, Host_Port))
        node_sock.setblocking(False)

        username = friendly_name.encode('utf-8')
        header = f"{len(username):<{BUF_SZ}}".encode('utf-8')
        
        node_sock.send(header + username)
        
        while True:
            chat = input(f'{friendly_name}:  ')

            if chat:
                chat = chat.encode('utf-8')
                chat_header = f"{len(chat):<{BUF_SZ}}".encode('utf-8')
                node_sock.send(chat_header + chat)

            try:
                while True:
                    header = node_sock.recv(BUF_SZ)
                    if not len(header):
                        print('Connection closed by the server')
                        sys.exit()
                    USR_SZ = int(header.decode('utf-8').strip())
                    username = node_sock.recv(USR_SZ).decode('utf-8')

                    chat_header = node_sock.recv(BUF_SZ)

                    chat_length = int(chat_header.decode('utf-8').strip())
                    chat = node_sock.recv(chat_length).decode('utf-8')
                    print(f'{username}:  {chat}')
            except IOError as err:
                if err.errno != errno.EAGAIN:
                    if err.errno != errno.EWOULDBLOCK:
                        print('Reading error: {}'.format(str(err)))
                        sys.exit()
                continue
            except Exception as err:
                print('Reading error: '.format(str(err)))
                sys.exit()

                