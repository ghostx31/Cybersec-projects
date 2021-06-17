#!/usr/bin/env python 

import subprocess
import optparse
import re

def input_data():
    objParse = optparse.OptionParser()
    objParse.add_option("-i", "--interface", dest="interface", help="Interface to change the MAC address. ")
    objParse.add_option("-m", "--mac", dest="new_mac", help="The new MAC address. ")
    (opts, args) = objParse.parse_args()
    if not opts.interface:
        objParse.error("[-] Please mention an interface. ")
    elif not opts.new_mac:
        objParse.error("[-] Please mention a MAC address. ")
    return opts

def mac_change(interface, new_mac):
    print('[+] Changing MAC address for ' + interface + " to " + new_mac) 
    subprocess.call(["ifconfig", interface, "down"]) 
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def foundMac(interface):
    res = subprocess.check_output(["ifconfig", opts.interface])
    regex = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", res)
    if regex:
        return regex.group(0)
    else:
        print("[-] Could not read the MAC address. ") 
opts = input_data()
currMAC = foundMac(opts.interface)
print("Current MAC address = " + str(currMAC)) 
mac_change(opts.interface, opts.new_mac)
currMAC = foundMac(opts.interface)
if currMAC == opts.new_mac:
    print("[+] MAC address was changed to: " + opts.new_mac)
    print("Calling ifconfig for " + opts.interface + " :")
    subprocess.call(["ifconfig", opts.interface])
else:
    print("[-] Could not change the MAC address. ")


