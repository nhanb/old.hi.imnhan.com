Title: "Have you built anything cool?"
Slug: have-you-built-anything-cool
Date: 2013-12-04 08:55:44
Status: draft

So yesterday I went to a *networking event* - something I have never liked or been good at. I'm
not sure if I'm one of those introverts or if I'm just socially awkward, but the very idea of
going around trying to converse with total strangers just to exchange business cards is not at all
appealing to me. Anyway, that's another story. Right now I want to write about something a guy
from a non-tech company asked me:

> \- Have you built anything cool?  
> \- [pause] Well, more or less...  
> \- What do you mean by "more or less"? [...] Have you built anything at all?  

Then I went on trying to explain what my recent side project - 
[pytaku](https://pytaku.appspot.com) - does and why it is awesome for me. He seemed to be
disinterested halfway through so I decided to shut up anyway.

Sure, I have done stuff every now and then, be it assignment work or something I decided to create
for my own amusement. It is just funny how I have already stepped into to my final year without
taking a proper look back at what I have done in these past 2 years, so I'm going to do just that.

If you - Nicholas - are reading this and don't want all the nerdy stuff, here are my condensed
answers:

### Have you built anything?  
Yes, I have done desktop and Android games, a movie ticket sales program, a desktop manga
grabber, a web version of it that talks to dropbox, and several small shell scripts / web
utilities.  

### So, nothing cool?  
If you're neither a tech geek nor an otaku (which I assume you're probably not) then no,
there's probably nothing I've done that you would find interesting.

## First year - Welcome to the web, and the GUI programming disillusionment

I had touched *web stuff* before in high school: a vBulletin forum that I created (unofficially)
for students in my middle school. However, I only properly learned PHP and JS when I started the
Web Programming course here. With (moderately) great power came great desires, so I set out to
build a basic PHP site to scrape a view page's HTML to get direct video links (not working anymore
since a recent youtube update)

![tubegrab v2.9](/images/tubegrab.jpg "tubegrab v2.9")

That was my first touch on jQueryUI and regular expressions; I also learned how RMIT's mekong
server sucked to the point that it didn't allow `get_file_contents()`.

About school assignments? Nothing interesting: standard barebones LAMP CMS with jQuery glitter
sprinkled on top. Not a bad experience but meh.

I also learned about MVC and GUI programming with Java swing. I did write a movie ticket program
with a (pretty minimal) seat picker and
[a battleship-inspired game](https://github.com/nhanb/sealord): 

![Cinema Movie Picker](/images/cinema_1.png "Cinema Movie Picker")
![Seat Picker](/images/cinema_2.png "Seat Picker")
![Sealord](/images/sealord.png)

Then it occurred to me that programming GUI interfaces for desktop programs is much more tedius
than doing it for the web, especially when working with the now-not-favored Swing toolkit.
Nightmarish days...

Another lession learned the hard way was that "MVC" is not even a concrete thing, and there is
hardly any obvious "one true way" to implement that. I spent much more time planning for plumbing
code than I the time I spent actually writing "feature" code. And the result, now looking back, was
not even that good. And yeah, there was no such thing as "separation of concerns" in my code back
then, which eventually led to countless times of tracing obscure stack traces for debugging (good
thing I had a lot of free time back then).

To rub salt in the wound, I came to realize that nobody cared how Swing looked on any desktop
environment other than OS X and Windows. Font rendering was painful to look at, and the only way to
make it *a little bit* more acceptable was using a
[forked version of OpenJDK](http://www.webupd8.org/2013/06/install-openjdk-patched-with-font-fixes.html).
WTF guys? And that's not the only problem; let's talk Look And Feel. The built-in
getSystemLookAndFeel() could only detect GNOME's. When developing `ajmg` I discovered that and had
to wrote my own method that extended the thing to detect more DEs, but soon after that I thought
"What the hell, why do I even have to do this?" and decided that Swing was dead to me (or any
desktop Linux user for that matter).
