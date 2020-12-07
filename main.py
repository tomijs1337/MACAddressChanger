#!/usr/bin/env python3

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Specify the interface.")
    parser.add_option("-m", "--mac", dest="new_mac", help="Input the new MAC address.")
    (options, arguments) = parser.parse_args()  # options - an object containing values for all options

    if not options.interface:  # checks if there is anything stored in interface "variable"
        parser.error("[-] Please specify an existing interface.")
    if not options.new_mac:  # checks if there is anything stored in new_mac "variable"
        parser.error("[-] Please enter a valid MAC address.")

    return options  # if both if statements return 'false' - that there is data stored in the options, they are returned


def change_mac(interface, new_mac):
    print("[*] Changing MAC address for interface " + interface + " to: " + new_mac)

    subprocess.call(["ifconfig", interface, "down"])  # Inputs the command "ifconfig eth0 down" into the terminal
    subprocess.call(["ifconfig", interface, "down", "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])  # Saves the ifconfig output
    mac_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode())  # searches the saved file for the MAC Address
    if mac_search_result:
        return mac_search_result.group(0)
    else:
        print("[-] Could not read MAC address. Try again.")
        exit()  # stops the code from running if no MAC Address could be read.


def compare_mac_addresses():
    if current_mac != previous_mac:
        print("[*] MAC Address was changed successfully, new MAC Address is " + current_mac)
        return 1
    else:
        print("[-] MAC Address did not get changed, because the new address is the same as the previous one.")
        return 0


options_variable = get_arguments()  # gets the arguments(variables) from options

previous_mac = get_current_mac(options_variable.interface)
print("[*] Your current MAC Address is " + str(previous_mac))

change_mac(options_variable.interface, options_variable.new_mac)

current_mac = get_current_mac(options_variable.interface)

if compare_mac_addresses() == 0:
    exit()
