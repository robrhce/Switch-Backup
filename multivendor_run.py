# All pre-installed besides Netmiko and ping3.
from csv import reader
from datetime import datetime
from netmiko import ConnectHandler
from ping3 import ping, verbose_ping
from vendor_backups import cisco_ios,cisco_asa,fortinet,huawei,juniper,microtik,vyos
import os
import locale

from logsetup import logger

# Specified CSV file for the script to grab the hosts from.
csv_name = "backup_hosts.csv"

# Checks if the folder exists, if not, it creates it.
if not os.path.exists('backup-config'):
    os.makedirs('backup-config')

# Set to user's current locale (e.g., 'en_AU', 'fr_FR', etc.)
locale.setlocale(locale.LC_TIME, '')  # Empty string means "use current system locale"

now = datetime.now()
dt_string = now.strftime("%x_%H-%M")  # %x = locale-appropriate date format

# Main function.
def run_script():
    # Imports the CSV file specified in the csv_name variable.
    with open(csv_name, 'r') as read_obj:
        csv_reader = reader(read_obj)
        list_of_rows = list(csv_reader)
        rows = len(list_of_rows)
        while rows >= 2:
            rows = rows - 1
            ip = list_of_rows[rows][0]
            vendor = list_of_rows[rows][1].lower()
            # Pings the hosts in the CSV file, successful pings move onto the else statement.
            # Unsuccessful pings go into a down_devices file.
            ip_ping = ping(ip)
            if ip_ping == None:
                #fileName = "down_devices_" + dt_string + ".txt"
                #downDeviceOutput = open("backup-config/" + fileName, "a")
                #downDeviceOutput.write(str(ip) + "\n")
                logger.info(str(ip) + " is down!")
            else:
                try:
                    # Based on user selection, run the script in the vendor_backups folder. The passed variables are hosts, username, password, and optional secret.
                    if vendor == "cisco_ios":
                        cisco_ios.backup(list_of_rows[rows][0], list_of_rows[rows][2], list_of_rows[rows][3], list_of_rows[rows][4])
                    elif vendor == "cisco_asa":
                        cisco_asa.backup(list_of_rows[rows][0], list_of_rows[rows][2], list_of_rows[rows][3], list_of_rows[rows][4])
                    elif vendor == "juniper":
                        juniper.backup(list_of_rows[rows][0], list_of_rows[rows][2], list_of_rows[rows][3])
                    elif vendor == "vyos":
                        vyos.backup(list_of_rows[rows][0], list_of_rows[rows][2], list_of_rows[rows][3])
                    elif vendor == "huawei":
                        huawei.backup(list_of_rows[rows][0], list_of_rows[rows][2], list_of_rows[rows][3])
                    elif vendor == "fortinet":
                        fortinet.backup(list_of_rows[rows][0], list_of_rows[rows][2], list_of_rows[rows][3])
                    elif vendor == "mikrotik":
                        microtik.backup(list_of_rows[rows][0], list_of_rows[rows][2], list_of_rows[rows][3])
                except Exception as e:
                    logger.exception(f"Backup failed for device {list_of_rows[rows][0]} (vendor: {vendor})")

# Asks the user what option they are going to use.
logger.info("running over the backup_hosts.csv")
# Pass the users choice to the main function.
run_script()