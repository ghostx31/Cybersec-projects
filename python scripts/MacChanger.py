#!/usr/bin/env python 

import subprocess
import argparse as ap 
import re

def input_data():                                                       # Def to input interface and MAC address from the user. 
    objParse = ap.ArgumentParser()
    objParse.add_argument("-i", "--interface", dest="interface", help="Interface to change the MAC address. ")
    objParse.add_argument("-m", "--mac", dest="new_mac", help="The new MAC address. ")
    opts = objParse.parse_args()
    if not opts.interface:
        objParse.error("[-] Please mention an interface. ")             # Interface not passed  
    elif not opts.new_mac:      
        objParse.error("[-] Please mention a MAC address. ")            # MAC address not passed. 
    return opts

def mac_change(interface, new_mac):                                     # Def to perform the operation of changing the MAC address
    print('[+] Changing MAC address for ' + interface + " to " + new_mac) 
    subprocess.call(["ifconfig", interface, "down"]) 
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def foundMac(interface):                                                   # Def to check whether the MAC was changed as requested by the user 
    res = subprocess.check_output(["ifconfig", opts.interface])
    regex = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", res)
    if regex:
        return regex.group(0)
    else:
        print("[-] Could not read the MAC address. ") 
opts = input_data()
currMAC = foundMac(opts.interface)

print("Current MAC address = " + str(currMAC))                             # Printing current MAC address 
mac_change(opts.interface, opts.new_mac)

currMAC = foundMac(opts.interface)
if currMAC == opts.new_mac:
    print("[+] MAC address was changed to: " + opts.new_mac)                # New MAC address
    print("Calling ifconfig for " + opts.interface + " :")                  # Call ifconfig for the interface for which MAC was changed. 
    subprocess.call(["ifconfig", opts.interface])
else:
    print("[-] Could not change the MAC address. ")


