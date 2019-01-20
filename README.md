ambieye
===========

A Pi-Zero W based led light with an web-interface to control the color and brightness.


Table of Contents
-----------------

  1. [News and Status](#news "News")
  2. [Installation](#install "Installation")
  3. [Hardware](#hardware "Hardware")
  4. [Prerequisites](#prerequisites "Prerequisites")
  5. [Configuration](#configuration "Configuration")
  6. [Usage](#usage "Usage")
  7. [Hacking](#Hacking "Hacking")


News
----

As always, the software and documentation is work in progress.
A detailed list of functions (current and planned) is available in the
document [Features](doc/features.md "Features"). Nevertheless, once in a
while I will release a stable version.

Available branches:

  - **stable_v?**: stable versions (frozen)
  - **master**: the current stable branch plus fixes
  - **next**: the bleeding-edge development version with new features, but
              possibly unstable

### next / work in progress ###

Planned features:

  - sound controlled lights

### stable_v1 /  Jan 6, 2018 ###

First productive version. All basic features working.


Prerequisites
-------------

Besides the hardware-modules listed in section [Hardware](#hardware "Hardware")
and the software-environment described in
[Installation](#install "Installation") there are no special prerequisites.


Hardware
--------

From hardware-side, you need

  - a Pi with internet access (a Pi-Zero-W will do fine)
  - the [LED-strip *Blinkt!* from Pimoroni](https://shop.pimoroni.com/products/blinkt "Blinkt!")


Installation
------------

As a prerequisite, you need a basic install of Raspbian Stretch-Lite.

Use the following commands to install the software:

    git clone https://github.com/benjaminfuchs/ambieye.git
    cd ambieye
    sudo tools/install

This will pull-in all dependencies, install the software, create technical
users and do a basic configuration of the system. Since the install command
changes the file `/boot/config.txt`, you need a reboot to activate the changes.


Upgrade
-------

Before uprading an existing system, you should stop the relevant system
services:

    sudo systemctl stop ambieye.service

Then run a normal install like documented above. After installation, you
should update you existing `/etc/ambieye.conf` from the file
`/etc/ambieye.conf.ambieye`.


Configuration
-------------

### System services ###

Edit the file `/etc/ambieye.conf` to configure the systemd-service
running the clock.


### Manual configuration ###

Program defaults are in the file `/var/lib/ambieye/defaults.json`.
You should not edit this file directly (unless you know what you are
doing). After first run, the settings are saved in
`/var/lib/ambieye/settings.json`. You can edit this file
manually, but you should make sure the clock-service is stopped before
doing so (it will be otherwise overwritten).


Usage
-----

After initial configuration as explained above, restart the system and then
it should just run. You can than use web-interface to change the color and
brightness or change other settings.


Hacking
-------

If you want to change the code and adapt it for your needs, you need some
python know-how and you have to understand the structure of the program.
For details read the [hacking-guide](doc/hacking.md "Hacking-Guide").


Credits
-------

Big thanks to Bernhard Bablok for his [nerd-alarmclock](https://github.com/bablokb/nerd-alarmclock)
which was used as template for this project.
