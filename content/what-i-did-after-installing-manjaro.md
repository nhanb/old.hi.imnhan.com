Title: What I did after installing Manjaro xfce
Slug: what-i-did-after-installing-manjaro-xfce
Date: 2014-02-04 20:20:13

After about 2 months with elementary OS, I got sick of the guaranteed once-every-hour crashes of
its **Files** file manager (yeah, I'm still hating their naming decisions with a passion), the
flickering when I play fullscreen OpenGL games, and the automatic collapsing of workspaces. I've
had enough of that. Let's go back to xfce! But hey, (X)ubuntu 14.04 is nearly out but I don't want
to install an alpha version right now, and installing 13.10 just to update 2 months later is insane
(to me, at least). That's when I noticed Manjaro - a battery-included distro based on Arch. All
hail rolling release!

Although Manjaro comes packed with most of the apps that I would install on any other distro
anyway: GIMP, LibreOffice, Steam, etc., here are some additional steps I took to make it rock.

## Get Mirosoft fonts

Getting Micro$oft fonts is like the first thing to do after any Linux distro installation. The Arch
community has a whole [wiki page][1] dedicated to it. It's worth mentioning that you can't
*legally* install those packages without the actual fonts already on your computer. Assuming you
have an installed copy of Windows 7, go to its `Fonts` folder and put the necessary fonts in the
same folder of the extracted package downloaded from the AUR page. For some instant copy-and-paste
commands: (**warning**: this script assumes you already have all your Windows 7 fonts in
`~/win_fonts/`. Put them there before running the following commands)

    :::bash
    curl -O 'https://gist.github.com/nhanb/8804875/raw/arch-ms-fonts.sh'
    bash arch-ms-fonts.sh

For 

[1]: https://wiki.archlinux.org/index.php/MS_Fonts
