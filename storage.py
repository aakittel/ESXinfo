import json
from program_data import ct

# =====================================================================
#
# NetApp / SolidFire
# CPE 
# ESXi log parser
#
# =====================================================================
# NOTES 
# map file /commands/localcli_storage-core-path-list.txt
# NMP/PSP /commands/localcli_storage-nmp-device-list.txt
# /json/localcli_storage-vmfs-lockmode-list--i.json

class sto():
    #============================================================
    # get storage device info
    # /data/CSD-5605/esx-icpidn200026.svr.apac.jpmchase.net-2023-06-07--19.51-2942619/json/localcli_storage-core-path-list.json
    def corepath(repo):
        print("\n==================== Storage device path information (DEVICE MAP)====================")
        filename = ("{}/json/localcli_storage-core-path-list.json".format(repo.directory))
        print("== Source: {}".format(filename))
        contents = ct.open_file_return_string(filename)
        if contents:
            contents_json = json.loads(contents)
            for item in contents_json:
                if 'SolidFir iSCSI Disk' in item['Device Display Name']:
                    print("\n{}\n\tTarget Details: {}\n\tRuntime Name: {}".format(item['Device'], item['Target Transport Details'], item['Runtime Name']))
                
                
    def devstats(repo):
        print("\n==================== Storage device stats FAILS ONLY====================")
        filename = ("{}/json/localcli_storage-core-device-stats-get.json".format(repo.directory))
        print("== Source: {}".format(filename))
        contents = ct.open_file_return_string(filename)
        if contents:
            contents_json = json.loads(contents)
            for item in contents_json:
                if item['Failed Blocks Read'] > 0 or item['Failed Blocks Written'] > 0 or item['Failed Read Operations'] > 0 or item['Failed Write Operations'] > 0:
                    print("\n{}\n\tFailed Block read: {}\n\tFailed Blocks Written: {}".format(item['Device'], str(item['Failed Blocks Read']), str(item['Failed Blocks Written'])))
                    print("\tFailed Read Operations: {}\n\tFailed Write Operations: {}".format(str(item['Failed Read Operations']), str(item['Failed Write Operations'])))
                
    def nmp(repo):
        print("\n==================== Storage NMP information ====================")
        filename = ("{}/json/localcli_storage-nmp-device-list.json".format(repo.directory))
        print("== Source: {}".format(filename))
        print("== https://www.netapp.com/us/media/tr-4806.pdf ==")
        contents = ct.open_file_return_string(filename)
        if contents:
            contents_json = json.loads(contents)
            for item in contents_json:
                if 'SolidFir iSCSI Disk' in item['Device Display Name']:
                    print("\nDevice: {}\n\tPath Selection Policy: {}\n\tPath Selection Policy Device Config: {}".format(item['Device Display Name'], item['Path Selection Policy'], item['Path Selection Policy Device Config']))
                    if("iops=1000" in item['Path Selection Policy Device Config']): 
                        print("** IOPS=1000 SEE KB https://kb.vmware.com/s/article/2069356 **")
                    print("\tWorking paths: {}".format(item['Working Paths']))
                    
                    
                
    def extents(repo):
        print("\n==================== Storage NMP information ====================")
        filename = ("{}/commands/localcli_storage-vmfs-extent-list.txt".format(repo.directory))
        print("== Source: {}".format(filename))
        contents = ct.open_file_return_list(filename)
        if contents:
            for line in contents:
                print(line.strip())
              
class vmfs():
    pass
        
    
class vvol():
    def endpoint(repo):
        # convert /data/CSD-5605/esx-icpidn200020.svr.apac.jpmchase.net-2023-06-07--19.51-2831891/json/localcli_storage-vvol-protocolendpoint-list.json
        print("\n==================== VVOL protocol endpoint information ====================")
        filename = ("{}/commands/localcli_storage-vvol-protocolendpoint-list.txt".format(repo.directory))
        print("== Source: {}".format(filename))
        contents = ct.open_file_return_list(filename)
        if contents:
            for line in contents:
                if("Array Id:" in line): print(line.strip())
                if("Lun Id:" in line): print(line.strip())
                if("Storage Containers:" in line): print(line.strip())
                
    def container(repo):
        # convert esx-icpidn200020.svr.apac.jpmchase.net-2023-06-07--19.51-2831891/json/localcli_storage-vvol-storagecontainer-list.json
        print("\n==================== VVOL storage container information ====================")
        filename = ("{}/commands/localcli_storage-vvol-storagecontainer-list.txt".format(repo.directory))
        print("== Source: {}".format(filename))
        contents = ct.open_file_return_list(filename)
        if contents:
            for line in contents:
                print(line.strip())
                
    def provider(repo):
        #convert /data/CSD-5605/esx-icpidn200020.svr.apac.jpmchase.net-2023-06-07--19.51-2831891/json/localcli_storage-vvol-vasaprovider-list.json
        print("\n==================== VVOL vasa provider information ====================")
        filename = ("{}/commands/localcli_storage-vvol-vasaprovider-list.txt".format(repo.directory))
        print("== Source: {}".format(filename))
        contents = ct.open_file_return_list(filename)
        if contents:
            for line in contents:
                print(line.strip())