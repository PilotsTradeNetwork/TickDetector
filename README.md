# TickDetector
PTN's own in-house BGS tick detector for Elite Dangerous.

## How it works
A System object is maintained for every (populated) system pinged on EDDN within the last hour, on 5 minute intervals.

To save memory, a hash of a system's overall faction state at each interval is used to represent a unique state.  The value of this hash will change when the state changes.