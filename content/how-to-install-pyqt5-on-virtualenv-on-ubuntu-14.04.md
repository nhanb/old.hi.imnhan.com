Title: How to install PyQt5 on a virtualenv on Ubuntu 14.04
Slug: how-to-install-pyqt5-on-virtualenv-on-ubuntu-14.04
Date: 2015-02-14 22:33
Category: tutorials

The official way to install PyQt5 for development is to download and compile SIP + PyQt5 from
source, which is painstakingly slow (compiling PyQt5 took like 10 minutes on my PC). If you're
[compiling it against a virtualenv][1], rinse and repeat for each new virtualenv you create.
Alhough it is doable, I prefer something faster.

And yes, there is something faster. Today I came across a [Stack Overflow answer][2] that suggested
a neat trick: installing PyQt globally, then copy the whole thing to your virtualenv
**site-packages** directory. Here's how I did it on Ubuntu 14.04, python3.4 and PyQt5:

```bash
# assuming you already have virtualenv & virtualenvwrapper installed

# install pyqt5 globally
sudo apt-get install python3-pyqt5

mkvirtualenv -p `which python3` cookies
# (replace "cookies" with your actual virtualenv name, duh!)

LIBDIR="$HOME/virtualenvs/cookies/lib/python3.4/site-packages"
cp -r /usr/lib/python3/dist-packages/PyQt5 "$LIBDIR/PyQt5"
cp /usr/lib/python3/dist-packages/sip.cpython-*.so "$LIBDIR/"
```

And you're done with no compiling involved. Isn't that neat? :)

[1]: https://michalcodes4life.wordpress.com/2014/03/16/pyqt5-python-3-3-in-virtualenv-on-ubuntu/
[2]: http://stackoverflow.com/a/1962076
