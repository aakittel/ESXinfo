import json
from tasks import tasks

# =====================================================================
#
# NetApp / SolidFire
# CPE 
# ESXi log parser
#
# =====================================================================

class sto():
    #============================================================
    # get storage device info and make a map of sorts to everything a volume could be on ESX
    def devmap(repo, outputfile):
        # volume info files
        fileone = "{}/json/localcli_storage-nmp-device-list.json".format(repo.directory)
        filetwo = "{}/json/localcli_storage-vmfs-extent-list.json".format(repo.directory)
        filethree = "{}/json/localcli_storage-core-path-list.json".format(repo.directory)
        nmp = tasks.open_file_return_string(fileone, outputfile)
        vmfs = tasks.open_file_return_string(filetwo, outputfile)
        dev = tasks.open_file_return_string(filethree, outputfile)
        # convert contents to json
        nmp_json = json.loads(nmp)
        vmfs_json = json.loads(vmfs)
        dev_json = json.loads(dev)
        # declare a json volume map
        volume_map = {}

        outputfile.write("\n\n==================== Storage device path information (DEVICE MAP)====================\n")
        outputfile.write("== https://www.netapp.com/us/media/tr-4806.pdf ==")

        for dev_line in dev_json:
            if "6f47acc" in dev_line['Device']:
                x = dev_line['Target Transport Details'].split()
                y = x[0].split('=')
                z = y[1].split('.')
                volume_map["iqn"] = y[1]
                volume_map["naa"] = dev_line['Device']
                volume_map["volume_id"] = z[(len(z) - 1)]
                for nmp_line in nmp_json:
                    if volume_map["naa"] == nmp_line['Device']:
                        volume_map["a_path"] = nmp_line['Working Paths'][0]
                        volume_map["b_path"] = nmp_line['Working Paths'][1]
                        volume_map["PSP"] = nmp_line['Path Selection Policy']
                        if volume_map["PSP"] != "VMW_PSP_RR":
                            volume_map["PSP"] = ("{} WARNING: SHOULD BE VMW_PSP_RR".format(nmp_line['Path Selection Policy']))
                        volume_map["PSPconfig"] = nmp_line['Path Selection Policy Device Config']
                        if "iops=1000" in nmp_line['Path Selection Policy Device Config']:
                            volume_map["doc"] = "** IOPS=1000 SEE KB https://kb.vmware.com/s/article/2069356 **"            
                for vmfs_line in vmfs_json:
                    if vmfs_line['Device Name'] == volume_map['naa']:
                        volume_map["datastore"] = vmfs_line['Volume Name']
                        volume_map["uuid"] = vmfs_line['VMFS UUID']        
                if repo.volume_id == 0:
                    outputfile.write("\nVolume ID: {}\n".format(volume_map["volume_id"]))
                    for key, value in volume_map.items():
                        outputfile.write("{}:\t{}\n".format(key, value))
            if int(volume_map['volume_id']) == int(repo.volume_id):
                repo.volume_info = volume_map
                outputfile.write("\nVolume ID: {}\n".format(volume_map["volume_id"]))
                for key, value in volume_map.items():
                    outputfile.write("{}:\t{}\n".format(key, value))
                break

    #============================================================
    # Show device stats if there are read and/or write failures                
    def devstats(repo, outputfile):
        outputfile.write("\n\n==================== Storage device stats FAILS ONLY====================\n")
        filename = ("{}/json/localcli_storage-core-device-stats-get.json".format(repo.directory))
        outputfile.write("== Source: {}".format(filename))
        contents = tasks.open_file_return_string(filename, outputfile)
        if contents:
            contents_json = json.loads(contents)
            for item in contents_json:
                if item['Failed Blocks Read'] > 0 or item['Failed Blocks Written'] > 0 or item['Failed Read Operations'] > 0 or item['Failed Write Operations'] > 0:
                    outputfile.write("\n{}\n\tFailed Block read: {}\n\tFailed Blocks Written: {}".format(item['Device'], str(item['Failed Blocks Read']), str(item['Failed Blocks Written'])))
                    outputfile.write("\n\tFailed Read Operations: {}\n\tFailed Write Operations: {}".format(str(item['Failed Read Operations']), str(item['Failed Write Operations'])))

    #============================================================
    # Show the datastore extents table                            
    def extents(repo, outputfile):
        outputfile.write("\n\n==================== Datastore information ====================\n")
        filename = ("{}/commands/localcli_storage-vmfs-extent-list.txt".format(repo.directory))
        outputfile.write("== Source: {}\n".format(filename))
        contents = tasks.open_file_return_list(filename, outputfile)
        if contents:
            for line in contents:
                outputfile.write(line)
    
class vvol():
    #============================================================
    # Show protocol endpoints
    def endpoint(repo, outputfile):
        # convert /data/CSD-5605/esx-icpidn200020.svr.apac.jpmchase.net-2023-06-07--19.51-2831891/json/localcli_storage-vvol-protocolendpoint-list.json
        outputfile.write("\n\n==================== VVOL protocol endpoint information ====================\n")
        filename = ("{}/json/localcli_storage-vvol-protocolendpoint-list.json".format(repo.directory))
        outputfile.write("== Source: {}".format(filename))
        contents = tasks.open_file_return_string(filename, outputfile)
        if contents:
            contents_json = json.loads(contents)
            for line in contents_json:
                outputfile.write(line)
        else:
            outputfile.write("No VVOL Endpoints available\n")

    #============================================================
    # Show storage containers                
    def container(repo, outputfile):
        # convert esx-icpidn200020.svr.apac.jpmchase.net-2023-06-07--19.51-2831891/json/localcli_storage-vvol-storagecontainer-list.json
        outputfile.write("\n\n==================== VVOL storage container information ====================\n")
        filename = ("{}/json/localcli_storage-vvol-storagecontainer-list.json".format(repo.directory))
        outputfile.write("== Source: {}".format(filename))
        contents = tasks.open_file_return_string(filename, outputfile)
        if contents:
            contents_json = json.loads(contents)
            for line in contents_json:
                outputfile.write(line)
        else:
            outputfile.write("No VVOL Storage Containers available\n")

    #============================================================
    # Show storage providers                
    def provider(repo, outputfile):
        #convert /data/CSD-5605/esx-icpidn200020.svr.apac.jpmchase.net-2023-06-07--19.51-2831891/json/localcli_storage-vvol-vasaprovider-list.json
        outputfile.write("\n\n==================== VVOL vasa provider information ====================\n")
        filename = ("{}/json/localcli_storage-vvol-vasaprovider-list.json".format(repo.directory))
        outputfile.write("== Source: {}".format(filename))
        contents = tasks.open_file_return_string(filename, outputfile)
        if contents:
            contents_json = json.loads(contents)
            for line in contents_json:
                outputfile.write(line)
        else:
            outputfile.write("No VVOL VASA Providers available\n")