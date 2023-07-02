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
    outputfile.write("\n\n==================== Parse logs ====================")
    for log_type in repo.log_types:
        print("\tParsing {} logs".format(log_type))
        outputfile.write("\n\n=== Parse {} logs".format(log_type))
        if log_type == 'hostd':
            filename = "hostd.*"
        else:
            filename = "{}*".format(log_type)
        logs = tasks.find_logs(repo, filename)
        for log in logs:
            print("\t{}".format(log))
            contents = tasks.open_file_return_list(log, outputfile)
            results = tasks.log_search(repo, contents, log_type)
            if results and len(results) > 1:
                table = PrettyTable(results[0])
                table.add_rows(results[1:])
                outputfile.write("\n\n{}\n".format(log))
                outputfile.write(str(table))

#============================================================
# Parse for SVIP. Wishlist: combine this with parse_logs
def parse_svip(repo, outputfile):
    outputfile.write("\n\n==================== Parse logs for SVIP {} ====================".format(repo.svip))
    for log_type in repo.log_types:
        print("\tParsing {} logs".format(log_type))
        outputfile.write("\n=== Parse {} logs\n".format(log_type))
        if log_type == 'hostd':
            filename = "hostd.*"
        else:
            filename = "{}*".format(log_type)
        logs = tasks.find_logs(repo, filename)
        for log in logs:
            print("\t{}".format(log))
            contents = tasks.open_file_return_list(log, outputfile)
            results = tasks.svip_search(repo, contents)
            if results and len(results) > 1:
                table = PrettyTable(results[0])
                table.add_rows(results[1:])
                outputfile.write("\n{}\n\tWarnings or errors for svip {}\n".format(log, repo.svip))
                outputfile.write(str(table))
                                 
#============================================================
# Parse for specific volume id. Wishlist: combine this with parse_logs               
def parse_volume(repo, outputfile):
    outputfile.write("\n\n==================== Parse logs for Volume ID {} ====================\n".format(repo.volume_id))
    for log_type in repo.log_types:
        print("\tParsing {} logs".format(log_type))
        if log_type == 'hostd':
            filename = "hostd.*"
        else:
            filename = "{}*".format(log_type)
        logs = tasks.find_logs(repo, filename)
        for log in logs:
            print("\t{}".format(log))
            contents = tasks.open_file_return_list(log, outputfile)
            results = tasks.volume_search(repo, contents)
            if results:
                outputfile.write("\n{}\n".format(log))
                for line in results:
                    outputfile.write(line)