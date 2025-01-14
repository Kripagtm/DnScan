#!/usr/bin/env python3

# A quick TCP port scanner that lets you specify a range of source ports to scan from
# Useful for identifying firewall rules that allow traffic from specific ports (such as 53 or 179)
# The lists of source and target ports are defined in the __main__ function below

import platform
import os
import socket
import sys

from itertools import repeat
from multiprocessing.dummy import Pool as ThreadPool
from socket import timeout

# Main scanning function
def scan(source_port, target, target_port):
    global verbose
    sys.stdout.write(str(source_port) + " -> " + target + ":" + str(target_port) + "     \r")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Adjust if you're testing something slow
    s.settimeout(0.5)
    try:
        s.bind(('', source_port))
    except OSError:
        if verbose:
            print("Source port " + str(source_port) + " in use, could not scan")

    try:
        s.connect((target, target_port))
        print(target + " allows connections to port " + str(target_port) + " from source port " + str(source_port))
    except timeout:
        pass
    except Exception as e:
        if verbose:
            print(str(source_port) + " -> " + target + ":" + str(target_port))
            print(e)

# Create the thread pool
def run_scan(target, target_portlist, portlist, thread_count=20):
    pool = ThreadPool(thread_count)
    for target_port in target_portlist:
        results = pool.starmap(scan, zip(portlist, repeat(target), repeat(target_port)))
    pool.close()
    pool.join()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " <target>\n")
        print("Source and target ports are hard-coded in the script")
        sys.exit(1)
    target = sys.argv[1]

    verbose = False
    thread_count = 20

    # Target ports to scan for
    target_portlist = [22, 80, 443, 8080, 8443]

    # Source ports to scan from
    # portlist = range(1, 65536)                    # Full scan (slow)
    portlist = [22, 53, 67, 179, 443, 705, 1025]    # Targeted list of source ports

    # Needs to be root to bind to ports < 1024
    if platform.system() == 'Linux' and os.geteuid() != 0:
        if not all(port >= 1024 for port in portlist):
            print("Not running as root.\n\nEither re-run with root privileges, or ensure that all source ports are above 1024")
            sys.exit(1)

    # Catch Ctrl+C and exit
    try:
        run_scan(target, target_portlist, portlist, thread_count)
    except KeyboardInterrupt:
        sys.exit(1)

