# =====================================================================
#
# NetApp / SolidFire
# CPE 
# ESXi log parser
#
# =====================================================================

#============================================================
# vobd log errors
vobd_strings = [
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
    "vob.iscsi.transport.connection.started",
    "esx.problem.vmsyslogd.remote.failure"
]

#============================================================
# vmkwarning log errors
vmkwarning_strings = [
    'iSCSI connection is being marked "OFFLINE"',
    "Lost path redundancy to storage device",
    "Login authentication failed with target",
    "has gone into disconnected state",
    "iscsivmk_StopConnection",
    "nmp_ResetDeviceLogThrottling",
    "Could not find VVol",
    "Lost access to volume",
    "AdapterServer caught exception",
    "FINAL FAILURE deleteVirtualVolume, error (RESOURCE_BUSY",
    "VasaSession::GetEndPoint: failed to get endpoint, err=SSL Exception",
    "Failed to initialize VMFS distributed locking on volume",
    "Failed to receive data: Connection closed by peer",
    "I/O latency increased"
]

#============================================================
# hostd log errors
hostd_strings = [
    "failed to get",
    "Lost access to volume",
    "Recovery attempt is in progress",
    "not found for datastore",
    "warning hostd"
]

#============================================================
# Common errors in esxcfg-info command output
esxcfg_strings = [
    "Error while retriving data from VMFS volume",
    "Slow refresh failed: Cannot open volume",
]

#============================================================
# Ignore items
ignore = ["vob.scsi.scsipath.add", 
          "vob.scsi.scsipath.pathstate.on", 
          "vob.vmfs.volume.mounted", 
          "esx.audit.vmfs.volume.mounted",
          "vob.scsi.scsipath.por", 
          "vob.vmfs.lock.busy.filedesc", 
          "esx.problem.vmfs.lock.busy.filedesc", 
          "Sleep and recheck lock",
          "info hostd", 
          "VMW_PSP_RR",
          "vCLS",
          "Error opening device vml"
            ]