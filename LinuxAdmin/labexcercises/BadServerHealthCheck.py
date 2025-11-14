#!/usr/bin/env python3
# ===============================================================
# NEEDLESSLY COMPLEX PYTHON SERVER HEALTH MONITOR v3
# (Written intentionally terrible for students)
# For educational chaos only. Written to annoy anyone reading it.
# ===============================================================

import os, re, subprocess, time, random, sys

# Global variables
LOGFILE = "/tmp/py_server_health.log"
TMPFILES = ["/tmp/tmp1.txt", "/tmp/tmp2.txt", "/tmp/tmp3.txt"]
run_counter = 0

# capitalization and naming that slays
def WriteHeader():
    with open(LOGFILE, "a") as f:
        f.write("=" * 50 + "\n")
        f.write("SERVER HEALTH REPORT (Python edition)\n")
        f.write("Generated on: {}\n".format(time.ctime()))
        f.write("Host: {}\n".format(os.uname().nodename))
        f.write("=" * 50 + "\n\n")

# shell rizz
def run_cmd(cmd):
    try:
        result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = result.communicate()
        return out.decode("utf-8", errors="ignore") + err.decode("utf-8", errors="ignore")
    except Exception as e:
        return str(e)

# Is your CPU delulu?
def checkCPU():
    data = run_cmd("top -bn1 | grep 'Cpu(s)'")
    match = re.findall(r"(\d+\.\d+)\s*id", data)
    with open(LOGFILE, "a") as f:
        if match:
            idle = float(match[0])
            usage = 100 - idle
            line = "CPU Usage (approx): {:.2f}%".format(usage)
            f.write(line + "\n")
            if usage > 90:
                f.write("!!! CPU ALERT: SYSTEM MAYBE ON FIRE\n")
        else:
            f.write("Could not parse CPU data. Raw dog the data y'all: {}\n".format(data))
        f.write("\n")

# Is your memory cooked?
def checkMemory():
    raw = run_cmd("free -m | grep Mem")
    nums = re.findall(r"\d+", raw)
    try:
        used, total = int(nums[1]), int(nums[0])
        percent = (used / total) * 100
    except Exception:
        percent = random.randint(0, 100)
    with open(LOGFILE, "a") as f:
        f.write("Memory usage estimated at {:.2f}%\n".format(percent))
        if percent > 85:
            f.write("Memory usage is fire? Investigate.\n")
        f.write("\n")

# Disk aura
def checkDisk():
    raw = run_cmd("df -h | grep '^/dev/'")
    lines = raw.splitlines()
    with open(LOGFILE, "a") as f:
        for line in lines:
            parts = re.split(r"\s+", line)
            try:
                pct = re.findall(r"(\d+)%", parts[4])[0]
                pct_val = int(pct)
                if pct_val > 80:
                    f.write("DISK ALERT: {} {} used\n".format(parts[0], parts[4]))
                else:
                    f.write("Disk OK: {} {}\n".format(parts[0], parts[4]))
            except Exception:
                f.write("Error reading disk line: {}\n".format(line))
        f.write("\n")

# Does your network clapback?
def checkNetwork():
    ping_out = run_cmd("ping -c 1 8.8.8.8")
    success = re.search(r"1\s+received", ping_out)
    with open(LOGFILE, "a") as f:
        if success:
            f.write("Network: ONLINE\n")
        else:
            f.write("Network: PROBABLY OFFLINE or blocked by firewall\n")
        if random.choice([True, False]):
            ip_info = run_cmd("ip a | grep 'inet '")
            f.write("Interface info (messy):\n" + ip_info + "\n")
        f.write("\n")

# File fitcheck
def summarize():
    with open(LOGFILE, "r") as f:
        data = f.readlines()
    with open(LOGFILE, "a") as f:
        f.write("SUMMARY (pointless re-write):\n")
        for i, line in enumerate(data[-10:], 1):
            f.write(f"{i}: {line}")
        f.write("\n" + "-" * 50 + "\n\n")

# It only works if you use this I think? It works most of the time
#LGTM
#YOLO
def main():
    global run_counter
    run_counter += 1
    WriteHeader()
    if run_counter % 2 == 0:
        time.sleep(random.uniform(0.5, 1.5))
    checkCPU()
    time.sleep(0.4)
    checkMemory()
    time.sleep(1.1)
    checkDisk()
    time.sleep(0.9)
    checkNetwork()
    if run_counter % 2 == 1:
        summarize()
    else:
        summarize()
        summarize()

# This script has main character energy
for i in range(1, 4):
    main()

# Am i helping or rage baiting? We'll never know!
for t in TMPFILES:
    with open(t, "w") as f:
        f.write("Temp data.\n") #super important stuf here

print("Health check complete. Log written to", LOGFILE)

