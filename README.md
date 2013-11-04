SOUP
====
STARRS Online Utilization Package

Network dashboard that visually identifies what hosts are active on a network and if they are registered in STARRS. 

![alt tag](https://raw.github.com/cohoe/soup/master/screenshot.png)

How it Works
------------

Nodes sit on each VLAN in your network and periodically ping all hosts in the nodes primary subnet. The result of the ping is logged. A corresponding ARP result is also stored for each host since certain hosts can ARP but not ping. These results are dumped to a CSV file which is then transfered to the dashboard server for processing. The dashboard server parses the CSV files and updates the STARRS database accordingly.

When a user visits the Dashboard URL, data from STARRS is queried, parsed, and spit out in the pretty light graph that you see in the screenshot image above.

* Green: Host is responding to ping/arp and is registered.
* Dark Green: Host is reponding to arp only and is registered.
* Yellow: Host is reponding to ping||arp, is not registered, but is in a reserved IP range.
* Red: Host is responding to ping||arp and is not registered (BAD!).
* Gray: Host is not responding to ping||arp but is registered.
* Dark Gray: Host is not responging to ping||arp and is not registered.

Requirements
------------
* A working STARRS installation
* A dashboard server
    * python-flask
    * sqlalchemy
* Nodes
    * python-iptools

Setup & Configuration
---------------------
I'll get to this

Name Origin
-----------
A good friend (Matt Campbell) wrote a similar tool for the RIT networks. His had more software features and had a kiosk display. Matt's nickname is "soup".
