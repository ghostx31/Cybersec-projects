#! /usr/bin/env python

import scapy.all as scapy 

def ipscan(ip):
    scapy.arping(ip)

ipscan("192.168.122.1/24")