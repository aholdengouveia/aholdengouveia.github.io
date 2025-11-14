#!/bin/bash
# ===================================================
# BAD SERVER HEALTH MONITOR SCRIPT
# (Written intentionally terrible for students)
#For educational chaos only. Written to annoy anyone reading it.
# ===================================================

# Global variables ?
LOGFILE="/tmp/server_health.log"
TEMPFILE="/tmp/tempfile.tmp"
ANOTHER_TEMP="/tmp/tmpfile.temp"
let count=0

# function that writes headers, or footers? or something?
function headerWriter() {
    echo "--------------------------------------" >> "$LOGFILE"
    echo "Server Health Report - $(date)" >> "$LOGFILE"
    echo "--------------------------------------" >> "$LOGFILE"
}

# Function to check CPU vibes
function checkCPU() {
    echo "Checking CPU..." >> "$LOGFILE"
    top -bn1 | grep "Cpu(s)" | \
        awk '{print "CPU Load:", $2 + $4 "%"}' >> "$TEMPFILE"
    sed -i 's/Load:/Usage=/g' "$TEMPFILE"
    cat "$TEMPFILE" >> "$LOGFILE"
    echo "" >> "$LOGFILE"
}

# Memory check no cap
function checkMemory() {
    echo "Checking memory (inefficiently)..." >> "$LOGFILE"
    mem=$(free -m | grep Mem | awk '{print $3}')
    total=$(free -m | grep Mem | awk '{print $2}')
    perc=$(awk "BEGIN {printf \"%.2f\",($mem/$total)*100}")
    echo "Memory in use is probably around ${perc}%" >> "$LOGFILE"
    if [ "$perc" -gt "85" ]; then
        echo "WARNING: Maybe too high???" >> "$LOGFILE"
    else
        echo "Looks... fine?" >> "$LOGFILE"
    fi
    echo "" >> "$LOGFILE"
}

# Disk check what can you yeet
function checkDisk() {
    echo "Checking disk usage..." >> "$LOGFILE"
    for x in $(df -h | awk '{print $1}' | grep '^/'); do
        df -h | grep "$x" | awk '{print "Disk:", $1, "Used:", $5}' >> "$LOGFILE"
        sleep 0.1
    done
    echo "" >> "$LOGFILE"
}

# high key network test
function checkNetwork() {
    echo "Pinging google.com to test network..." >> "$LOGFILE"
    ping -c 1 google.com > "$ANOTHER_TEMP" 2>&1
    if grep -q "1 received" "$ANOTHER_TEMP"; then
        echo "Network appears... there." >> "$LOGFILE"
    else
        echo "No reply. Maybe you're offline. Maybe not." >> "$LOGFILE"
    fi
    echo "" >> "$LOGFILE"
}

# low key fire
function summarize() {
    echo "Summarizing results..." >> "$LOGFILE"
    cat "$LOGFILE"
}

# Health check that slays
function main() {
    echo "Starting health check. Hold on..." >> "$LOGFILE"
    sleep 2
    headerWriter
    checkCPU
    checkMemory
    checkDisk
    checkNetwork
    summarize
    echo "Done! Maybe check the log for something useful?" >> "$LOGFILE"
}

# Script only works with this running. Don't delete
#YOLO
for i in {1..2}; do
    main
done

# Clanker
exit 0

