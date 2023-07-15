import datetime
import dateutil.parser
import glob
import gzip
import json
import os
from datetime import timedelta
from prettytable import PrettyTable
from program_data import drv_fw
from search_strings import esxcfg_strings, vmkwarning_strings, vobd_strings, hostd_strings, ignore

# =====================================================================
#
# NetApp / SolidFire
# CPE 
# ESXi log parser
#
# =====================================================================

#============================================================        
# common tasks
class tasks():
    #============================================================
    #report header
    def header(repo, outputfile):
        table_data = []
        outputfile.write("==================== Header information ====================\n")
        table_data.append(["Management IP", "{}".format(repo.esxconf['/adv/Net/ManagementAddr'].strip())])
        table_data.append(["Management vmk", "{}".format(repo.esxconf['/adv/Net/ManagementIface'].strip())])
        table_data.append(["Host Name", "{}".format(repo.esxconf['/adv/Misc/HostName'].strip())])
        if os.path.isfile("{}/commands/vmware_-vl.txt".format(repo.directory)):
            with open("{}/commands/vmware_-vl.txt".format(repo.directory), 'r') as f:
                lines = f.readlines()
                table_data.append(["ESXi Version", "{}".format(lines[0].strip())])
                if 'ESXi 6.7' in lines[0]: repo.esx_version = 'esx_67'
                elif 'ESXi 7' in lines[0]: repo.esx_version = 'esx_7'
                elif 'ESXi 8' in lines[0]: repo.esx_version = 'esx_8'
        else:
            table_data.append(["ESXi Version", "UNKNOWN"])
        if os.path.isfile("{}/commands/localcli_system-stats-uptime-get.txt".format(repo.directory)):
            with open("{}/commands/localcli_system-stats-uptime-get.txt".format(repo.directory), 'r') as f:
                uptimelines = f.read()
                uptime = str(timedelta(microseconds=int(uptimelines)))
                table_data.append(["System Uptime", "{}".format(str(uptime.strip()))])
        else:
            table_data.append(["Uptime", "UNKNWON"])
        if os.path.isfile("{}/commands/smbiosDump.txt".format(repo.directory)):
            with open("{}/commands/smbiosDump.txt".format(repo.directory)) as f:
                platform = f.readlines()
                for line in platform:
                    if "Product" in line:
                        repo.platform = line
                        table_data.append(["Platform", "{}".format(line).strip()])
                        break
        table = PrettyTable()
        table.add_rows(table_data[0:])
        outputfile.write(str(table))
    
    #============================================================
    # See if the compute platform is NetApp
    def check_platform(repo):
        platforms = ["H300", "H500", "H700", "H410", "H610", "H615"]
        for platform in platforms:
            if platform in repo.platform:
                netapp = True
                break
            else:
                netapp = False
        return netapp
    #============================================================
    # Display driver/firmware info from IMT
    def show_drv_fw(repo, outputfile):
        outputfile.write("\n\n==================== Supported Driver/Firmware information ====================\n")
        outputfile.write("=== NetApp IMT \n\t{}\n".format(drv_fw.imt_url))
        outputfile.write("=== NetApp Firmware Realease Notes\n\t{}\n".format(drv_fw.firmware_rn["14.29.1016"]))
        outputfile.write("=== Driver downloads\n\t4.17.71.1: {}\n\t4.21.71.1: {}\n".format(drv_fw.driver_downloads["4.17.71.1"],drv_fw.driver_downloads["4.21.71.1"]))
        table_data = []
        row = []
        for key, value in drv_fw.driver_firmware.items():
            if key == repo.esx_version:
                for platform in value:
                    if platform['platform'] in repo.platform:
                        table_data.append(["{}".format(key), "Driver", "Firmware"])
                        for imt in platform['IMT']:
                            row = ["{}".format(platform['platform']), "{}".format(imt['driver']), "{}".format(imt['firmware'])]
                            table_data.append(row)
        table = PrettyTable(table_data[0])
        table.add_rows(table_data[1:])
        outputfile.write(str(table))
        
    #============================================================
    # Open a file and return contents as a list
    def open_file_return_list(filename, outputfile):
        contents = []
        if os.path.isfile(filename):
            if 'gz' in filename:
                f = gzip.open(filename, "r")
                c = f.readlines()
                f.close()
                for line in c:
                    contents.append(line.decode("utf-8"))
                del(c)
            else:
                f = open(filename, "r")
                contents = f.readlines()
                f.close()
            return contents
        else:
            outputfile.write("Cannot open {}\n".format(filename))   
    
    #============================================================
    # Open a file and return contents as a string
    def open_file_return_string(filename, outputfile):
        if os.path.isfile(filename):
            if 'gz' in filename:
                f = gzip.open(filename, "r")
                c = f.read()
                f.close()
                for line in c:
                    contents.append(line.decode("ascii"))
                    del(c)
            else:
                f = open(filename, "r")
                contents = f.read()
                f.close()
            return contents
        else:
            outputfile.write("Cannot open {}\n".format(filename))   
    
    #============================================================
    # Recursively find all required log files
    def find_logs(repo, filename):
        result = []
        result = glob.glob("{}/var/run/log/{}".format(repo.directory, filename))
        if result:    
            return result
        else:
            result = glob.glob("{}/commands/{}".format(repo.directory, filename))
            return result

    #============================================================
    # Check the timestamp
    def check_timestamp(repo, line):
        if not repo.startdate:
            return True
        else:
            s = line.split()
            try:
                line_date = dateutil.parser.parse(s[0], fuzzy=True)
                ld = datetime.datetime.strptime(str(line_date)[:19], "%Y-%m-%d %H:%M:%S")
                start_date = dateutil.parser.parse(repo.startdate, fuzzy=True)
                sd = datetime.datetime.strptime(str(start_date), "%Y-%m-%d %H:%M:%S")
                end_date = dateutil.parser.parse(repo.enddate, fuzzy=True)
                ed = datetime.datetime.strptime(str(end_date), "%Y-%m-%d %H:%M:%S")
                if ld >= sd and ld <= ed:
                    return True
                else:
                    return False
            except:
                pass
        
        
    #============================================================
    # Parse the /var/run/log files
    def log_search(repo, contents, log_type):
        messages_found = []
        table_values = [["Count", "String", "Start", "End"]]
        if log_type == 'vmkwarning': message_array = vmkwarning_strings
        elif log_type == 'vobd': message_array = vobd_strings
        elif log_type == 'hostd': message_array = hostd_strings
        elif log_type == 'esxcfg': message_array = esxcfg_strings
        for search_string in message_array:
            for line in contents:
                if search_string in line:
                    if tasks.check_timestamp(repo, line) == True:
                        s = line.split()
                        t = ("{}".format(s[0]))
                        messages_found.append(t)
            if len(messages_found) > 0:
                e = messages_found[(len(messages_found) - 1)]
                s = messages_found[0]
                table_values.append([str(len(messages_found)), search_string, s, e])
                messages_found = []
        return table_values
    
    #============================================================
    # Parse logs for the SVIP
    def svip_search(repo, contents):
        messages_found = []
        table_values = [["Count", "SVIP", "Start", "End"]]
        for line in contents:
            if tasks.check_timestamp(repo, line) == True:
                if repo.svip in line and 'warn' in line.lower() or repo.svip in line and 'err' in line.lower():
                    messages_found.append(line)
        if len(messages_found) > 0:
            e = messages_found[(len(messages_found) - 1)].split()
            s = messages_found[0].split()
            table_values.append([str(len(messages_found)), repo.svip, s[0], e[0]])
            return table_values

    #============================================================
    # Parse logs for a specific volume        
    def volume_search(repo, contents):
        messages_found = []
        for item in repo.volume_info.items():
            if item[0] != 'volume_id' and item[0] != 'PSP' and item[0] != 'PSPconfig':
                messages_found.append("=== Searching for {}\n".format(item[1]))
                for line in contents:
                    if item[1] in line:
                        if tasks.check_timestamp(repo, line) == True:
                            for ignore_item in ignore:
                                skip = False
                                if ignore_item in line:
                                    skip = True
                                    break
                            if skip == False:
                                messages_found.append("{}".format(line))
        return messages_found
            