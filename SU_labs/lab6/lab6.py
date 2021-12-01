import socket
import select
import sys
from _thread import *

class lab6(object):
    def __init__(self, host_addr, su_name):
        self.host_addr = host_addr
        self.su_name = su_name

    def run():
        
if __name__ == '__main__':
    peers = []

    if not 3 <= len(sys.argv) <= 4:
        print("Usage: python lab2.py host_ip, host_port, [client || server]")
        exit()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if sys.argv[3] == "client":
            my_IP_address = str(sys.argv[1])
            my_port = int(sys.argv[2])

