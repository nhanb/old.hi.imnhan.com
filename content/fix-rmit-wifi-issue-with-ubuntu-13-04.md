Title: Fix RMIT wi-fi issue in Ubuntu 13.04 and variants
Date: 2013-06-17 08:12
Category: tutorials
Tags: ubuntu, linux
Slug: fix-rmit-wifi-issue-in-ubuntu-13-04-and-variants
Summary: The problem is NetworkManager, there's a workaround but nobody has been assigned to formally fix it.

## The issue

When I upgraded to Xubuntu 13.04, although I could connect to any other wi-fi network painlessly,
the RMIT-WPA network just never allowed me to establish a connection. The most annoying part was
that it had been working fine in previous versions (12.04, 12.10).

After days of googling, I finally pinpointed the issue: a certain version of NetworkManager
bundled in Ubuntu 13.04 has a bug that automatically turns CA certificate usage to *true* for any
WPA2 wifi network, even if we choose to use none in the GUI.

![RMIT wi-fi settings](/static/images/rmit_wifi.png)

## The solution

Just manually edit `/etc/NetworkManager/system-connections/RMIT-WPA`, make sure that you have
`system-ca-certs=false`, then restart the wifi connection. To edit this file you will need root
permission. If you're not sure how to do this, open a terminal and enter this command to open
`gedit` with sudo permission (`mousepad` if you're using xubuntu):

    :::bash
    # Protip: DON'T use sudo for GUI programs! Use gksudo instead.
    gksudo gedit /etc/NetworkManager/system-connections/RMIT-WPA

This is a [known bug](https://bugs.launchpad.net/ubuntu/+source/network-manager/+bug/1104476) and
many have complained about it. There seems to be no developer assigned to fix it though. I'll keep
you updated on the issue.
