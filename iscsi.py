import json
from program_data import ct
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
    def iscsihba(repo):
        print("\n==================== iscsi adapter information ====================")
        filename = ("{}/json/localcli_storage-core-adapter-list.json".format(repo.directory))
        print("== Source: {}".format(filename))
        contents = ct.open_file_return_string(filename)
        if contents:
            contents_json = json.loads(contents)
            for item in contents_json:
                if item['Driver'] == 'iscsi_vmk':
                    print("\n{}\n\tDriver: {}\n\tHBA Name: {}\n\tLink State: {}\n\tUID: {}".format(item['Description'], item['Driver'], item['HBA Name'], item['Link State'], item['UID']))
        
        
    #============================================================
    # vmk port bindings
    def portbinding(repo):
        print("\n==================== vmkernel nic bindings  ====================")
        print("=== WILL ONLY BE POPULATED IF PORT BINDINGS EXIST")
        filename = ("{}/json/localcli_iscsi-networkportal-list.json".format(repo.directory))
        print("== Source: {}".format(filename))
        contents = ct.open_file_return_string(filename)
        if contents:
            contents_json = json.loads(contents)
            for item in contents_json:
                print("\nvmknic: {}\n\tCompliant Status: {}".format(item['Vmknic'], item['Compliant Status']))
                print("\tVswitch: {}\n\tVlan ID: {}\n\tPortGroup: {}\n\tPath Status: {}".format(item['Vswitch'],item['Vlan ID'],item['PortGroup'],item['Path Status']))
                print("\tNIC Driver: {}\n\tNIC Driver Version: {}\n\tNIC Firmware Version: {}".format(item['NIC Driver'], item['NIC Driver Version'], item['NIC Firmware Version']))
                print("\tIPv4: {}\n\tCurrent Speed: {}\n\tLink Up: {}\n\tMTU: {}".format(item['IPv4'], item['Current Speed'], item['Link Up'], item['MTU']))
                   
