Title: Acer Chromebook Spin 713 "Voxel": an adequate Crostini device, a buggy Linux laptop
Date: 2023-04-22 15:55
Slug: acer-chromebook-spin
Category: consoom

**TL;DR:** bright crisp screen, acceptable keyboard, thin & light build, buggy
touchpad even on ChromeOS, almost usable on MrChromebox UEFI + Arch Linux
except for the fact that sound crashes most of the time. It's absolutely not
worth the sticker price at [$1,099.99][1] (lol). Maybe consider buying if you can
find it at a heavy discount and the Linux sound issue has been fixed somehow.

## Context

Sometime in 2022 I was looking for a replacement for my T530---something
lighter with a better screen---and saw a listing for a used Acer Chromebook
Spin 713-3W at only 10mil VND ($425, give or take). A recently released HiDPI
laptop with an i5-1135G7 at 425 freedom dollars? And I get to play with
ChromeOS/Crostini on a not-pathetically-weak x86 device? Sign me right up, I
thought. The plan was to run ChromeOS/Android apps for GUI stuff, and install
my usual tmux+vim based development [environment][2] on Crostini.

## ChromeOS/Crostini

As advertised, the laptop can run ChromeOS apps, Android apps, and Linux apps
via containers. By default I got a Debian container, but since I need
up-to-date software for development, I set up an Arch container instead. [The
process][3] itself was straightforward enough.

Zoom for Android worked as expected, and to my surprise, Tailscale for Android
managed to wrangle traffic correctly for programs running inside Crostini too!
The only hiccup was that Magic DNS didn't work, so I needed to put the
hostname-IP pairs into /etc/hosts manually. I also had to change the temp dir
from /tmp to ~/tmp for golang tools to work, because Crostini programs weren't
allowed to exec files inside /tmp or something like that.

[1]: https://www.acer.com/us-en/chromebooks/acer-chromebook-enterprise-spin-713-cp713-3w/pdp/NX.AHAAA.006
[2]: https://git.sr.ht/~nhanb/neodots
[3]: https://wiki.archlinux.org/title/Chrome_OS_devices/Crostini
