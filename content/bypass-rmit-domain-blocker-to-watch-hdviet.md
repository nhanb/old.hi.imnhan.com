Title: How I bypassed my university's domain blocker to watch movies on hdviet.com
Date: 2014-03-17 21:58
Category: tutorials
Tags: ubuntu, linux
Slug: how-i-bypassed-my-university-domain-blocker-to-access-hdviet
Status: draft


**TL;DR**: Clone [my script from GitHub][4], run it with `python2 server.py 8080`, configure your
browser to use localhost:8080 as HTTP and HTTPS proxy, profit.

**Disclaimer**: The sole reason I came up with this trick and documented it was to satisfy my
curiosity. I don't come to campus often anymore so it's not like I'm going to spend 8 hours a day
wasting the university's internet bandwidth for "Two and a half men" anyway...

**Another Note** (last one, promise!): If you're using Mac OS X or Windows, Proxifier will probably
do the trick way better and without any hassle. If you're using Linux or you simply want to learn
more about this stuff, read on!

## The problem

This semester the RMIT-WPA wifi network no longer requires manual proxy configuration (probably
because it makes Web Programming students miserable - they have to use Google App Engine), which is
good news. Nevertheless, that annoying domain filter is still up and running, meaning we still
can't go to certain blacklisted websites. (mediafire, fshare, gamevn, vnsharing, etc.)

Hdviet's case is a bit special: the domain `hdviet.com` itself is not blocked, but the domain of
the actual server hosting its videos, `v-01.vn-hd.com`, is. A quick look at Google Chrome's
excellent Network inspector confirmed that:

[img]

## Going for the IP

Naturally, I wanted to check if I could access the resource directly via the IP. An easy way to look
up a domain's IP is using [ping.eu][1]. Once you've got the IP, try replacing the domain with it in
the failed request:

[img]

This time it works, which means only the domain is blocked, not the IP.

One thing worth noting about hdviet: The video is not served as 1 single file, it is instead
chopped into multiple parts, which are loaded in order. Therefore, our first job is to
automatically replace `v-01.vn-hd.com` with the IP in all of the request.

## Twisted proxy

Since changing the request destination directly in the browser is probably difficult (I don't think
Google Chrome even allows that), we'll use an HTTP(S) proxy. This is when Twisted comes in handy.

[Twisted][2] is a battery-included framework to build robust network applications. By
"battery-included" they mean that most of the common functionalities have already been implemented
so we can use them out of the box. For the purpose of this tutorial, we are only interested in its
HTTP proxy library.

To install twisted, use `pip`:

    :::bash
    sudo pip install twisted

Since the default implementation doesn't support HTTPS, we'll use a [powered-up one][4] I found on
GitHub, written by Peter Ruibal. Let's clone this thing:

    :::bash
    git clone https://github.com/fmoo/twisted-connect-proxy.git

Now let's try running the proxy server: `cd` into the cloned directory and run it with `python2`:

    :::bash
    cd twisted-connect-proxy
    python2 server.py 8080

Then configure your browser to use **localhost:8080** as the proxy. For Firefox it's easy:

[img]

You should now be able to surf the web through the running proxy. But hey, you still can't visit
any blocked site! Of course you can't, since we haven't replaced the domains with IPs. Let's do
that.

## Domain to IP


[1]: http://ping.eu
[2]: https://twistedmatrix.com/
[3]: https://github.com/fmoo/twisted-connect-proxy
[4]: https://github.com/nhanb/twisted-connect-proxy
