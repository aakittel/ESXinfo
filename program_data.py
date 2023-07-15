# =====================================================================
#
# NetApp / SolidFire
# CPE 
# ESXi log parser
#
# =====================================================================

#============================================================
# Global vaiables
class globalvar():
    def __init__(self, args):
        self.esxconf = {}
        self.esx_version = ""
        self.enddate = ""
        self.directory = ""
        self.log_types = ['vmkwarning', 'vobd', 'hostd']
        self.platform = ""
        self.startdate = ""
        self.svip = ""
        self.volume_id = 0
        self.volume_info = {}

class drv_fw():
    driver_firmware = {
        "esx_67": [
                {"platform": "H615", "IMT": 
                    [
                     {"driver": "4.19.16.8", "firmware": "14.24.1000, 14.29.1016"},
                     {"driver": "4.17.15.16", "firmware": "14.25.1020, 14.29.1016"},
                     {"driver": "4.17.71.1", "firmware": "14.29.1016"}
                    ]
                },
                {"platform": "H610", "IMT": 
                    [
                     {"driver": "4.17.15.16", "firmware": "14.25.1020, 14.29.1016"},
                     {"driver": "4.17.13.8-1", "firmware": "14.22.1002"},
                     {"driver": "4.17.71.1", "firmware": "14.29.1016"}
                    ]
                },
                {"platform": "H410", "IMT":
                    [
                     {"driver": "4.17.15.16", "firmware": "14.25.1020, 14.29.1016"},
                     {"driver": "4.19.16.1", "firmware": "14.25.1020, 14.29.1016"},
                     {"driver": "4.17.13.8-1", "firmware": "14.21.1000"},
                     {"driver": "4.17.71.1", "firmware": "14.29.1016"}
                    ]
                },
                {"platform": "H300", "IMT":
                 [
                    {"driver": "4.17.13.8-1", "firmware": "14.21.1000"},
                    {"driver": "4.17.15.16", "firmware": "14.25.1020, 14.29.1016"},
                    {"driver": "4.17.71.1", "firmware": "14.29.1016"},
                    {"driver": "4.19.16.1", "firmware": "14.25.1020, 14.29.1016"}
                 ]
                },
                {"platform": "H500", "IMT":
                 [
                    {"driver": "4.17.13.8-1", "firmware": "14.21.1000"},
                    {"driver": "4.17.15.16", "firmware": "14.25.1020, 14.29.1016"},
                    {"driver": "4.17.71.1", "firmware": "14.29.1016"},
                    {"driver": "4.19.16.1", "firmware": "14.25.1020, 14.29.1016"}
                 ]
                },
                {"platform": "H700", "IMT":
                 [
                    {"driver": "4.17.13.8-1", "firmware": "14.21.1000"},
                    {"driver": "4.17.15.16", "firmware": "14.25.1020, 14.29.1016"},
                    {"driver": "4.17.71.1", "firmware": "14.29.1016"},
                    {"driver": "4.19.16.1", "firmware": "14.25.1020, 14.29.1016"}
                 ]
                },
            ],
        "esx_7": [
                {"platform": "H615", "IMT": 
                    [
                     {"driver": "4.19.16.8", "firmware": "14.24.1000, 14.29.1016"},
                     {"driver": "4.17.15.16", "firmware": "14.25.1020, 14.29.1016"},
                     {"driver": "4.21.71.1", "firmware": "14.29.1016"},
                    ]
                },
                {"platform": "H610", "IMT": 
                    [
                     {"driver": "4.17.15.16", "firmware": "14.25.1020, 14.29.1016"},
                     {"driver": "4.19.16.11", "firmware": "14.25.1020, 14.29.1016"},
                     {"driver": "4.19.16.8", "firmware": "14.25.1020, 14.29.1016"},
                     {"driver": "4.21.71.1", "firmware": "14.29.1016"}
                    ]
                },
                {"platform": "H410", "IMT":
                    [
                     {"driver": "4.17.15.16", "firmware": "14.25.1020, 10.29.1016"},
                     {"driver": "4.19.16.1", "firmware": "14.25.1020, 10.29.1016"},
                     {"driver": "4.19.16.8", "firmware": "14.25.1020, 10.29.1016"},
                     {"driver": "4.19.16.11", "firmware": "14.25.1020, 10.29.1016"},
                     {"driver": "4.19.16.10-vmw", "firmware": "14.25.1020, 10.29.1016"},
                     {"driver": "4.21.71.1", "firmware": "14.29.1016"},
                    ]
                },
                {"platform": "H300", "IMT":
                 [
                    {"driver": "4.17.13.8-1", "firmware": "14.21.1000"},
                    {"driver": "4.17.15.16", "firmware": "14.25.1020, 14.29.1016"},
                    {"driver": "4.17.71.1", "firmware": "14.29.1016"},
                    {"driver": "4.19.16.1", "firmware": "14.25.1020, 14.29.1016"},
                    {"driver": "4.19.16.8", "firmware": "14.25.1020, 14.29.1016"},
                    {"driver": "4.19.16.10-1vmw", "firmware": "14.25.1020, 14.29.1016"},
                    {"driver": "4.19.16.11", "firmware": "14.25.1020, 14.29.1016"}
                 ]
                },
                {"platform": "H500", "IMT":
                 [
                    {"driver": "4.17.13.8-1", "firmware": "14.21.1000"},
                    {"driver": "4.17.15.16", "firmware": "14.25.1020, 14.29.1016"},
                    {"driver": "4.17.71.1", "firmware": "14.29.1016"},
                    {"driver": "4.19.16.1", "firmware": "14.25.1020, 14.29.1016"},
                    {"driver": "4.19.16.8", "firmware": "14.25.1020, 14.29.1016"},
                    {"driver": "4.19.16.10-1vmw", "firmware": "14.25.1020, 14.29.1016"},
                    {"driver": "4.19.16.11", "firmware": "14.25.1020, 14.29.1016"}
                 ]
                },
                {"platform": "H700", "IMT":
                 [
                    {"driver": "4.17.13.8-1", "firmware": "14.21.1000"},
                    {"driver": "4.17.15.16", "firmware": "14.25.1020, 14.29.1016"},
                    {"driver": "4.17.71.1", "firmware": "14.29.1016"},
                    {"driver": "4.19.16.1", "firmware": "14.25.1020, 14.29.1016"},
                    {"driver": "4.19.16.8", "firmware": "14.25.1020, 14.29.1016"},
                    {"driver": "4.19.16.10-1vmw", "firmware": "14.25.1020, 14.29.1016"},
                    {"driver": "4.19.16.11", "firmware": "14.25.1020, 14.29.1016"}
                 ]
                },
            ],
        "esx_8": [
                {"platform": "H615", "IMT":
                    [
                        {"driver": "4.23.0.36", "firmware": "14.29.1016"}
                    ]
                },
                {"platform": "H610", "IMT":
                    [
                        {"driver": "4.23.0.36", "firmware": "14.29.1016"}
                    ]
                },  
                {"platform": "H410", "IMT":
                    [
                        {"driver": "4.23.0.36", "firmware": "14.29.1016"}
                    ]
                }
        ]}
        
    driver_downloads = {
        "4.17.71.1": "https://my.vmware.com/en/web/vmware/downloads/details?downloadGroup=DT-ESXI67-MELLANOX-NMLX5_CORE-417711&productId=742",
        "4.21.71.1": "https://my.vmware.com/en/web/vmware/downloads/details?downloadGroup=DT-ESXI70-MELLANOX-NMLX5_CORE-421711&productId=974"
        
    }
    firmware_rn = {
        "14.29.1016": "https://docs.netapp.com/us-en/hci/docs/rn_compute_firmware_2.174.0.html"
    }
    imt_url = "https://imt.netapp.com/matrix/imt.jsp?components=95927;96230;95905;96231;95925;95926;95928;95924;83113;85550;87666;90084;95808;97723;99423;102224;&solution=1737&isHWU&src=IMT"
    
