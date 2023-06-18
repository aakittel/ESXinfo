import json
import os
import re
from program_data import ct

# =====================================================================
#
# NetApp / SolidFire
# CPE 
# ESXi log parser
#
# =====================================================================

class vnet():
    #============================================================
    # info for physical nics
    def pnic(repo):
        print("\n==================== Physical nic information ====================")
        output = []
        filename = ("{}/commands/nicinfo.sh.txt".format(repo.directory))
        print("== Source: {}".format(filename))
        contents = ct.open_file_return_list(filename)
        if contents:
            for line in contents:
                if "Description" in line: print(line.strip())
                elif "vmnic" in line and not "Name:" in line and not "statistics" in line: print(line.strip())
                elif "NIC:" in line: print(line.strip())
                elif "Driver:" in line: print(line.strip())
                elif "Firmware Version:" in line: print(line.strip())
                elif "Version: " in line :print(line)
            
    #============================================================
    # get vmnic info
    def vmnic(repo):
        print("\n==================== vmnic information ====================")
        filename = ("{}/json/localcli_iscsi-physicalnetworkportal-list.json".format(repo.directory))
        print("== Source: {}".format(filename))
        contents = ct.open_file_return_string(filename)
        if contents:
            contents_json = json.loads(contents)
            for item in contents_json:
                print("\nvmnic: {}\n\tCurrent Speed: {}\n\tMax Speed: {}\n\tMAC: {}\n\t".format(item['Vmnic'], item['Current Speed'], item['Max Speed'], item['MAC Address']))
            
    #============================================================
    # get vmk info
    def vmk(repo):
        print("\n==================== vmk information ====================")           
        filename = ("{}/commands/esxcfg-vmknic_-l.txt".format(repo.directory))
        print("\n== Source: {}".format(filename))
        contents = ct.open_file_return_list(filename)
        if contents:
            for line in contents:
                print(line.strip())
      
    #============================================================
    # distributed switch info
    def dvs(repo):
        print("\n==================== Distributed switch information  ====================")
        filename = ("{}/commands/net-dvs_-l.txt".format(repo.directory))
        print("== Source: {}".format(filename))
        contents = ct.open_file_return_list(filename)
        if contents:
            for line in contents:
                if("com.vmware.common.alias" in line): print(line.strip())
                if("com.vmware.common.portset.mtu" in line): print(line.strip())
                if re.search("port ", line): print("\n" + line.strip())
                if("com.vmware.common.port.portgroupid" in line): print(line.strip())
                if("com.vmware.common.port.block" in line): print(line.strip())
                if("com.vmware.etherswitch.port.security" in line): print(line.strip())
                if("com.vmware.etherswitch.port.vlan" in line): print(line.strip())
                if("pktsInDropped" in line): print(line.strip())
                if("pktsOutDropped" in line): print(line.strip())
            
    #============================================================
    # vswitch info
    def vswitch(repo):
        print("\n==================== Standard switch information  ====================")
        filename = ("{}/commands/esxcfg-vswitch_-l.txt".format(repo.directory))
        print("== Source: {}".format(filename))
        contents = ct.open_file_return_list(filename)
        if contents:
            for line in contents:
                print(line.strip())