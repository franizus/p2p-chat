import socket
import subprocess
import shlex
import xml.etree.ElementTree as elt


def get_network_mask():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    ip_addr = sock.getsockname()[0]
    ip_split = ip_addr.split('.')
    net_addr = ''
    for i in range(3):
        net_addr += ip_split[i] + '.'
    net_addr += '0/24'
    return net_addr


def get_connected_peers():
    args = shlex.split('nmap -oX ./ex.xml -p ' + str(PORT) + ' ' + get_network_mask() + ' --open')
    subprocess.call(args)
    xml_content = elt.parse('ex.xml').getroot()
    for address in xml_content.iter('address'):
        PEERS_LIST.append(address.get('addr'))

def search_peers():
    get_connected_peers()
    if PEERS_LIST:
        return True
    else:
        return False


if __name__ == "__main__":
    PORT = 8889
    PEERS_LIST = []
    print(search_peers())
    print(PEERS_LIST)
    print('fin')
