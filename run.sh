#!/bin/bash

# take in the target ip address as the first argument
TARGET_IP="$1"

if [ -z "$TARGET_IP" ]; then
    echo "Usage: $0 <target_ip>"
    exit 1
fi

# run audio receiver and receiver with the target ip address (only display output for receiver)
python3 audioreceiver.py &    # run in background, suppress output
python3 receiver.py &         # run in foreground, show output

# wait until enter is pressed to run 
read -p "Press Enter to start sending..."

# run audio sender and sender with the target ip address
python3 audiosender.py "$TARGET_IP" &
python3 sender.py "$TARGET_IP"