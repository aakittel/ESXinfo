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
        self.enddate = ""
        self.directory = ""
        self.log_types = ['vmkwarning', 'vobd', 'hostd']
        self.startdate = ""
        self.svip = ""
        self.volume_id = 0
        self.volume_info = {}