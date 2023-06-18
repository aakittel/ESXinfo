from datetime import timedelta
import os

# =====================================================================
#
# NetApp / SolidFire
# CPE 
# ESXi log parser
#
# =====================================================================

#============================================================
# Global vaiables
class globalvar():
    def __init__(self, args):
        self.esxconf = {}
        self.directory = ""
        self.outputfile = ""

#============================================================        
# common tasks
class ct():
    #============================================================
    #report header
    def header(repo):
        print("==================== Header information ====================")
        print("Management IP:\t{}".format(repo.esxconf['/adv/Net/ManagementAddr']))
        print("Management vmk:\t {}".format(repo.esxconf['/adv/Net/ManagementIface']))
        print("Host Name:\t {}".format(repo.esxconf['/adv/Misc/HostName']))
        if os.path.isfile("{}/commands/vmware_-vl.txt".format(repo.directory)):
            with open("{}/commands/vmware_-vl.txt".format(repo.directory), 'r') as f:
                versionlines = f.readlines()
                print("ESXi Version:\t{}".format(versionlines))
        else:
            print("ESXi Version:\tUNKNOWN")
        if os.path.isfile("{}/commands/localcli_system-stats-uptime-get.txt".format(repo.directory)):
            with open("{}/commands/localcli_system-stats-uptime-get.txt".format(repo.directory), 'r') as f:
                uptimelines = f.read()
                uptime = str(timedelta(microseconds=int(uptimelines)))
                print("System Uptime:\t{}".format(str(uptime.strip())))
        else:
            print("Uptime:\tUNKNWON")
        #print("\nssh server enabled:\t{}".format(repo.esxconf['/firewall/services/sshServer/enabled']))
        #print("ssh client enabled:\t{}".format(repo.esxconf['/firewall/services/sshClient/enabled']))
    
    #============================================================
    # Open a file and return contents as a list
    def open_file_return_list(filename):
        contents = []
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                contents = f.readlines()
                return contents
        else:
            print("Cannot open {}".format(filename))   
    
    #============================================================
    # Open a file and return contents as a string
    def open_file_return_string(filename):
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                contents = f.read()
                return contents
        else:
            print("Cannot open {}".format(filename))   
        