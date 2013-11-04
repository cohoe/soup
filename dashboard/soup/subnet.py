#!/usr/bin/env python

from iptools import IpRangeList
from math import ceil
from config import *

class Subnet:
    
    def __init__(self, subnet, vlan):
        if APP_DEBUG is True: print "subnet:init subnet" 
        self.subnet = subnet
        self.vlan = vlan
        self.r = IpRangeList(self.subnet)

    def get_subnet(self):
        if APP_DEBUG is True: print "subnet:get_subnet" 
        return self.subnet

    def get_vlan(self):
        if APP_DEBUG is True: print "subnet:get_vlan" 
        return self.vlan

    def get_ips(self):
        if APP_DEBUG is True: print "subnet:get_ips" 
        return list(self.r.__iter__())
    
    def get_ip_count(self):
        if APP_DEBUG is True: print "subnet:get_ip_count" 
        return len(self.get_ips())

    def get_display_columns(self):
        if APP_DEBUG is True: print "subnet:get_display_columns" 
        return int(ceil(self.get_ip_count()/float(DISPLAY_HOSTS_PER_COL)))
    def get_subnet_url(self):
        return self.subnet.replace('/','%2F')
