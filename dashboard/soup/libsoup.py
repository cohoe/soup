#!/usr/bin/env python

from db import dbconn
from subnet import Subnet
from math import ceil
from config import *
from iptools import IpRangeList

def get_subnets():
    if APP_DEBUG is True: print "libsoup:nets"
    res = dbconn.execute("SELECT subnet,vlan FROM ip.subnets WHERE family(subnet) = 4 AND subnet != api.get_site_configuration('DYNAMIC_SUBNET')::cidr AND subnet IN (SELECT DISTINCT subnet FROM ip.ranges) ORDER BY vlan")
    snets = []
    for r in res.fetchall():
        r = dict(r)
        snets.append(Subnet(r['subnet'],r['vlan']))
    return snets

def get_registered_hosts(subnet):
    if APP_DEBUG is True: print "libsoup:hosts"  
    res = dbconn.execute("SELECT address FROM systems.interface_addresses WHERE address << '"+subnet.get_subnet()+"' ORDER BY address")
    ips = []
    for r in res.fetchall():
        r = dict(r)
        ips.append(r['address'])
    return ips

def get_reserved_hosts(subnet):
    #res = dbconn.execute("SELECT address FROM ip.addresses WHERE api.get_address_range(address) IN (SELECT name FROM ip.ranges WHERE subnet = '"+subnet.get_subnet()+"' AND use='RESV') ORDER BY address")
    res = dbconn.execute("SELECT name,first_ip,last_ip FROM ip.ranges WHERE use='RESV' AND subnet='"+subnet.get_subnet()+"' ORDER BY first_ip")
    ips = []
    for r in res.fetchall():
        r = dict(r)
	range = IpRangeList((r['first_ip'],r['last_ip']))
	ips += list(range.__iter__())
        #if r['address'] not in ips:
        #    ips.append(r['address'])

    return ips


def get_arp_hosts(subnet):
    if APP_DEBUG is True: print "libsoup:arp"  
    res = dbconn.execute("SELECT address FROM ip.addresses WHERE address << '"+subnet.get_subnet()+"' AND arp IS true ORDER BY address")
    arps = []
    for r in res.fetchall():
        r = dict(r)
        arps.append(r['address'])
    return arps

def get_ping_hosts(subnet):
    if APP_DEBUG is True: print "libsoup:ping"  
    res = dbconn.execute("SELECT address FROM ip.addresses WHERE address << '"+subnet.get_subnet()+"' AND ping IS true ORDER BY address")
    pings = []
    for r in res.fetchall():
        r = dict(r)
        pings.append(r['address'])
    return pings

def get_ip_ranges(subnet):
    if APP_DEBUG is True: print "libsoup:ranges"  
    res = dbconn.execute("SELECT address,api.get_address_range(address) AS range FROM ip.addresses WHERE address << '"+subnet.get_subnet()+"' ORDER BY address")
    ips = {}
    for r in res.fetchall():
        r = dict(r)
        ips[r['address']] = r['range']
    return ips
