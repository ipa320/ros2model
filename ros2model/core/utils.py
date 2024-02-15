import psutil


def find_process_by_node_name(node_name, namespace):
    for process in psutil.process_iter(["pid", "cmdline"]):
        try:
            cmdline = process.info["cmdline"]
            if namespace in str(cmdline) and node_name in str(cmdline):
                cmdline_list = cmdline[0].split("/")
                return cmdline_list[-2], cmdline_list[-1]
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return "TODO", "TODO"
