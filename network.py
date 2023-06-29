import json
import os
import re
from tasks import tasks

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
    def pnic(repo, outputfile):
        outputfile.write("\n\n==================== Physical nic information ====================\n")
        output = []
        filename = ("{}/commands/nicinfo.sh.txt".format(repo.directory))
        outputfile.write("== Source: {}\n".format(filename))
        contents = tasks.open_file_return_list(filename, outputfile)
        if contents:
            for line in contents:
                if "Description" in line: outputfile.write(line)
                elif "vmnic" in line and not "Name:" in line and not "statistics" in line: outputfile.write(line)
                elif "NIC:" in line: outputfile.write(line)
                elif "Driver:" in line: outputfile.write(line)
                elif "Firmware Version:" in line: outputfile.write(line)
                elif "Version: " in line :outputfile.write(line)
            
    #============================================================
    # get vmnic info
    def vmnic(repo, outputfile):
        outputfile.write("\n\n==================== vmnic information ====================\n")
        filename = ("{}/json/localcli_iscsi-physicalnetworkportal-list.json".format(repo.directory))
        outputfile.write("== Source: {}".format(filename))
        contents = tasks.open_file_return_string(filename, outputfile)
        if contents:
            contents_json = json.loads(contents)
            for item in contents_json:
                outputfile.write("\nvmnic: {}\n\tCurrent Speed: {}\n\tMax Speed: {}\n\tMAC: {}\n\t".format(item['Vmnic'], item['Current Speed'], item['Max Speed'], item['MAC Address']))
            
    #============================================================
    # get vmk info
    def vmk(repo, outputfile):
        outputfile.write("\n\n==================== vmk information ====================\n")           
        filename = ("{}/commands/esxcfg-vmknic_-l.txt".format(repo.directory))
        outputfile.write("== Source: {}\n".format(filename))
        contents = tasks.open_file_return_list(filename, outputfile)
        if contents:
            for line in contents:
                outputfile.write(line)
      
    #============================================================
    # distributed switch info
    def dvs(repo, outputfile):
        outputfile.write("\n\n==================== Distributed switch information  ====================\n")
        filename = ("{}/commands/net-dvs_-l.txt".format(repo.directory))
        outputfile.write("== Source: {}\n".format(filename))
        contents = tasks.open_file_return_list(filename, outputfile)
        if contents:
            for line in contents:
                if("com.vmware.common.alias" in line): outputfile.write(line)
                if("com.vmware.common.portset.mtu" in line): outputfile.write(line)
                if re.search("port ", line): outputfile.write("\n" + line)
                if("com.vmware.common.port.portgroupid" in line): outputfile.write(line)
                if("com.vmware.common.port.block" in line): outputfile.write(line)
                if("com.vmware.etherswitch.port.security" in line): outputfile.write(line)
                if("com.vmware.etherswitch.port.vlan" in line): outputfile.write(line)
                if("pktsInDropped" in line): outputfile.write(line)
                if("pktsOutDropped" in line): outputfile.write(line)
            
    #============================================================
    # vswitch info
    def vswitch(repo, outputfile):
        outputfile.write("\n\n==================== Standard switch information  ====================\n")
        filename = ("{}/commands/esxcfg-vswitch_-l.txt".format(repo.directory))
        outputfile.write("== Source: {}\n".format(filename))
        contents = tasks.open_file_return_list(filename, outputfile)
        if contents:
            for line in contents:
                outputfile.write(line)