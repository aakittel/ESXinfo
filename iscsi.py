import json
from tasks import tasks
# =====================================================================
#
# NetApp / SolidFire
# CPE 
# ESXi log parser
#
# =====================================================================

class iscsi():
    #============================================================
    # software iscsi adapter
    def iscsihba(repo, outputfile):
        outputfile.write("\n\n==================== iscsi adapter information ====================\n")
        filename = ("{}/json/localcli_storage-core-adapter-list.json".format(repo.directory))
        outputfile.write("== Source: {}".format(filename))
        contents = tasks.open_file_return_string(filename, outputfile)
        if contents:
            contents_json = json.loads(contents)
            for item in contents_json:
                if item['Driver'] == 'iscsi_vmk':
                    outputfile.write("\n{}\n\tDriver: {}\n\tHBA Name: {}\n\tLink State: {}\n\tUID: {}".format(item['Description'], item['Driver'], item['HBA Name'], item['Link State'], item['UID']))
        
        
    #============================================================
    # vmk port bindings
    def portbinding(repo, outputfile):
        outputfile.write("\n\n==================== vmkernel nic bindings  ====================\n")
        outputfile.write("=== WILL ONLY BE POPULATED IF PORT BINDINGS EXIST\n")
        outputfile.write("=== IF NO BINDINGS EXIST, DATA TRAFFIC IS BEING ROUTED OR ADAPTER IS MISCONFIGURED\n")
        outputfile.write("=== https://core.vmware.com/resource/best-practices-running-vmware-vsphere-iscsi\n")
        filename = ("{}/json/localcli_iscsi-networkportal-list.json".format(repo.directory))
        outputfile.write("== Source: {}".format(filename))
        contents = tasks.open_file_return_string(filename, outputfile)
        if contents:
            contents_json = json.loads(contents)
            for item in contents_json:
                outputfile.write("\nvmknic: {}\n\tCompliant Status: {}".format(item['Vmknic'], item['Compliant Status']))
                outputfile.write("\n\tVswitch: {}\n\tVlan ID: {}\n\tPortGroup: {}\n\tPath Status: {}".format(item['Vswitch'],item['Vlan ID'],item['PortGroup'],item['Path Status']))
                outputfile.write("\n\tNIC Driver: {}\n\tNIC Driver Version: {}\n\tNIC Firmware Version: {}".format(item['NIC Driver'], item['NIC Driver Version'], item['NIC Firmware Version']))
                outputfile.write("\n\tIPv4: {}\n\tCurrent Speed: {}\n\tLink Up: {}\n\tMTU: {}".format(item['IPv4'], item['Current Speed'], item['Link Up'], item['MTU']))
                   
