from tasks import tasks
from prettytable import PrettyTable
from search_strings import vmkwarning_strings, vobd_strings, hostd_strings, esxcfg_strings
# =====================================================================
#
# NetApp / SolidFire
# CPE 
# ESXi log parser
#
# =====================================================================

#============================================================
# General log parser
def parse_logs(repo, outputfile):
    for log_type in repo.log_types:
        print("\tParsing {} logs".format(log_type))
        outputfile.write("\n\n==================== Parse {} logs ====================\n".format(log_type))
        filename = "{}*".format(log_type)
        logs = tasks.find_logs(repo, filename)
        for log in logs:
            contents = tasks.open_file_return_list(log, outputfile)
            results = tasks.log_search(repo, contents, log_type)
            if len(results) > 1:
                table = PrettyTable(results[0])
                table.add_rows(results[1:])
                outputfile.write("\n\n{}\n".format(log))
                outputfile.write(str(table))

#============================================================
# Parse for SVIP. Wishlist: combine this with parse_logs
def parse_svip(repo, outputfile):
    outputfile.write("\n\n==================== Parse logs for SVIP {} ====================\n".format(repo.svip))
    for log_type in repo.log_types:
        print("\tParsing {} logs".format(log_type))
        outputfile.write("==================== Parse {} logs ====================\n".format(log_type))
        filename = "{}*".format(log_type)
        logs = tasks.find_logs(repo, filename)
        for log in logs:
            contents = tasks.open_file_return_list(log, outputfile)
            results = tasks.svip_search(repo, contents)
            if len(results) > 1:
                table = PrettyTable(results[0])
                table.add_rows(results[1:])
                outputfile.write("\n\n{}\n\tWarnings or errors for svip {}".format(log, str(len(results))))
                outputfile.write(str(table))
                                 
#============================================================
# Parse for specific volume id. Wishlist: combine this with parse_logs               
def parse_volume(repo, outputfile):
    outputfile.write("\n\n==================== Parse logs for Volume ID {} ====================\n".format(repo.volume_id))
    for log_type in repo.log_types:
        print("\tParsing {} logs".format(log_type))
        filename = "{}*".format(log_type)
        logs = tasks.find_logs(repo, filename)
        for log in logs:
            contents = tasks.open_file_return_list(log, outputfile)
            results = tasks.volume_search(repo, contents)
            if results:
                outputfile.write("\n{}\n".format(log))
                for line in results:
                    outputfile.write(line)