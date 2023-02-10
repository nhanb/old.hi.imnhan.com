Title: Go, Postgres, Caddy, systemd: a simple, highly portable, Docker-free web stack
Slug: go-postgres-caddy-systemd-stack
Date: 2023-02-12 14:24

I've [mentioned][1] before that I'm not a fan of Docker as a deployment
strategy. In that same post I briefly mentioned that Go could simplify
deployment compared to Python. Today I'll _go_ (haha get it?) into detail,
warts and all, how I recently set up a publicly accessible Go web service,
backed by a Postgres database, fronted by Caddy which does TLS termination &
automatic Let's Encrypt cert renewal, supervised & isolated by systemd.

## Go

If you're new to Go like me, you may find it helpful to skim the book [Let's
Go][2] by Alex Edwards. It demonstrates helpful patterns so you can quickly put
together a web service with little more than the Go standard library. However,
it's cumbersome to define routes using only `net/http`, so I recommend using
the very minimal [flow][3] routing library written by the same author: it
offers a cleaner API while having very little code itself. Heck, you should
probably vendor it and later customize whichever way you want.

As for the PostgreSQL driver, I chose [github.com/lib/pq][4] simply because
it's a pure Go library that implements the standard `database/sql` interface.
I preferred to learn the most common API before branching into more
special-purpose stuff. It quickly became tedious and error-prone to write all
that boilerplate for reading data into Go structs though. I heard good things
about [sqlc][5], which generates Go code from SQL queries. I'll most likely try
that next.

Sticking to pure Go code brings 2 big benefits: **independence from glibc** and
**effortless cross-compilation**.

Not depending on glibc means our compiled executable for, say, Linux, will run,
not only on any Linux distro regardless of its glibc version, but also on
distros that use alternative libc implementations e.g. musl. Coming from
Python, it's incredibly liberating to no longer have to find an ancient distro
with the oldest possible glibc to build my executables on (most Python projects
that do anything useful use C extensions, sadly). It's not without caveat
though: some of Go's own standard libraries, namely `net` and `os/user`, use cgo
by default. We can set `CGO_ENABLED=0` to avoid that, which tells the Go
compiler to use their alternative pure Go implementations, but those are not as
full-featured. If your code or dependency requires those, make sure to check if
they work correctly with the pure Go version. The easiet way to confirm that
your compiled executable is truly static is using either `ldd` or `file`:

```sh
$ ldd mybinary
#        not a dynamic executable

$ file mybinary | tr , '\n'
# mybinary: ELF 64-bit LSB executable
#  x86-64
#  version 1 (SYSV)
#  statically linked
#  Go BuildID=[...]
#  with debug_info
#  not stripped
```

Cross-compilation is self-explanatory: out of the box, you can compile to any
architecture/OS combination that Go supports. No more looking for the right CI
service or docker container to build your stuff in.

See also:

- [cgo is not Go][11]—a more exhaustive argument for staying in pure
  Go-land.
- [Statically compile Go programs][16]—a deep dive into static Go compilation
  and its quirks, complete with examples on how to statically link against
  SQLite with musl libc, if you must.

## Postgres

While SQLite is a fine choice for small-to-medium sites, it does have its own
quirks: so-called [flexible type checking][6] and [limited ALTER TABLE
capabilities][7] are my two pet peeves.

Postgres has none of those quirks, but causes extra operational complexity, not
only for deployment, but also for development: you now need to erect a Postgres
server with the right db/user/password combination for each project.

From the local development perspective, this is actually one of the few cases
where Docker rightfully shines: whip up a tiny docker-compose.yml, hit that
`docker-compose up` command, and you've got yourself a nicely isolated,
delightfully disposable postgres server with your desired user/password/db
combination, exposed at the exact port you want:

```yaml
# docker-compose.yml
version: '3.9'
services:
  db:
    image: postgres:15
    ports: 127.0.0.1:5432:5432
    environment:
      POSTGRES_USER: example
      POSTGRES_PASSWORD: example
      POSTGRES_DB: example
```

Since a developer's computer is typically not lacking in resources, we can get
away with docker's storage overhead, and, in MacOS's case, VM overhead.

But what if we want to stick to our anti-docker guns? Good news: it's still
possible to have [Per-project Postgres][8] instances. Here's the gist:

```sh
cd my-project
mkdir .pgres # postgres data dir

# These envars tell postgres cli tools to:
# a) put data files in .pgres
# b) connect to server via a socket inside .pgres
export PGDATA="$PWD/.pgres"
export PGHOST="$PWD/.pgres"

initdb # populate .pgres/

echo "listen_addresses = ''" >> .pgres/postgresql.conf
echo "unix_socket_directories = '$PGHOST'" >> .pgres/postgresql.conf

echo "CREATE DATABASE $USER;" | postgres --single -E postgres
```

_(I also made a [python script][9] to automate this process)_

Now whenever you develop on this project, just cd into the project dir, make
sure $PGDATA and $PGHOST point to the correct dir, then run `postgres`. You can
save those environment variables into a `setenv.sh` script to source every
time, or use tools like [direnv][10] to automatically set them on cd. When you
no longer need it, cleaning up is as simple as removing the .pgres dir.

On the server side, if you're on, say, Debian, the Postgres developers maintain
an [Apt repo][13] that provides any currently supported version of Postgres, so
you can always use the latest and greatest DB while still enjoying the
stability of Debian. Just follow the instructions to add the repo, install your
preferred postgres version, then enable & start the postgresql service using
`systemctl`.

You'll then need to follow the distro's [convention][12] to create a DB with
its dedicated username/password combination. Here's how I set up mine:

```sh
$ su - postgres
(as postgres) $ createuser --pwprompt mypguser
(as postgres) $ createdb -O mypguser mypgdatabase
```

I didn't bother to create a dedicated OS user, because I'll later use systemd's
DynamicUser feature to run my service on its own dynamically created user
anyway. This brings us to...

## systemd

Inevitably you'll need something to manage your service process: autostart on
boot, report/restart when it goes down, piping logs to the right place, that
sort of thing. People used to install things like [supervisord][14] for that.
(Docker Compose would kinda work too, but we're trying to see if we can avoid
gratuitous container usage here, remember?)

Nowadays though, systemd is already pervasive in mainstream Linux distros, and
comes tightly integrated with supporting services e.g. journald, so it makes
little sense to use anything else for service management.

To limit the blast radius if (when?) a service gets pwn'ed, it's recommended to
run each service as its own OS user that only has access to what it actually
needs. In the past I used to create 1 system user to run each service as, but
this time I realized I could use systemd's [DynamicUser][15] instead:

```ini
# /etc/systemd/system/myservice.service
[Service]
ExecStart=/usr/local/bin/myservice
Environment=MYSERVICE_DB=postgres://db-user:db-password@localhost/db-name
Environment=MYSERVICE_ADDR=localhost:8000
DynamicUser=1
Restart=always

[Install]
WantedBy=multi-user.target
```

It's just a little less work compared to creating a system user with the
correct restrictions and running the service under that user, but hey, less
work is less work! Also that's one fewer thing that I have to worry about
messing up.

You may have noticed the `ExecStart=/usr/local/bin/myservice` line, which
assumes my service's executable is in /usr/local/bin/. Since my service is only
1 binary with no support files, this, and postgres credentials (provided via
the `MYSERVICE_DB` envar), are all that's needed to run the service. It also
means for subsequent deployments, this will be my entire deployment procedure:

```sh
# compile:
CGO_ENABLED=0 go build -o dist/myservice
# copy binary to server (scp works too):
rsync -av dist/myservice myserver:/usr/local/bin/myservice
# restart service:
ssh myserver systemctl restart myservice
```

## Caddy

Nowadays I prefer [Caddy][17] as the TLS-terminating reverse proxy instead of
nginx, since it transparently performs Let's Encrypt's ACME challenge behind
the scene. With my web service listening at localhost:8000, it literally takes
2 lines of config to:

- Serve HTTPS at port 443, with a valid cert provided by Let's Encrypt, using
  reasonable default cryptographic settings—I just ran my site through the
  [ssllabs.com test][18] and it handily scored an A.
- Serve HTTP at port 80 that simply redirects to the HTTPS port

```nginx
# /etc/caddy/Caddyfile
my-domain.com {
    reverse_proxy localhost:8000
}
```

There are many interesting problems to solve when running a web service, and
HTTPS cert bookkeeping is not one of them, so I'm more than happy to stop
fiddling with certbot cron jobs.

## Closing remarks

For a proper production-grade service, there's more to be done:
personally I'm using `ufw` to lock down everything except for the HTTP(S) ports
and wireguard (I'm doing ssh over wireguard only too). Enabling unattended
upgrades is also a good idea. But of course these depend heavily on each
person's requirements and tastes.

Of course I'm not advocating for manual "pet" server maintenance everywhere.
Nothing from this setup prevents you from doing proper automated provisioning,
configuration management, so on and so forth. In fact, it is easier to e.g.
write an ansible playbook for this setup, because it's simpler: you don't have
to worry about setting up the correct python virtual environment, or making
nginx and certbot play well with each other. Hell, you can dockerize parts of
this setup, and your Dockerfiles will be simpler thanks to it. I've [said it
before][1], and I'll say it again:

> Throwing abstractions over complex procedures is simply shifting the costs
> elsewhere. Shipping your software in a Dockerfile is fine, but making your
> distribution so simple that people can easily write a couple of lines of
> Dockerfile for it by themselves is more valuable. Simple distribution is
> simple to deploy regardless of whether you're using docker, packer, ansible,
> pyinfra, podman, nomad, k8s, k3s, an impenetrable shell script some dude
> wrote 2 years ago who just left the company last month... or any combination
> of the above. The point is **you shouldn't be forced to use more heavyweight
> solutions just because the software is a pain in the butt to setup
> manually**.

Sooner or later we'll all have to peek under the hood to diagnose problems, and
the fewer moving pieces you have to learn and understand, the more grateful
you'll be to your predecessors (and, let's be honest, the fewer profanities
you'll have to utter to yourself).

[1]: /posts/i-made-my-python-webapp-pip-installable/
[2]: https://lets-go.alexedwards.net/
[3]: https://www.alexedwards.net/blog/introducing-flow
[4]: https://github.com/lib/pq
[5]: https://sqlc.dev/
[6]: https://www.sqlite.org/flextypegood.html
[7]: https://www.sqlite.org/lang_altertable.html#making_other_kinds_of_table_schema_changes
[8]: https://jamey.thesharps.us/2019/05/29/per-project-postgres/
[9]: https://github.com/nhanb/neodots/blob/f79713b4e79c5da4fa92f75b1537b73b4c114d03/fish/scripts/standalone-postgres
[10]: https://direnv.net/
[11]: https://dave.cheney.net/2016/01/18/cgo-is-not-go
[12]: https://wiki.debian.org/PostgreSql
[13]: https://www.postgresql.org/download/linux/debian/
[14]: http://supervisord.org/
[15]: https://0pointer.net/blog/dynamic-users-with-systemd.html
[16]: https://www.arp242.net/static-go.html
[17]: https://caddyserver.com/
[18]: https://www.ssllabs.com/ssltest/
