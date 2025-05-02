from netmiko import ConnectHandler
from datetime import datetime
from logsetup import logger
import dt_string

# Gives us the information we need to connect to Huawei devices.
def backup(host, username, password):
    huawei = {
        "device_type": "huawei",
        'host': host,
        'username': username,
        'password': password,
    }
    # Creates the connection to the device.
    net_connect = ConnectHandler (** huawei)
    net_connect.enable()
    # Gets the running configuration.
    output = net_connect.send_command("dis current-configuration")
    # Gets and splits the hostname for the output file name.
    hostname = net_connect.find_prompt().replace('#','').replace('>','')
    if not hostname:
        hostname = net_connect.send_command("dis saved-configuration | inc sysname")
        hostname = hostname.split()
        hostname = hostname[1]
    # Creates the file name, which is the hostname, and the date and time.
    fileName = hostname + "_" + dt_string
    # Creates the text file in the backup-config folder with the special name, and writes to it.
    backupFile = open("backup-config/" + fileName + ".txt", "w+")
    backupFile.write(output)
    logger.info("Outputted to " + fileName + ".txt")
    # For the GUI
    global gui_filename_output
    gui_filename_output = fileName