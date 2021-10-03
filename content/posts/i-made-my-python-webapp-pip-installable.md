Title: I made my python webapp installable via pip
Date: 2021-10-02 19:49
Slug: i-made-my-python-webapp-pip-installable

Running `pip3 install pytaku` now gives you all the tools you need [^1] to
deploy [pytaku][3] - a hobby webapp of mine - on a fresh Debian 11 server:

```sh
pytaku-generate-config > pytaku.conf.json  # generate config file
pytaku-migrate  # generate initial sqlite3 db, or migrate to new version
pytaku -w 5  # run main webapp using gunicorn on localhost:8000
pytaku-scheduler  # daemon that executes scheduled background tasks

# Optionally, run this to copy all static assets to a designated dir so your
# web server (nginx/caddy/etc.) can serve them directly instead of through
# the less performant gunicorn:
pytaku-collect-static /var/www/pytaku
```

So how does that work? Let's break it down.

## The pytaku-\* executables

[Poetry][4] is awesome. Not only does it offer sane dependency management that
plays well with the pyenv + virtualenv combo, but it also vastly simplifies
building and publishing python libraries. Telling pip to install executables
alongside my library is as simple as writing a few lines in my
[pyproject.toml][5] file:

```toml
[tool.poetry.scripts]
pytaku = "pytaku:serve"
pytaku-dev = "pytaku:dev"
pytaku-migrate = "pytaku:migrate"
pytaku-generate-config = "pytaku:generate_config"
pytaku-scheduler = "pytaku:scheduler"
pytaku-collect-static = "pytaku:collect_static"
```

The left hand side indicates the executable file name, while the right hand
side declares which function to call. In my example, "pytaku:serve" points to
the serve() function inside src/pytaku/\_\_init\_\_.py.

Now that we have easy access to CLI entry points, let's quickly go over
[how][7] each command works:

- `pytaku` and `pytaku-dev` simply exec gunicorn and flask respectively
  behind the scene.
- `pytaku-migrate` runs my bespoke migrator script (which is extremely
  primitive but hey it was a good learning experience).
- `pytaku-generate-config` uses [goodconf][6] to generate a config template,
  pre-filling as many values as it can.
- `pytaku-scheduler` is just a dead simple single-threaded scheduler that I
  don't recommend for any service that has more than a handful of users.
- `pytaku-collect-static` leverages importlib.resources.path to get the
  package's installation path. From there it copies the bundled static assets
  to wherever you want your nginx to serve. It's basically a simplified version
  of Django's collectstatic command.

## But why bother?

Lincoln Loop's series of Django-related blog posts were my main inspiration.
Central to this idea is [Using setup.py in Your (Django) Project][8], which
explains both how and why you would want to make your python project
pip-friendly. The "why" boils down to 2 points:

- You don't want to reinvent package management. Let pip handle the minute
  details of packaging, distributing, versioning, etc. for you.
- You no longer need to run python from the source code's path. In pytaku's
  case, the working dir now only stores the sqlite database file and the
  json config file, i.e. purely data, completely separate from the source
  code.

More broadly, the idea of simple distributing/deployment is, in my opinion,
often overlooked these days. Fiddly deployment procedures are largely why
Docker flourished: our industry just collectively gave up on self-contained
software distribution and decided to ship a whole rootfs for each application
process instead. Okay, I may be overreacting here, but I think it's at least
fair to say that if every webdev shop standardized on shipping Go binaries
statically compiled with musl libc, we'd probably reach out for Docker less
often. When I showed pytaku to a colleague of mine, his first question was
essentially "Dockerfile when?". Sure, Docker is neat and solves real problems,
but how about we strive to avoid, or at least minimize, those problems in the
first place? Remember, while container evangelists love harping on about
negligible CPU overhead, they tend to gloss over the storage overhead:

```sh
$ docker image ls
REPOSITORY   TAG        IMAGE ID       CREATED       SIZE
python       3-alpine   bcf864391ba1   3 weeks ago   45.1MB
python       3-slim     66f4843b721f   3 weeks ago   122MB
```

And the operational complexity overhead. Did you know that by default Docker
[completely sidesteps your firewall][9]? That even if you specifically tell it
to only listen to a port on localhost, it may or may not still expose it to the
whole world? That this remains an [open bug since 2016][10]? This isn't one of
those security bogeyman stories either, actual people have been [bitten by
it][11]. At this point cloud apologists would probably jump in and point out
how this isn't an issue if you're running on GCP or AWS because they have
another layer of firewall that locks down every port by default that you can
setup on their totally usable web console or infrastructure-as-code it in your
cloudformations or your terraformses or, actually, do you have a moment to talk
about our lord and savior Cthulhubernetes--

But I digress.

I guess what I was trying to say is, throwing abstractions over complex
procedures is simply shifting the costs elsewhere. Shipping your software in a
Dockerfile is fine, but making your distribution so simple that people can
easily write a couple of lines of Dockerfile for it by themselves is more
valuable. Simple distribution is simple to deploy regardless of whether you're
using docker, packer, ansible, pyinfra, podman, nomad, k8s, k3s, an
impenetrable shell script some dude wrote 2 years ago who just left the company
last month... or any combination of the above. The point is **you shouldn't be
forced to use more heavyweight solutions just because the software is a pain in
the butt to setup manually**.

And other people _have_ been trying to make python application distribution
simpler:

- [shiv][12] bundles everything but the python interpreter
- [PyOxidizer][13] bundles everything _including_ the python interpreter
- [nuika][14] actually compiles your python application into an executable,
  unlike PyInstaller which just generates a self-extracting archive.

We'll get there. Someday.


[^1]: Well actually you still need to `apt install python3-apsw`, but that's
  only because apsw [refuses][2] to provide a binary wheel on pypi. It can be
  replaced by the standard library sqlite3 module anyway - I only picked apsw
  because it exposes essentially the same API as the SQLite C library, which
  helped when I was learning to use SQLite properly for the first time.

[^2]: Even with the above, pytaku still won't run out of the box because it
  needs a [crappy proxy](https://github.com/nhanb/gae-proxy/) in order to
  bypass mangasee's strict cloudflare protection. I know it's lame but pytaku
  is practically a web scraper project and there's no way to make it work
  reliably without a proxy pool anyway. I hope this doesn't distract you from
  the point of the article though.

[1]: https://git.sr.ht/~nhanb/pytaku/tree/ff20e51f8c178bf981d80aa3737bf31a1059a506/item/README.md#production
[2]: https://rogerbinns.github.io/apsw/download.html#easy-install-pip-pypi
[3]: https://sr.ht/~nhanb/pytaku/
[4]: https://python-poetry.org/
[5]: https://git.sr.ht/~nhanb/pytaku/tree/ff20e51f8c178bf981d80aa3737bf31a1059a506/item/pyproject.toml#L15-21
[6]: https://github.com/lincolnloop/goodconf
[7]: https://git.sr.ht/~nhanb/pytaku/tree/ff20e51f8c178bf981d80aa3737bf31a1059a506/item/src/pytaku/__init__.py
[8]: https://lincolnloop.com/blog/using-setuppy-your-django-project/
[9]: https://www.jeffgeerling.com/blog/2020/be-careful-docker-might-be-exposing-ports-world
[10]: https://github.com/moby/moby/issues/22054
[11]: https://blog.newsblur.com/2021/06/28/story-of-a-hacking/
[12]: https://shiv.readthedocs.io/en/latest/
[13]: https://github.com/indygreg/PyOxidizer
[14]: https://nuitka.net/
