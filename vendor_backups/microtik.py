from netmiko import ConnectHandler
from datetime import datetime
from logsetup import logger
from dt_string import get_safe_dt_string

# Gives us the information we need to connect to MicroTik devices.
def backup(host, username, password):
    microtik = {
        'device_type': 'mikrotik_routeros',
        'host': host,
        'username': username,
        'password': password,
    }
    # Creates the connection to the device.
    net_connect = ConnectHandler(**microtik)
    # Gets the running configuration.
    output = net_connect.send_command_timing("export", delay_factor=40)
    # Gets and splits the hostname for the output file name.
    hostname = net_connect.find_prompt().replace('#','').replace('>','')
    if not hostname:
        hostname = net_connect.send_command("system identity print")
        hostname = hostname.split()
        hostname = hostname[1]
    # Creates the file name, which is the hostname, and the date and time.
    dt_string = get_safe_dt_string()
    fileName = "config_backup-" + hostname + "_" + dt_string
    # Creates the text file in the backup-config folder with the special name, and writes to it.
    backupFile = open("backup-config/" + fileName + ".txt", "w+")
    backupFile.write(output)
    logger.info("Outputted to " + fileName + ".txt")
    # For the GUI
    global gui_filename_output
    gui_filename_output = fileName