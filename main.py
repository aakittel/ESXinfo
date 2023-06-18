#!/usr/bin/python
import argparse
import textwrap
from iscsi import iscsi
from network import vnet
from program_data import globalvar, ct
from storage import sto, vmfs

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
    required_named = cmd_args.add_argument_group('required named arguments')
    required_named.add_argument('-d', '--directory', required=True, help='Specify log bundle directory.')
    required_named.add_argument('-o', '--outputfile', help='Specify an output file')
    required_named.add_argument('-a', '--action', help=textwrap.dedent('''Specify action task.                                                          
    all: Runs all data gathering
    network: Gather network data
    log: Parse the log files
    storage: Gather VMFS and storage
    vvol: Gather vvol data
    
    updateonepw: Update one asset password'''))

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
    if not args.outputfile:
        print("Please specify an outputfile")    
        exit()
    else:
        repo.outputfile = args.outputfile
        
    # Get the esx.conf data
    try:
        esxconffile = ("{}/etc/vmware/esx.conf".format(args.directory))
        with open(esxconffile, "r") as esxconf:
            for line in esxconf:
                key,value = line.strip().split(' = ')
                repo.esxconf[key] = value
    except FileNotFoundError:
        print("Could not open {}/etc/vmware.esx.conf".format(args.directory))
        print("Host specific information will be missing\n")

    ct.header(repo)
    
    #vnet.pnic(repo)
    #vnet.vmnic(repo)
    #vnet.vmk(repo)
    #vnet.dvs(repo)
    #vnet.vswitch(repo)
    
    sto.corepath(repo)
    #sto.devstats(repo)
    #sto.nmp(repo)
    #sto.extents(repo)
    
    #iscsi.iscsihba(repo)
    #iscsi.portbinding(repo)