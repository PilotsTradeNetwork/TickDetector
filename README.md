# TickDetector
PTN's own in-house BGS tick detector for Elite Dangerous.

## How it works
A System object is maintained for every (populated) system pinged on EDDN within the last hour, on 5 minute intervals.

To save memory, a hash of system's overall faction state at each interval is created and stored on receipt of an faction status update