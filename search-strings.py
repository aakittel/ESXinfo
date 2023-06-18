# =====================================================================
#
# NetApp / SolidFire
# CPE 
# ESXi log parser
#
# =====================================================================

# Common vobd.log errors
vobd = [
    "vob.vmfs.volume.mounted",
    "vob.storage.apd.start",
    "vob.scsi.scsipath.pathstate.dead",
    "vob.iscsi.connection.stopped",
    "esx.problem.storage.apd.start",
    "esx.problem.storage.apd.timeout",
    "esx.problem.storage.connectivity.lost",
    "vob.vmfs.heartbeat.timedout",
    "esx.problem.vmfs.heartbeat.timedout",
    "esx.clear.storage.apd.exit",
    "vob.storage.apd.exit",
    "vob.scsi.scsipath.por",
    "vob.scsi.scsipath.pathstate.on",
    "vob.iscsi.transport.connection.started"
]

# Common vmkernel.log, vmkwarning.log errors
vmkernel = [
    "Lost path redundancy to storage device",
    "Login authentication failed with target",
    "has gone into disconnected state",
    "iscsivmk_StopConnection",
    "PF Exception 14",
    "Generating backtrace",
    "get connection stats failed",
    "nmp_ResetDeviceLogThrottling",
    "Could not find VVol",
    "Lost access to volume",
    "AdapterServer caught exception",
    "FINAL FAILURE deleteVirtualVolume, error (RESOURCE_BUSY",
    "VasaSession::GetEndPoint: failed to get endpoint, err=SSL Exception",
    "Failed to initialize VMFS distributed locking on volume",
    "Failed to get object 28 type 3"
]

# Common errors in esxcfg-info command output
esxfginfo = [
    "Error while retriving data from VMFS volume",
    "Slow refresh failed: Cannot open volume",
]

