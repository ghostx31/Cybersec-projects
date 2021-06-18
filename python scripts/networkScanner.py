#! /usr/bin/env python

from re import VERBOSE
import scapy.all as sc
import argparse as ap

def get_args():                                     # Def to get the IP address from the user 
    obj = ap.ArgumentParser()
    obj.add_argument("-i", "--ip", dest="address", help="Target IP / Range IP")
    opts = obj.parse_args()
    if not opts.address:
        obj.error("[-] Please mention an IP address. [-]")
    return opts

def arp_scan(ip):                                   # Def to generate ARP request
    req = sc.ARP(pdst=ip)                           #ARP request
    broadcast = sc.Ether(dst="ff:ff:ff:ff:ff:ff")   #Broadcast signal
    arp_broadcast = broadcast/req                   #Add ARP request and broadcast signal together
    ans = sc.srp(arp_broadcast, timeout=1, verbose=False)[0]  #making list answered to filter out the required part.

   
    dev_list = []
    for e in  ans:
        dev_dict = {"ip" : e[1].psrc, "mac" : e[1].hwsrc}
        dev_list.append(dev_dict) 
    return  (dev_list)

def print_res(res):                             # Def to print the output of the devices found 
    print("IP Address\t\t\tMAC Address")
    print("\n-------------------------------------------------------------------------------")
    for dev in res:
        print(dev["ip"] + "\t\t" + dev["mac"])          # Print from dictionary for ip and mac
        print("-------------------------------------------------------------------------------") 

opts = get_args()
scan_res = arp_scan(opts.address)
print_res(scan_res)
