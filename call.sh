#!/bin/bash

# Debug message with the passed number
echo "Debug: number passed to script is $1"
number=$1

# Function to check if the device is rooted
is_rooted() {
  if [ "$(id -u)" -eq 0 ]; then
    return 0
  else
    return 1
  fi
}

# Function to make a call in the background (requires root)
call_in_background() {
  echo "Device is rooted. Attempting to make call in background..."
  if svc data enable && service call phone 2 s16 "$number"; then
    echo "Call initiated to $number in the background."
    svc data disable
  else
    echo "Failed to make call in background. Falling back to normal call..."
    call_normal
  fi
}

# Function to make a normal call (foreground)
call_normal() {
  echo "Making normal call..."
  am start -a android.intent.action.CALL -d tel:$number
  if [ $? -ne 0 ]; then
    echo "Failed to make normal call. Falling back to termux-telephony-call..."
    termux_telephony_call
  fi
}

# Function to make a call using termux-telephony-call
termux_telephony_call() {
  echo "Attempting to make call using termux-telephony-call..."
  termux-telephony-call $number
}

# Main script execution
if is_rooted; then
  call_in_background
else
  call_normal
fi
