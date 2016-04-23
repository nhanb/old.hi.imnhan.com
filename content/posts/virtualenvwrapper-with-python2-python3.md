Title: Virtualenv(wrapper), python2 and python3
Date: 2014-12-16 21:35
Category: tutorials
Tags: linux, vim, python
Slug: virtualenwrapper-python2-python3
Summary: TL;DR: Install virtualenv via `apt-get`, not `pip`, then `mkvirtualenv -p /path/to/python/executable`.


Virtualenv and virtualenvwrapper make it super easy to have a sandboxed python environment for each
of your projects, no doubt about it (if you're not using them already, feel free to google how to
get started).

By default, `mkvirtualenv my-env-name` will create a virtualenv using the OS's default python
version (in Ubuntu's case, that's python2). If you want a virtualenv that has `python` mapped to
python3 instead, use the `-p` argument:

```bash
$ mkvirtualenv -p `which python3` my-env-name
# assumming you have python3 installed already, of course!
```

However, on Ubuntu this will fail if you installed virtualenv as a pip package. If that's the case,
simply remove it and install the Ubuntu package instead. It goes like this for Ubuntu 14.04:

```bash
$ sudo pip uninstall virtualenv
$ sudo apt-get install python-virtualenv
$ sudo pip install virtualenvwrapper  # yes, you can install virtualenvwrapper via pip
$ mkvirtualenv -p `which python3` my-env-name
```

Neat, eh?
