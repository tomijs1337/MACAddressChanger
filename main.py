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
    # print("[*] Changing MAC address for interface " + interface + " to: " + new_mac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "down", "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    # subprocess.call(["ifconfig", interface])


def mac_read_check():
    ifconfig_result = subprocess.check_output(["ifconfig", options_variable.interface])
    mac_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode())
    if mac_search_result:
        print(mac_search_result.group(0))
        return mac_search_result
    else:
        print("[-] Could not read MAC address.")


options_variable = get_arguments()

previous_mac = mac_read_check()  # checks and outputs previous MAC Address

change_mac(options_variable.interface, options_variable.new_mac)

changed_mac = mac_read_check()  # checks and outputs MAC Address after it has been changed