Hacking-Guide
=============

Architecture
------------

The firmware for the alarmclock is implemented in python. The main program
is the script `/usr/local/sbin/ambieye.py`, which is started by
the systemd-service defined in `/etc/systemd/system/ambieye.service`.


The main script does not contain much logic. It mainly creates and loads
various object taking care of the hardware. All classes are submodules
of the `ncolors`-module. During installation, the code is copied to
`/usr/local/lib/python2.7/site-packages/ncolors`.

Logically, the software follows the MVC paradigm.
The model is implemented in the class `Settings`. The `LedController` is the view,
and the `WebThread` is the controllers.

Objects don't call methods directly, they only change attributes in
the `Settings`. They also register callbacks for attribut-changes
there and are called when the registered attribute changes.
