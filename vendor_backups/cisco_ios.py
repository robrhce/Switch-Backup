from netmiko import ConnectHandler
from datetime import datetime
from logsetup import logger
from dt_string import get_safe_dt_string

# Gives us the information we need to connect to Cisco devices.
def backup(host, username, password, enable_secret):
    cisco_ios = {
        'device_type': 'cisco_ios',
        'host': host,
        'username': username,
        'password': password,
        'secret': enable_secret,
    }
    # Creates the connection to the device.
    net_connect = ConnectHandler(**cisco_ios)
    net_connect.enable()
    #any reason not to use netmiko built-in func to find a hostname? Try it, and if you like it - replace everywhere. YW
    hostname = net_connect.find_prompt().replace('#','').replace('>','')
    if not hostname:
        # Gets and splits the hostname for the output file name.
        hostname = net_connect.send_command("show conf | i hostname")
        hostname = hostname.split()
        hostname = hostname[1]
    # Gets the running configuration.
    output = net_connect.send_command("show run")
    
    dt_string = get_safe_dt_string()
    # Creates the file name, which is the hostname, and the date and time.
    fileName = hostname + "_" + dt_string
    # Creates the text file in the backup-config folder with the special name, and writes to it.
    backupFile = open("backup-config/" + fileName + ".txt", "w+")
    backupFile.write(output)
    logger.info("Outputted to " + fileName + ".txt")
    # For the GUI
    global gui_filename_output
    gui_filename_output = fileName



def collect_runtime_info(host, username, password, enable_secret):
    cisco_ios = {
        'device_type': 'cisco_ios',
        'host': host,
        'username': username,
        'password': password,
        'secret': enable_secret,
    }
    net_connect = ConnectHandler(**cisco_ios)
    net_connect.enable()

    hostname = net_connect.find_prompt().replace('#','').replace('>','')
    if not hostname:
        hostname = net_connect.send_command("show run | i hostname").split()[1]




    commands = {
        "version": "show version",
        "environment": "show environment",
        "cdp_neighbors": "show cdp neighbors",
        "cdp_detail": "show cdp neighbors detail",
        "lldp_neighbors": "show lldp neighbors",
        "mac_table": "show mac address-table",
        "arp": "show arp",
        "interface_status": "show interface status",
        "interfaces": "show interfaces"
    }

    output_lines = []
    for label, cmd in commands.items():
        output_lines.append(f"\n\n--- {cmd} ---\n")
        output_lines.append(net_connect.send_command(cmd))

    # Save to file
    dt_string = get_safe_dt_string()
    fileName = f"{hostname}_runtime_{dt_string}.txt"

    with open("backup-config/" + fileName + ".txt", "w+") as f:
        f.write("\n".join(output_lines))

    logger.info(f"Runtime info collected to {fileName}")
    return fileName