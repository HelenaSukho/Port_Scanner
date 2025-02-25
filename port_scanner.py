import socket
import json
from datetime import datetime
from time import sleep

print(f"[WELCOME TO PORT SCANNER 2025 - VERSION 0.0.4]")

#Some constant Variables like the Target IP and the Ports
SOURCE = socket.gethostbyname(socket.gethostname()) #Which IP initializes the scan
TARGET = socket.gethostbyname("scanme.nmap.org") #get own local IP | Changeable if meant to scan other IP
print(TARGET)
PORTS = [80, 21, 22, 443, 445, 8080] #most used Ports

#starting Point of the Port Scanner
def daemon_scanner():
    while True:
        for port in PORTS:
            daemon = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #establishing TCP connection on IPv4
            daemon.settimeout(2) #After two seconds of no respond cut off
            daemon_open = daemon.connect_ex((TARGET, port)) #scanning Target and Port | Output either 0 if open or Errno if closed
            daemon_service = socket.getservbyport(port) #Looking for services running on Port

            print("---------------------------------------------------------------------------------")
            if daemon_open == 0:
                port_open = f"[+]PORT {port} IS OPEN WITH SERVICE {daemon_service.upper()} RUNNING | TARGET-IP: {TARGET} | TIME: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
                print(port_open)
                try:
                    with open("Port_Scanner_Logs/daemon_logs.json", "r", encoding="utf-8") as f:
                        daemon_log = json.load(f)
                except(FileNotFoundError, json.JSONDecodeError):
                    daemon_log = {}

                if SOURCE in daemon_log:
                    daemon_log[SOURCE].append(port_open)
                else:
                    daemon_log[SOURCE] = [port_open]
                with open("Port_Scanner_Logs/daemon_logs.json", "w", encoding="utf-8") as f:
                    json.dump(daemon_log, f, indent=2)

            else:
                port_closed = f"[-]PORT {port} IS CLOSED WITH SERVICE {daemon_service.upper()} RUNNING | TARGET-IP: {TARGET} | TIME: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
                print(port_closed)
                try:
                    with open("Port_Scanner_Logs/daemon_logs.json", "r", encoding="utf-8") as f:
                        daemon_log = json.load(f)
                except(FileNotFoundError, json.JSONDecodeError):
                    daemon_log = {}

                if SOURCE in daemon_log:
                    daemon_log[SOURCE].append(port_closed)
                else:
                    daemon_log[SOURCE] = [port_closed]
                with open("Port_Scanner_Logs/daemon_logs.json", "w", encoding="utf-8") as f:
                    json.dump(daemon_log, f, indent=2)
            daemon.close()  # To cut off connection cleanly after ending scan
        print("--------120 SECONDS SLEEP--------")
        sleep(120)


daemon_scanner() #run function
