#!/usr/bin/python
import argparse
from datetime import datetime
from iscsi import iscsi
from network import vnet
from program_data import globalvar
from log_parse import parse_logs, parse_svip, parse_volume
from storage import sto, vvol
from tasks import tasks

# =====================================================================
#
# NetApp / SolidFire
# CPE 
# ESXi log parser
#
# =====================================================================

#============================================================
# Gather command line arguments
def get_args():
    cmd_args = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    cmd_args.add_argument('-sd', '--startdate', help='Specify a starttime')
    cmd_args.add_argument('-ed', '--enddate', help='Specify a starttime')
    cmd_args.add_argument('-svip', '--storage_svip', help='Specify a cluster SVIP')
    cmd_args.add_argument('-vid', '--volume_id', help='Specify a cluster volume id')
    required_named = cmd_args.add_argument_group('required named arguments')
    required_named.add_argument('-d', '--directory', required=True, help='Specify log bundle directory.')

    return cmd_args.parse_args()


#============================================================
# main
if __name__ == "__main__":
    args = get_args()
    repo = globalvar(args)
    
    if not args.directory:
        print("Please specify -d/--directory path to ESXi support bundle\n")
        exit()
    else:
        repo.directory = args.directory
    
    if args.startdate and args.enddate:
        repo.startdate = args.startdate
        repo.enddate = args.enddate
    
    if args.volume_id:
        repo.volume_id = str(args.volume_id)
        
    date_time = datetime.now()
    time_stamp = date_time.strftime("%d-%b-%Y-%H.%M.%S")
    outfile = ("{}/ESXinfoReport.txt".format(args.directory))
    try:
        outputfile = open(outfile, "w")
        print("Generating ESXinfo report {}".format(outfile))
    except FileNotFoundError:
        print("Could not open {} for writing.".format(outfile,repo.directory))
        outfile = "/tmp/ESXinforReport-{}".format(repo.directory)
        print("Sending report to {}".format(outfile))
        outputfile = open(outfile, "w")
    
    #============================================================            
    # Get the esx.conf data
    try:
        esxconffile = ("{}/etc/vmware/esx.conf".format(args.directory))
        with open(esxconffile, "r") as esxconf:
            for line in esxconf:
                key,value = line.split(' = ')
                repo.esxconf[key] = value
    except FileNotFoundError:
        outputfile.write("Could not open {}/etc/vmware.esx.conf".format(args.directory))
        outputfile.write("Host specific information will be missing\n")

    #============================================================
    # Start the run      
    print("Processing header data")
    tasks.header(repo, outputfile)
    
    tasks.show_drv_fw(repo, outputfile)
    
    print("Processing network data")
    vnet.pnic(repo, outputfile)
    vnet.vmnic(repo, outputfile)
    vnet.vmk(repo, outputfile)
    vnet.dvs(repo, outputfile)
    vnet.vswitch(repo, outputfile)
    
    print("Processing storage data")
    sto.devmap(repo, outputfile)
    sto.devstats(repo, outputfile)
    sto.extents(repo, outputfile)
    
    vvol.container(repo, outputfile)
    vvol.endpoint(repo, outputfile)
    vvol.provider(repo, outputfile)
    
    print("Processing iscsi data")
    iscsi.iscsihba(repo, outputfile)
    iscsi.portbinding(repo, outputfile)
    
    print("Parsing logs. This may take a while")
    parse_logs(repo, outputfile)
    
    if args.storage_svip:
        repo.svip = args.storage_svip
        print("Searching logs for SVIP {}".format(repo.svip))
        parse_svip(repo, outputfile)
    if args.volume_id:
        if repo.volume_info:
            print("Searching logs for volumeID {}".format(args.volume_id))
            parse_volume(repo, outputfile)
    
    print("Completed ESXinfo report: {}".format(outfile))
    outputfile.close()