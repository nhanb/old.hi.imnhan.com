Title: Why I use Linux: Automation
Date: 2013-06-07 08:02
Category: tutorials
Tags: python, linux
Slug: why-i-use-linux-automation
Summary: Repeating is for losers.

(In this post, when I say Linux, I mean any popular GNU/Linux distribution. Hope this clarification
will keep the nitpickers away.)

First let's discuss *why* automation rocks.

## Repetition is evil (and boring)

As a (would-be) software engineer, the *repetition is evil* notion has been planted in my head for
far more times than anything else, and for good reasons.

People are far more prone to error than computers, and doing repetitive tasks creates just too
much room for that. Computers, on the other hand, do everything exactly how you tell them to do,
with extreme speed and accuracy.

Moreover, let's face it: We developers are all (or at least mostly) lazy. Not the "I'm don't
wanna do anything" kind of lazy, but more of the "This crap is boring and not challenging at all,
why the hell am I wasting time for it?" type. We've all got better things to do with our lives,
like re-watching the last episode of BBC's *Sherlock* to look for clues to how he faked his death,
or trying to figure out what that "Han shot first" meme means (sorry, I'm from the later
generation).

## Automation needs command line tools

Because, of course, GUI programs are (nearly) impossible to interact with in our scripts. Sure
you can try mouse click emulation tools and stuff like that, but is it really worth the effort?
And I'd bet anything that those tools are far from reliable (GUI latency, anyone?).

And this is where Windows falls short. Most (if not all) Windows tools are designed for GUI, and
the whole Windows ecosystem is built around GUI use.

It's a whole different matter in Linux: from the good old awk, sed, grep, wget to the new shiny
aria2... Almost anything you can think of is available as a command line tool.

## Putting them all together

Just like any UNIX-like system, Linux tools utilize the One True Phylosophy: Do only 1 thing, and
do it well. (okay, I'm paraphrasing a bit, but you get the idea)

The true power of command line tools is when they are used together. Let's take a look at a
[python script](https://gist.github.com/nhanb/5726342) I wrote last night to download the whole
beginner course from [justinguitar](http://www.justinguitar.com).

The real flow starts from line 48:

    :::python
    # Fetch index pages which has links to all beginner lessons
    r = requests.get('http://www.justinguitar.com/en/BC-000-BeginnersCourse.php')
    start_page = r.text

    # Search for all links to lessons
    pat = re.compile('<a href="(BC-[0-9]{3}-.+?)"')
    pages = pat.findall(start_page)

    # Fetch html for each lesson
    pages_html = fetch_html(pages)

    # Crawl each lesson page, pull out lesson names and youtube link code
    youtube_codes = []
    for html in pages_html:
        code = parse_info(html)
        print code
        if code not in youtube_codes:
            youtube_codes.append(code)

To summarize, this snippet goes to justinguitar's beginner course index page, grab all links to
each lesson, then grab the lesson title as well as the youtube video code to its video. The
result is the list name `youtube_codes`; each element is a tuple with the format
`(title, youtube_code)`.

Then I use a command line tool called `youtube-dl` to fetch the direct link to each video. The
tool itself can download the video too, but it doesn't support multiple connections to
accelerate the download. This is where `aria2c` jumps in: it takes the direct link from
`youtube-dl` then download the whole thing:

    :::python
    # Leech the hell out of them
    for lesson in youtube_codes:

        # Ignore if lesson has no video
        if lesson[1] == None:
            call(['touch', lesson[0]])
            continue

        # Use youtube-dl to get fresh download link and file extension
        command = 'youtube-dl ' + lesson[1] +\
                ' --skip-download --get-url --get-filename -f 35/34/82/44/43/100'

        shell_output = str(check_output(command.split()))
        direct_link, fname = shell_output.splitlines()
        file_ext = fname[fname.rfind('.'):]
        file_name = lesson[0] + file_ext

        # Then aria2 for serious multi-part download acceleration
        print 'Downloading ' + file_name + '...'
        command = ['aria2c', "-o", file_name, '-x2',
                "%s" % direct_link]
        shell_output = check_output(command)
        print shell_output

That's it! I just needed to launch this script, turn off the laptop screen and go to bed. This
morning I woke up seeing the whole course with almost 100 lessons downloaded. Imagine having to
manually download all that by clicking each link... You don't wanna go there, do you?

So that's just a very simple example of what automation helps your every day life. Of course its
true power is unleashed when used in development; this is how one-click test and deployment
works. Windows can do this too, but your choice of tool will be limited. And don't get me started
on its lack of a decent package manager!

To make a long story short, do yourself a favor and install a Linux distro.

... or buy a Mac.
