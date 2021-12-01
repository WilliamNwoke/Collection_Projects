import lab5
import socket

peers = []
peers_6 = []
file = ""

def ipv6_to_ipv4(ipv6):
    return '.'.join([str(b) for b in ipv6[12:]])

filename = open('nodes_main.txt','r')
file = filename.readlines()
lines_to_print = range(0,465)
for index,line in enumerate(file):
    morelines = range(414,465)
    if (index in lines_to_print):
        file = line.strip().split(':')
        peers.append(file)
        

with socket.socket(socket.AF_INET6,socket.SOCK_STREAM) as s:
    # for peer in peers_6:
    try:
        # print(f"Connecting to :{}")
        s.connect(('2001:1608:1b:f9::1', 26491))

        print("connected")
    except OSError as err:
        print(f'Failed to connect: {err}')

'''
[2001:1608:1b:f9::1]:26491
[2001:470:1f1d:61f:cd1a::109]:42434
[2001:470:a:c13::2]:8333
[2001:4801:7819:74:b745:b9d5:ff10:aaec]:8333
[2001:648:2800:131:4b1f:f6fc:20f7:f99f]:8333
[2001:678:cc8::1:10:88]:20008
[2001:8f1:1404:3700:8e49:715a:2e09:b634]:9444
[2001:b07:6442:b59f:a0ec:bbc2:d46f:f3f2]:8333
[2001:da8:a0:500::224]:8333
[2002:2f5b:a5f9::2f5b:a5f9]:8885
[2002:b6ff:3dca::b6ff:3dca]:28364
[2003:a:63a:8800:211:32ff:fe9c:e46d]:8333
[2401:b140::44:130]:8333
[2405:9800:b910:5f8e:1830:f630:2cc6:88fb]:8333
[240b:10:2782:5800:dea6:32ff:feb4:6e0e]:9600
[240d:1a:791:3400:d681:d7ff:fef6:a21e]:10050
[2600:1f18:66fc:d700:9b71:f45:f3c9:c43b]:8333
[2600:1f18:66fc:d703:a57:996d:d487:c646]:8333
[2601:442:c300:124:1cc3:f70a:2d96:6cb7]:8333
[2602:ffb8::208:72:57:200]:8333
[2603:301f:1ebf:e000:e23f:49ff:fee7:7431]:8333
[2604:4500::2e06]:8112
[2604:5500:c134:4000:7285:c2ff:fe4a:e143]:32797
[2604:5500:c134:4000::3fc]:32797
[2605:ae00:203::203]:8333
[2605:c000:2a0a:1::102]:8333
[2605:f700:c0:827:225:90ff:fee3:34a6]:8333
[2607:5300:203:1214::]:8333
[2804:4640:2001:74:4548:e9da:c558:a362]:8333
[2804:d57:5537:4800:3615:9eff:fe23:d610]:8333
[2a00:1c10:2:709::217]:22220
[2a01:4f8:10a:3e62::2]:8333
[2a01:7a0:2:137c::3]:8333
[2a01:7a7:2:131b:20c:29ff:fe9a:3922]:8333
[2a01:e0a:9fb:b0e0:54f8:1901:6e83:62c1]:8333
[2a01:e0a:aa7:c8c0:9679:affa:b6e5:efc7]:8333
[2a02:120b:2c4c:e8a0:3079:809f:1c2:7ffd]:8333
[2a02:2f05:661a:2c00::1]:8333
[2a02:7aa0:1619::adc:8de0]:8333
[2a02:7b40:b905:372d::1]:8333
[2a02:810d:8cbf:f3a8:96c6:91ff:fe17:ae1d]:8333
[2a02:a311:8143:8c00::4]:8353
[2a02:e00:fff0:506::1]:8444
[2a02:e00:fff0:506::a]:8444
[2a03:b0c0:1:e0::77e:4001]:8333
[2a04:2180:0:2::aa]:8333
[2a04:52c0:101:29e::]:8333
[2a04:bc40:1dc3:8d::2:1001]:8333
[2a07:a880:4601:1062:b4b4:bd2a:39d4:7acf]:51401
[2a0a:a543:15c3:0:ba27:ebff:fee5:226e]:8333
[2a0a:c801:1:7::183]:8333
[2a10:8b40:1::103]:8335

'''