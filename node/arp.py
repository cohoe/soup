#!/usr/bin/env python

from iptools import IpRangeList
import re
import subprocess
import os

def get_actual_ips(net):
    # Make range object
    r = IpRangeList(net)
    # Generate list of all addresses
    ips = list(r.__iter__())
    # Remove the broadcast
    ips.pop()
    # Remove the network ID
    ips = ips[1:]
    # Done
    return ips

def get_system_subnet():
    net = subprocess.Popen(["ip route | grep $(ip route | grep default | cut -d ' ' -f 5) | grep link | cut -d ' ' -f 1 | head -1"],shell=True,stdout=subprocess.PIPE,stderr=None)
    netmask = net.stdout.read()
    return netmask.rstrip()

def get_system_interface(snet):
    child = subprocess.Popen(["ip route | grep "+snet+"| cut -d ' ' -f 3"],shell=True,stdout=subprocess.PIPE,stderr=None)
    iface = child.stdout.read()
    return iface.rstrip()

def parse_arp_line(line):
    #tokens = line.split(" ")
    #return tokens
    cleaned = re.sub(r'\s+',',',line)
    tokens = cleaned.split(",")
    return tokens

def get_arp(ip):
    f = open("/proc/net/arp","r")
    for line in f:
        if re.match(ip, line):
            parts = parse_arp_line(line)
            if parts[3] != "00:00:00:00:00:00":
                return parts[3]
    return False

def get_ping(ip):
    p = subprocess.call(["ping -c 1 -W 1 %s" % ip], shell=True, stdout=subprocess.PIPE)
    if p == 0:
        return True
    else:
        return False

#ips = get_actual_ips('10.101.38.0/23')

#print get_actual_ips(get_system_subnet())
#print get_actual_ips(get_system_subnet())
sys_iface = get_system_interface(get_system_subnet())

#print "ip,ping_result,arp_result,mac_address"

filename = get_system_subnet().replace('/','-')+".csv"
report = open(filename ,"w")

for ip in get_actual_ips(get_system_subnet()):
    arpres, pingres = False, False
    pingres = get_ping(ip)
    arpres = get_arp(ip)

    if arpres is False:
        mac = ""
    else:
        mac = arpres
        arpres = True
    #print ",".join([ip,str(int(pingres)),str(int(arpres)),mac])
    line = ",".join([ip,str(int(pingres)),str(int(arpres)),mac])
    line += "\n"
    report.write(line)

report.close()
