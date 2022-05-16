import socket
import threading
import argparse
import sys
import ipaddress
from dns import resolver, reversename
from subprocess import Popen, PIPE
import typing

parser = argparse.ArgumentParser()
parser.add_argument("--target", "-t", type=str, required=True)
parser.add_argument("--ports", "-p", type=str)
parser.add_argument("--quick", "-q", action="store_true")

#args = parser.parse_args()

class Scanner:
    def __init__(self):
        pass

    def dns_lookup(self, ip_to_search):
        names = []
        dns_resolver = resolver.Resolver()
        nameserver = dns_resolver.nameservers[0]
        for ip in ip_to_search:
            try:
                address = reversename.from_address(str(ipaddress.IPv4Address(ip)))
                name = str(resolver.resolve(address, "PTR")[0])
                names.append(str(ipaddress.IPv4Address(ip)))
                names.append(name)
            except:
                names.append(str(ipaddress.IPv4Address(ip)))
                names.append(str(ipaddress.IPv4Address(ip)))
                continue
        return names

    def ping_scan(self, ip_to_ping: list) -> list:
        host_states = []
        commands = [["ping", "-n", "1", "-w", "200", str(ipaddress.IPv4Address(ip))] for ip in ip_to_ping]
        procs = [Popen(i, stderr=PIPE, stdout=PIPE) for i in commands]
        for i, p in enumerate(procs):
            p.wait()
            host_states.append(str(ipaddress.IPv4Address(ip_to_ping[i])))
            host_states.append(p.returncode)
        states_dict = {host_states[i]: host_states[i + 1] for i in range(0, len(host_states), 2)}
        print(states_dict)



# Testing
c = Scanner()

start_ip = ipaddress.IPv4Address("192.168.254.1")
end_ip = ipaddress.IPv4Address("192.168.254.254")

ips = [i for i in range(int(start_ip), int(end_ip + 1))]


c.ping_scan(ips)



