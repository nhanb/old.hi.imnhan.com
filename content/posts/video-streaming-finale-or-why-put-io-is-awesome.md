Title: The video streaming finale, or why put.io is awesome
Date: 2020-10-21 11:45


[Previously](/posts/streaming-videos-from-google-drive-a-second-attempt/),
[previously](/posts/towards-an-acceptable-video-playing-experience/).


I ditched the whole self hosted mess and just bought a [put.io](https://put.io)
subscription instead. This has become the smoothest, most no-nonsense video
streaming experience I've ever had.

It's a seedbox.

It transcodes.

It streams.

It has a web-based video player that lets me pick subtitles.

In cases when the subtitles aren't recognized, or when I want to switch between
audio tracks, I can always drag-n-drop the original file's streaming URL from
the browser straight to an mpv launcher like this:

<video controls>
  <source src="/images/put.io_01_mpv.mp4" type="video/mp4">
  <a href="/images/put.io_01_mpv.mp4">Video: /images/put.io_01_mpv.mp4</a>
</video>


It also has a open source third-party [Android app][1] that lets me browse and
stream via mpv-android. As icing on the cake, this app supports casting to
Chromecast-enabled TVs - everything Just Works (tm).

The above is only possible because put.io exposes a powerful, well-documented
API for everyone to play with.

The web player is clean, snappy (see that, Google Drive team?) and has
autoplay disabled by default (screw you, Netflix).

It's refreshing to find software that works _for_ instead of _against_ its
users these days.

[1]: https://github.com/DSteve595/Put.io
