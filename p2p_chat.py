import socket
import subprocess
import shlex
import xml.etree.ElementTree as elt


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


aux = get_ip_address().split('.')
addr = ''
for i in range(3):
    addr += aux[i] + '.'
addr += '0/24'
print(addr)

args = shlex.split("nmap -oX ./ex.xml -p 8889 172.31.99.0/24 --open")
subprocess.call(args)
content = elt.parse('ex.xml').getroot()
for address in content.iter('address'):
    print(address.get('addr'))

print('fin')
