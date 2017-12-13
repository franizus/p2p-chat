import socket
import subprocess
import shlex
import threading
import select
import sys
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
    args = shlex.split('nmap -oX ./ex.xml -p ' + str(PORT) +
                       ' ' + get_network_mask() + ' --open')
    subprocess.call(args)
    xml_content = elt.parse('ex.xml').getroot()
    for address in xml_content.iter('address'):
        PEERS_LIST.append(address.get('addr'))


def prompt():
    """Prints a prompt to the console to send messages."""
    sys.stdout.write('>>> ')
    sys.stdout.flush()


def client_thread(peer_ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((peer_ip, PORT))
    except socket.error as msg:
        print(msg)

    socket_list = [sys.stdin, client_socket]
    prompt()
    while True:
        read_sockets, write_sockets, error_sockets = select.select(
            socket_list, [], [])
        for sock in read_sockets:
            if sock != client_socket:
                msg = sys.stdin.readline()
                client_socket.send(msg.encode('ascii'))
                prompt()

    client_socket.close()


def listen_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if data:
                sys.stdout.write('\r' + data.decode('ascii'))
                prompt()
        except socket.error:
            client_socket.close()


def server_thread(server_sock):
    while 1:
        connection, address = server_sock.accept()
        print('\r' + address[0])
        if address[0] not in PEERS_LIST:
            CLIENT_THREADS.append(threading.Thread(
                target=client_thread, args=(address[0], )).start())
        CONNECTION_THREADS.append(threading.Thread(
            target=listen_client, args=(connection,)).start())

    server_sock.close()


if __name__ == "__main__":
    HOST = ''
    PORT = 8870
    PEERS_LIST = []
    CONNECTION_THREADS = []
    CLIENT_THREADS = []

    get_connected_peers()

    SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        SERVER_SOCKET.bind((HOST, PORT))
    except socket.error as msg:
        print(msg)
    SERVER_SOCKET.listen(10)
    threading.Thread(target=server_thread, args=(SERVER_SOCKET, )).start()

    if PEERS_LIST:
        for peer in PEERS_LIST:
            CLIENT_THREADS.append(threading.Thread(
                target=client_thread, args=(peer, )).start())
