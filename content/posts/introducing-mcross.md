Title: Introducing McRoss—a minimal gemini browser
Date: 2020-05-29 09:44
Category: side projects


The last couple of months saw the first "PR" wave of [the gemini protocol][1]
on the usual online [tech][2][(bro)][3] forums. Its pitch is simple: the web
has gone out of hand, gopher is too barebones and insecure by default, here's a
new thing that sits in the middle.

Personally I'm skeptical if this thing will take off any time soon (or ever).
Sure I agree the web is [comically bloated][4], [openly user-hostile][5], and
the big players are only [adding to the problem][7], but the fact remains that
the web is the most convenient thing there is, both from a user's and
developer's perspective. Gemini is a fun experiment. It may even be a hit among
<strike>nerds</strike> power users and the overly privacy-concious, but that's
it.

But then again, I consider myself among the "<strike>nerds</strike> power users
and the overly privacy-concious" demographic, so I naturally want to see what
cool stuff people on the gemini-verse are up to. Therefore, I need a gemini
browser. _Naturally_, I [wrote one][12]:

![McRoss Browser screenshot](/images/mcross_01_screenshot.png)

At this stage it can browse plaintext and gemini content, but not binary yet.
It also doesn't verify TLS certificates, because turns out [in the gemini
world][11] it's preferable for browser to use self-signed certs and expect
clients to trust on first use (TOFU), just like how basic SSH works. I haven't
implemented TOFU yet so the browser trusts whatever and is vulnerable to MITM
attacks for every request. It's highly unlikely that anyone would bother to,
but take everything you read with a pinch of salt anyway.

Why not use one of the existing browsers you ask? Sure enough there are a bunch
of existing browsers, with [Castor][8] appearing to be the furthest along in
development, but it didn't work _quite_ the way I would like. This made me want
to find out for myself just how hard it is to build a reasonably user-friendly
desktop GUI application. For the rest of this blog post I try to elaborate on
my idea of a _user-friendly desktop GUI application_.

### Visual feedback:

When I click a button, visit a link, or press Enter on the address bar, I
expect some kind of visual feedback that tells me my input registered
correctly, and the browser is working on my request, not hanging. This sounds
ridiculously elementary considering that's how, say, all Windows 95 programs
worked, but here we are two decades and a half later and the Castor browser
just completely freezes the GUI during every network request.

With McRoss I intentionally put the GUI and I/O event loops in their separate
threads to make sure the program's always responsive. I also paid attention to
small details like the loading cursor and real-time status bar. At no point
should the program hang or crash without displaying a proper message.

### Aesthetics:

Call me picky but I don't like how in Castor links are presented as buttons and
they don't even have breathing room between them:

![Castor links](/images/mcross_02_castor.png)

Another admittedly petty issue I have is that it's GTK while I'm using KDE
Plasma, and although KDE has a compatibility layer that tries to render GTK
widgets as close to KDE counterparts as possible, the result is still...
subpar.

McRoss on the other hand uses the tk gui toolkit, and as of tk 8.6, it
automatically gives you the native look and feel on Windows and Mac OS (well,
not automatically but it takes trivial work anyway). Linux however doesn't have
such a thing, but the bundled `clam` theme looks pleasing enough for me. Yes, I
do think a retro looking theme fares better than the gtk-on-kde look, and its
simple scrollbar looks and, more importantly, _works_ way better than those
nigh-unclickable abominations that KDE and GTK call their "modern scrollbar",
fight me.

Another explicit design decision in McRoss is that while custom styling is
applied to special lines (heading, list, code block...), their textual content
is kept the same as source, with the special characters (`#`, `*`, etc.)
intact. This way when someone has read a gemini page, they already know how to
write one. I lifted this idea off of [imageboards][9] and [textboards][10].

### Installation:

Castor is written in Rust. One of Rust's strong points is the ability to
compile to a single statically linked executable that users can just download
and run. Unfortunately, Castor doesn't currently provide those compiled
executables so users are supposed to install the Rust toolchain then build
Castor themselves. Compiling a gtk-enabled Rust project is... not a quick
affair.

McRoss is currently packaged as a well-behaved PyPI package and can be
installed with `pip3 install mcross`. Its only dependencies are the standard
library and `curio` so installation should be super fast. I know I know,
requiring python in the first place is its own can of worms. I do plan to
improve the situation with "frozen" executables some time down the line.

# Closing thoughts

To me the whole gemini ecosystem represents the long-lost naive optimism of an
earlier web ecosystem. It was not even as far as the "good old
gopher/bbs days" those boomers keep ranting about - it was the days of early
MMORPGs, of crappy Yahoo! 360 blogs riced up with copy-pasted html/css all over
the place, of numerous Vietnamese warez forums powered by pirated vBulletin
running on shady free shared CPanel hosts, of monthly Drupal/Joomla SQL
injection zero-days. It was truly the wild wild web, insanely accessible,
insanely unsafe, and insanely fun. It was the web where a young clueless
teenage me could find fun random stuff everyday, put fun random stuff out
there for everyone to see, no matter how shitty and unsecure they are, because
it didn't matter if I get pwn'd: my life back then wasn't that much dependent
on the web.

Can I get all that back? I think not. The web, or more broadly, the internet
grew up (to be a nasty adult, but an adult nevertheless), just like anything
where there's enough profit to be made. I'm not saying it's a bad thing (hell,
I make a living out of building webstuff), but it is undeniably a sad thing.
Gemini may be a spark that begins a push back against unjustified complexity,
or it may end up being just another niche tech curiosity. I'm leaning towards
the latter, but in the meantime, I'll keep peeking at the geminiverse with my
comfy trusty browser.

[1]: https://gemini.circumlunar.space/
[2]: https://lobste.rs/s/79pu7o/gemini_protocol_inbetween_gopher_web
[3]: https://news.ycombinator.com/item?id=23042424
[4]: https://idlewords.com/talks/website_obesity.htm
[5]: https://neustadt.fr/essays/against-a-user-hostile-web/
[6]: https://www.theverge.com/2019/11/20/20974832/facebook-google-surveillance-data-assault-privacy-amnesty-international
[7]: https://developers.google.com/amp
[8]: https://sr.ht/~julienxx/Castor/
[9]: https://4chan.org/
[10]: https://textboard.org/
[11]: https://todo.sr.ht/~nhanb/mcross/1
[12]: https://sr.ht/~nhanb/mcross/
