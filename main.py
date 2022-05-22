import socket
import threading
import argparse
import sys
import ipaddress
from dns import resolver, reversename
from subprocess import Popen, PIPE
import typing

# Parses commandline agruments
parser = argparse.ArgumentParser()
parser.add_argument("--target", "-t", type=str, required=True)
parser.add_argument("--ports", "-p", type=str)
parser.add_argument("--quick", "-q", action="store_true")

args = parser.parse_args()

# Scanner class
# All methods for scanning or detecting hosts are contained in this class
class Scanner:
    def __init__(self):
        pass

    # Performs a reverse DNS lookup of each IP address in ip_to_search
    # Returns a dict containing IP:Hostname key value pair
    def dns_lookup(self, ip_to_search: list) -> dict:
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
        names_dict = {names[i]: names[i + 1] for i in range(0, len(names), 2)}
        return names_dict

    # Pings each IP address in ip_to_ping
    # Returns a dict with host:state key value pairs
    def ping_scan(self, ip_to_ping: list) -> dict:
        host_states = []
        commands = [["ping", "-n", "1", "-w", "200", str(ipaddress.IPv4Address(ip))] for ip in ip_to_ping]
        procs = [Popen(i, stderr=PIPE, stdout=PIPE) for i in commands]
        for i, p in enumerate(procs):
            p.wait()
            host_states.append(str(ipaddress.IPv4Address(ip_to_ping[i])))
            host_states.append(p.returncode)
        states_dict = {host_states[i]: host_states[i + 1] for i in range(0, len(host_states), 2)}
        return states_dict

    # Will only detect hosts currently discoverable with ping
    # Pings each IP address in ip_range, then performs a dns_lookup() of each host currently discoverable
    # Returns list of IPs and hostnames
    def quick_scan(self, ip_range: list) -> list:
        up_hosts = []
        ping_result = self.ping_scan(ip_range)
        for ip in ping_result.keys():
            if ping_result[ip] == 0:
                up_hosts.append(ipaddress.IPv4Address(ip))
            else:
                continue
        dns_result = self.dns_lookup(up_hosts)
        names = [name for name in dns_result.values()]

        return up_hosts



