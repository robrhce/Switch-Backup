from netmiko import ConnectHandler
from datetime import datetime
from logsetup import logger
from dt_string import get_safe_dt_string

# Gives us the information we need to connect to Fortinet devices.
def backup(host, username, password):
    fortinet = {
        'device_type': 'fortinet',
        'host': host,
        'username': username,
        'password': password
    }
    # Creates the connection to the device.
    net_connect = ConnectHandler(**fortinet)
    net_connect.enable()
    # Gets the running configuration.
    output = net_connect.send_command("show")

    # Creates the file name, which is the hostname, and the date and time.
    hostname = net_connect.find_prompt().replace('#','').replace('>','')
    dt_string = get_safe_dt_string
    if not hostname:
        hostname = host
        fileName = host + "_" + dt_string
    else:
        fileName = hostname + "_" + dt_string
    # Creates the text file in the backup-config folder with the special name, and writes to it.
    backupFile = open("backup-config/" + fileName + ".txt", "w+")
    backupFile.write(output)
    logger.info("Outputted to " + fileName + ".txt!")
    # For the GUI
    global gui_filename_output
    gui_filename_output = fileName



def collect_runtime_info(host, username, password):
    fortinet = {
        'device_type': 'fortinet',
        'host': host,
        'username': username,
        'password': password
    }
    # Creates the connection to the device.
    net_connect = ConnectHandler(**fortinet)
    net_connect.enable()
    # Gets the running configuration.
    output = net_connect.send_command("show")

    # Creates the file name, which is the hostname, and the date and time.
    hostname = net_connect.find_prompt().replace('#', '').replace('>', '')
    if not hostname:
        hostname = host

    commands = {
        "version": "get system status",                                # Includes time and uptime
        "ntp": "diagnose sys ntp status",
        "lldp_neighbors_summary": "get switch lldp neighbors-summary",
        "lldp_neighbors_detail": "get switch lldp neighbors-detail",
        "mac_table": "diagnose switch mac-address list",
        "arp": "get system arp",
        "interface_status": "get switch physical-port",
        "interfaces": "get system interface"
    }

    output_lines = []
    for label, cmd in commands.items():
        output_lines.append(f"\n\n--- {cmd} ---\n")
        output_lines.append(net_connect.send_command(cmd))

    fileName = f"{hostname}_runtime_{dt_string}.txt"
    
    with open("backup-config/" + fileName, "w+") as f:
        f.write("\n".join(output_lines))

    logger.info(f"Runtime info collected to {fileName}")
    return fileName