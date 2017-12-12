import nmap

nm = nmap.PortScanner()
nm.scan('172.31.99.1-254', '8555')
nm.command_line()
