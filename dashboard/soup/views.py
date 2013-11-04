#!/usr/bin/env python

from flask import render_template, jsonify
from soup import soup
from config import *
import libsoup
import random
import config as CONFIG

@soup.route('/')
@soup.route('/index')
def index():
    if APP_DEBUG is True: print "views:index" 
    snets = libsoup.get_subnets()
    return render('map.html', subnets = snets, conf = CONFIG)

def render(tmpl_name, **kwargs):
    if APP_DEBUG is True: print "views:render" 
    return render_template(tmpl_name, app_name=APP_NAME, **kwargs)

@soup.route('/status2/')
def status2():
    if APP_DEBUG is True: print "views:status2" 
    all_ips = {}
    subnets = libsoup.get_subnets()
    for subnet in subnets:
	if APP_DEBUG is True: print "views:status2:snet-loop" 
	snet = subnet.get_subnet()
	if APP_DEBUG is True: print "views:status2:registered" 
        registered_hosts = libsoup.get_registered_hosts(subnet)
	if APP_DEBUG is True: print "views:status2:reserved" 
        reserved_hosts = libsoup.get_reserved_hosts(subnet)
	if APP_DEBUG is True: print "views:status2:arp" 
        arp_hosts = libsoup.get_arp_hosts(subnet)
	if APP_DEBUG is True: print "views:status2:ping" 
        ping_hosts = libsoup.get_ping_hosts(subnet)
	if APP_DEBUG is True: print "views:status2:ranges" 
        ranges = libsoup.get_ip_ranges(subnet)
        for ip in subnet.get_ips():
	    if APP_DEBUG is True: print "views:status2:ip-loop" 
            range_name = "Unknown"
            if ip in ranges:
                range_name = ranges[ip]
            sip = {'address':ip, 'arp':0, 'ping':0, 'reg':0, 'range':range_name, 'warn':0, 'subnet':snet}

            if ip in registered_hosts:
                sip['reg'] = 1
            elif ip in reserved_hosts:
                sip['warn'] = 1

            if ip in arp_hosts:
                sip['arp'] = 1
            if ip in ping_hosts:
                sip['ping'] = 1
		
            all_ips[sip['address']] = sip
	    if APP_DEBUG is True: print "views:status2:ip-loop-complete" 
    return jsonify(all_ips)


@soup.route('/starrs/<ip>')
def starrs(ip):
    return "https://"+WEB_HOST+"/address/view/"+ip
