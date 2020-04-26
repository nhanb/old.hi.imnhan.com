Title: Towards an acceptable video playing experience
Date: 2020-04-26 10:06
Category: side projects

I watch movies and TV shows.
Naturally, I have some strong preferences on how to view them:

**English subtitles**. Most things I watch are in English.
Although I'm perfectly comfortable with face-to-face English conversations, I
just can't keep up with English dialogue in movies.
I also don't want to put up with badly translated subs, so English subtitles
they must be. This rules out most Vietnamese "netflixes".

**1080p**, unless it's ancient or super rare stuff.

**Streamable from tablets**. I shouldn't need to turn on my PC just to catch up
on the latest Better Call Saul episode.

In 2020, there sure are a variety of options available, all of which fall short
in some ways:

- Shady ad-infested Vietnamese movie streaming sites (phimmoi etc): Obnoxious
  pop-up tabs aside, they always [abuse Google Drive][1] (or even Facebook?)
  storage behind the scene. Problem is Google Drive encoding is lossy as hell,
  so even at 1080p they look noticeably worse than the original. Also they
  almost always come with hardcoded Vietnamese subs.

- Netflix clones by big ISPs: Pathetic catalogues. Vietnamese subs.

- Netflix itself: Actually quite good thanks to usable Android app, but besides
  the increasingly shitty catalogue, it's [impossible to get 1080p from
  Linux][2]. Also I hate that I can't manually set the video quality: even if
  my current connection gets slow I'd rather pause and wait for buffering
  instead of putting up with a pixelated 480p mess. I still have my Netflix
  subscription today, but only grudgingly.

- "dude, like, just torrent it". Solid advice since torrents usually come with
  embedded English sub, but it requires actually downloading the thing first,
  and can't easily switch devices without moving the file along.

- Setting up a torrent + plex server? That would require (1) ample disk space,
  (2) generous network bandwidth, (3) actual horsepower for transcoding and (4)
  fast enough network access from home or wherever I watch movies from.

    - A local NAS-style server satisfies (1), (3) & (4) but struggles with (2),
      and I don't want it to hog my home internet pipes.

    - Finding a VPS service with (1) & (2) is doable, but (3) gets expensive
      fast and usually they're in the US or EU which can never have (4). I'm
      actually running a seedbox on Ramnode but can't run plex on it because of
      lack of (3) and (4). If I'm willing to pay more I can get a Hetzner
      dedicated server which can probably do (3) but (4) gets even worse.


## Remote seedbox + Google Drive

I settled on Netflix and torrented stuff that's not available there.
For the seedbox, I installed Transmission-web on a Ramnode VPS that has 320GB
of HDD at $50/year. The network bandwidth is meh but it gets the job done.

Since Transmission supports hooks via external scripts, I set it up so that
downloaded torrents get uploaded to my Google Drive using `rclone`.

Now whenever I find something interesting that's not on Netflix, I look for a
working torrent file and tell my seedbox to get it. Thanks to the web interface
I can do it from both my PC and tablet. I don't have to keep my devices running
so it doesn't matter if the torrent is not well-seeded and takes a long time.

Once the file lands on Google Drive, I can either:

- watch it directly from GDrive's web/Android app if I don't care about
  subtitles or original quality, or

- download the file first and watch properly

The latter is not ideal.


## Enter gflick

Turns out advanced video players like `mpv` and `vlc` can directly stream HTTP
videos with full support for seeking and audio / text(a.k.a subtitles) tracks.
See, well-formed video container formats will have metadata at the beginning of
the file telling where each track lies within the file. The player can download
just the metadata first, then the subtitle track, then the actual video track
starting from a specific position. This is only possible if the http server
supports partial content download [via the `Range` header][3].

Google Drive does have a "direct link" API in the form of
`https://www.googleapis.com/drive/v3/files/<fileId>?alt=media`, which luckily
supports partial download. The bad news is downloading private files requires
authentication via a bearer token. The only HTTP authentication scheme that
these players support, as far as I know, is [Basic auth][4].

So I wrote [gflick][5], which is practically an HTTP proxy that does Google
authentication behind the scene, exposing a plain HTTP streaming endpoint so
`mpv` and the like can use without modification.

Here's what it looks like in action:

<video controls>
  <source src="https://junk.imnhan.com/gflick.mp4" type="video/mp4">
</video>

It can run just fine as a local server, but cumbersome and not practical on
tablets, so I put it on a publicly accessible server, protected by nginx which
does TLS and Basic Auth. As mentioned earlier, good video players can do basic
auth out of the box. Gflick also exposes a simple web interface to browse my
Google Drives, so now I can browse my drive on any pc/tablet, and watch things
with full seek, subtitle/audio track support, right?

Not quite. While desktop versions of these players work fine, their Android
versions won't play it. Now I regret selling my Surface Go! :(

And... that's where I'm stuck at the moment. Not sure if I should buy one of
those Chinese Surface knock-offs or what.


## Other failed attempts

- [mpv-gdrive][6]: Using mpv's lua scripting API to automatically set the
  correct bearer auth headers. Worked fine on desktop, failed miserably on
  android.
- [drivein][7]: Uses `rclone mount`. Worked fine on desktop, android wouldn't
  allow mounting without root.

Also both of those required setting up each client device. Not ideal.

[1]: https://kipalog.com/posts/Cac-web-phim-da-giam-99-99--chi-phi-bang-google-drive-nhu-the-nao
[2]: https://help.netflix.com/en/node/23742
[3]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Range
[4]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication#Basic_authentication_scheme
[5]: https://github.com/nhanb/gflick
[6]: https://github.com/nhanb/mpv-gdrive
[7]: https://github.com/nhanb/drivein
