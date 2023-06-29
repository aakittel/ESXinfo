import datetime
import dateutil.parser
import glob
import gzip
import os
from datetime import timedelta
from prettytable import PrettyTable
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
        table_data.append(["Management IP", "{}".format(repo.esxconf['/adv/Net/ManagementAddr'])])
        table_data.append(["Management vmk", "{}".format(repo.esxconf['/adv/Net/ManagementIface'])])
        table_data.append(["Host Name", "{}".format(repo.esxconf['/adv/Misc/HostName'])])
        if os.path.isfile("{}/commands/vmware_-vl.txt".format(repo.directory)):
            with open("{}/commands/vmware_-vl.txt".format(repo.directory), 'r') as f:
                versionlines = f.readlines()
                for line in versionlines:
                    table_data.append(["ESXi Version", "{}".format(line.strip())])
        else:
            table_data.append(["ESXi Version", "UNKNOWN"])
        if os.path.isfile("{}/commands/localcli_system-stats-uptime-get.txt".format(repo.directory)):
            with open("{}/commands/localcli_system-stats-uptime-get.txt".format(repo.directory), 'r') as f:
                uptimelines = f.read()
                uptime = str(timedelta(microseconds=int(uptimelines)))
                table_data.append(["System Uptime", "{}".format(str(uptime.strip()))])
        else:
            table_data.append(["Uptime", "UNKNWON"])
        table = PrettyTable()
        table.add_rows(table_data[0:])
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
                    contents.append(line.decode("ascii"))
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
            line_date = dateutil.parser.parse(s[0], fuzzy=True)
            test = str(line_date)
            ld = datetime.datetime.strptime(str(line_date)[:19], "%Y-%m-%d %H:%M:%S")
            start_date = dateutil.parser.parse(repo.startdate, fuzzy=True)
            sd = datetime.datetime.strptime(str(start_date)[:19], "%Y-%m-%d %H:%M:%S")
            end_date = dateutil.parser.parse(repo.enddate, fuzzy=True)
            ed = datetime.datetime.strptime(str(end_date)[:19], "%Y-%m-%d %H:%M:%S")
            if ld >= sd and ld <= ed:
                return True
            else:
                return False
        
        
    #============================================================
    # Parse the /var/run/log files
    def log_search(repo, contents, log_type):
        messages_found = []
        return_value = [["Count", "String", "Start", "End"]]
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
                s = messages_found[(len(messages_found) - 1)]
                e = messages_found[0]
                return_value.append([str(len(messages_found)), search_string, s, e])
                messages_found = []
        return return_value
    
    #============================================================
    # Parse logs for the SVIP
    def svip_search(repo, contents):
        messages_found = []
        return_value = [["Count", "SVIP", "Start", "End"]]
        for line in contents:
            if tasks.check_timestamp(repo, line) == True:
                if repo.svip in line and 'warn' in line.lower() or repo.svip in line and 'err' in line.lower():
                    messages_found.append(line)
        if len(messages_found) > 0:
            s = messages_found[(len(messages_found) - 1)].split()
            e = messages_found[0].split()
            return_value.append([str(len(messages_found)), repo.svip, s[0], e[0]])
            return return_value

    #============================================================
    # Parse logs for a specific volume        
    def volume_search(repo, contents):
        messages_found = []
        for item in repo.volume_info.items():
            if item[0] != 'volume_id':
                for line in contents:
                    if item[1] in line:
                        if tasks.check_timestamp(repo, line) == True:
                            for ignore_item in ignore:
                                skip = False
                                if ignore_item in line:
                                    skip = True
                                    break
                            if skip == False:
                                messages_found.append(line)
        return messages_found
            