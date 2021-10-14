# TickDetector
PTN's own in-house BGS tick detector for Elite Dangerous.

## How it works (or, how it's *going* to work)

* Using player generated [journal](https://elite-journal.readthedocs.io/) data received from [EDDN](https://github.com/EDCD/EDDN)'s relay, each Faction in a given System has its current textual influence % recorded as a hash.

* Within-system hashes across an observed window are maintained where there is sufficient data.  Systems with sufficient data are 'Tracked'.

* Whenever a new entry about a Tracked System is received, the new hash is compared against existing ones, if they differ, the System is labelled as 'Ticked' until the change goes out of scope.

* If a significant* proportion of observed systems are 'Ticked', it can be inferred that the daily server-side tick has began.

* A notification of the Tick's details can then be sent to other programs, such as via webhook to Discord.

*invariably, 3rd party user-provided data is not the 'cleanest', so false-positive system updates do occur.  Setting a threshold for the Ticked:Tracked ratio resolves this.

## How it has been implemented

A System class maintains it's name, and received hash values across a several time-based intervals (eg: every 5 mins in an hour, so a list of 12 hashes).

Systems maintained in a list by SystemManager, whose methods are called by two threads using multithreading:

* EDDNThread, which actively listens for System data from EDDN. It creates new Systems, and updates existing ones with incoming data.

* IteratorThread, which runs once every interval (eg. once every 5 mins). It calls interval-relevant functions on all observed systems (CRUD).

Some details have been glossed over here, please read the SystemManager class' implementation for more details.
