import socket
import time
import random
import struct
import hashlib
import binascii
import datetime


HDR_SZ = 24

def compactsize_t(n):
    if n < 252:
        return uint8_t(n)
    if n < 0xffff:
        return uint8_t(0xfd) + uint16_t(n)
    if n < 0xffffffff:
        return uint8_t(0xfe) + uint32_t(n)
    return uint8_t(0xff) + uint64_t(n)


def unmarshal_compactsize(b):
    key = b[0]
    if key == 0xff:
        return b[0:9], unmarshal_uint(b[1:9])
    if key == 0xfe:
        return b[0:5], unmarshal_uint(b[1:5])
    if key == 0xfd:
        return b[0:3], unmarshal_uint(b[1:3])
    return b[0:1], unmarshal_uint(b[0:1])


def bool_t(flag):
    return uint8_t(1 if flag else 0)


def ipv6_from_ipv4(ipv4_str):
    pchIPv4 = bytearray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0xff, 0xff])
    return pchIPv4 + bytearray((int(x) for x in ipv4_str.split('.')))


def ipv6_to_ipv4(ipv6):
    return '.'.join([str(b) for b in ipv6[12:]])


def uint8_t(n):
    return int(n).to_bytes(1, byteorder='little', signed=False)


def uint16_t(n):
    return int(n).to_bytes(2, byteorder='little', signed=False)


def int32_t(n):
    return int(n).to_bytes(4, byteorder='little', signed=True)


def uint32_t(n):
    return int(n).to_bytes(4, byteorder='little', signed=False)


def int64_t(n):
    return int(n).to_bytes(8, byteorder='little', signed=True)


def uint64_t(n):
    return int(n).to_bytes(8, byteorder='little', signed=False)


def unmarshal_int(b):
    return int.from_bytes(b, byteorder='little', signed=True)


def unmarshal_uint(b):
    return int.from_bytes(b, byteorder='little', signed=False)

def checksum(payload:bytes):
    if len(payload) == 0:
        return bytes.fromhex('5df6e0e2')
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    return checksum 



def print_message(msg, text=None):
    """
    Report the contents of the given bitcoin message
    :param msg: bitcoin message including header
    :return: message type
    """
    print('\n{}MESSAGE'.format('' if text is None else (text + ' ')))
    print('({}) {}'.format(len(msg), msg[:60].hex() + ('' if len(msg) < 60 else '...')))
    payload = msg[HDR_SZ:]
    command = print_header(msg[:HDR_SZ], checksum(payload))
    if command == 'version':
        print_version_msg(payload)
    # FIXME print out the payloads of other types of messages, too
    return command


def print_version_msg(b):
    """
    Report the contents of the given bitcoin version message (sans the header)
    :param payload: version message contents
    """
    # pull out fields
    version, my_services, epoch_time, your_services = b[:4], b[4:12], b[12:20], b[20:28]
    rec_host, rec_port, my_services2, my_host, my_port = b[28:44], b[44:46], b[46:54], b[54:70], b[70:72]
    nonce = b[72:80]
    user_agent_size, uasz = unmarshal_compactsize(b[80:])
    i = 80 + len(user_agent_size)
    user_agent = b[i:i + uasz]
    i += uasz
    start_height, relay = b[i:i + 4], b[i + 4:i + 5]
    extra = b[i + 5:]

    # print report
    prefix = '  '
    print(prefix + 'VERSION')
    print(prefix + '-' * 56)
    prefix *= 2
    print('{}{:32} version {}'.format(prefix, version.hex(), unmarshal_int(version)))
    print('{}{:32} my services'.format(prefix, my_services.hex()))
    time_str = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(unmarshal_int(epoch_time)))
    print('{}{:32} epoch time {}'.format(prefix, epoch_time.hex(), time_str))
    print('{}{:32} your services'.format(prefix, your_services.hex()))
    print('{}{:32} your host {}'.format(prefix, rec_host.hex(), ipv6_to_ipv4(rec_host)))
    print('{}{:32} your port {}'.format(prefix, rec_port.hex(), unmarshal_uint(rec_port)))
    print('{}{:32} my services (again)'.format(prefix, my_services2.hex()))
    print('{}{:32} my host {}'.format(prefix, my_host.hex(), ipv6_to_ipv4(my_host)))
    print('{}{:32} my port {}'.format(prefix, my_port.hex(), unmarshal_uint(my_port)))
    print('{}{:32} nonce'.format(prefix, nonce.hex()))
    print('{}{:32} user agent size {}'.format(prefix, user_agent_size.hex(), uasz))
    print('{}{:32} user agent \'{}\''.format(prefix, user_agent.hex(), str(user_agent, encoding='utf-8')))
    print('{}{:32} start height {}'.format(prefix, start_height.hex(), unmarshal_uint(start_height)))
    print('{}{:32} relay {}'.format(prefix, relay.hex(), bytes(relay) != b'\0'))
    if len(extra) > 0:
        print('{}{:32} EXTRA!!'.format(prefix, extra.hex()))


def print_header(header, expected_cksum=None):
    """
    Report the contents of the given bitcoin message header
    :param header: bitcoin message header (bytes or bytearray)
    :param expected_cksum: the expected checksum for this version message, if known
    :return: message type
    """
    magic, command_hex, payload_size, cksum = header[:4], header[4:16], header[16:20], header[20:]
    command = str(bytearray([b for b in command_hex if b != 0]), encoding='utf-8')
    psz = unmarshal_uint(payload_size)

    if expected_cksum is None:
        verified = ''
    elif expected_cksum == cksum:
        verified = '(verified)'
    else:
        verified = '(WRONG!! ' + expected_cksum.hex() + ')'
    prefix = '  '
    print(prefix + 'HEADER')
    print(prefix + '-' * 56)
    prefix *= 2
    print('{}{:32} magic'.format(prefix, magic.hex()))
    print('{}{:32} command: {}'.format(prefix, command_hex.hex(), command))
    print('{}{:32} payload size: {}'.format(prefix, payload_size.hex(), psz))
    print('{}{:32} checksum {}'.format(prefix, cksum.hex(), verified))
    return command
# -----------------------------------------------
# Binary encode the sub-version
def create_sub_version():
    sub_version = "/Satoshi:0.7.2/"
    return b'\x0F' + sub_version.encode()

# Binary encode the network addresses
def create_network_address(ip_address, port):
    network_address = struct.pack('>8s16sH', b'\x01', 
        bytearray.fromhex("00000000000000000000ffff") + socket.inet_aton(ip_address), port)
    return(network_address)

# Create the TCP request object
def create_message(payload):
    magic = bytes.fromhex("F9BEB4D9")
    command = "version" + 5 * "\00"
    length = struct.pack("I", len(payload))

    check = checksum(payload)
    msg = magic + bytes(command.encode("utf-8")) + length + check + payload
    return msg

# Create the "version" request payload
def create_version_message(peer_address):
    version = int32_t(70015)

    services = struct.pack("Q", 0)
    timestamp = struct.pack("q", int(time.time()))

    addr_recv_services = struct.pack("Q", 0) #services
    addr_recv_ip = struct.pack(">16s", b"127.0.0.1")
    addr_recv_port = struct.pack(">H", 8333)

    addr_trans_services = struct.pack("Q", 0) #services
    addr_trans_ip = struct.pack(">16s", b"127.0.0.1")
    addr_trans_port = struct.pack(">H", 8333)

    nonce = struct.pack("Q", random.getrandbits(64))
    user_agent_bytes = struct.pack("B", 0)
    starting_height = int32_t(0)
    relay = struct.pack("?", False)

    payload = version + services + timestamp + addr_recv_services + addr_recv_ip + addr_recv_port + addr_trans_services + addr_trans_ip + addr_trans_port + nonce + user_agent_bytes + starting_height + relay
    return create_message(payload)

def create_message_verack():
    return bytearray.fromhex("f9beb4d976657261636b000000000000000000005df6e0e2")


# ----------------------------------------------------------------------

def getblockhash(height):
    '''
    Return the block hash of the block height
    '''
    return 

def getblocks(verbosity):
    hash



if __name__ == '__main__':
    
    SU_ID = 4164917
    peer_address = '5.2.67.244'
    peer_port = 8333
    magic_value = 0xd9b4bef9
    buffer_size = 1024
    height = SU_ID % 700000

    peers = []
    peers_6 = []
    file = ""
    # filename = open('nodes_main.txt','r')
    # file = filename.readlines()
    # lines_to_print = range(0,413)
    # for index,line in enumerate(file):
    #     if (index in lines_to_print):
    #         file = line.strip().split(':')
    #         peers.append(file)
          

    
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        # for peer in peers:
        #     try:
        #         print(f"Connecting to :{peer}")
        #         s.settimeout(10)
        #         s.connect((peer[0], int(peer[1])))

        #         print("connected")
        #         s.settimeout()
        #     except OSError as err:
        #         print(f'Failed to connect: {err}')

        version_message = create_version_message(peer_address)
        verack_message = create_message_verack()

        s.connect((peer_address, peer_port))
            
        # Send message "version"
        print()
        print_message(version_message, "sending")
        s.send(version_message)
        response_data = s.recv(buffer_size)
        print_message(response_data, "recieved")
        
        # # Send message "verack"
        # #print(verack_message)
        s.send(verack_message)
        response_data = s.recv(buffer_size)
        print_message(response_data, "recieved")
        # print_message("verack", verack_message, response_data)