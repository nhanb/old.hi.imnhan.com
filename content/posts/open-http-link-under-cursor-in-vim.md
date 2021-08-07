Title: Opening http link under the cursor in vim
Date: 2021-08-07 11:37

Internet's wise old chatty uncle [Walter Bright](https://www.walterbright.com/)
recently [commented](https://news.ycombinator.com/item?id=28090272) on Hacker
News:

> [...]
>
> Ever since the Intel CPU spec went online, I started doing this with the code
> generator - providing links to the man page for the instruction being used:
>
> <https://github.com/dlang/dmd/blob/master/src/dmd/cparse.d#L591>
>
> And for bug fixes, reference the issue which often gives a detailed
> explanation for why the code is a certain way:
>
> <https://github.com/dlang/dmd/blob/master/src/dmd/backend/cgxmm.d#L1210>
>
> Ever since I enhanced the editor I use to open the browser on links, this
> sort of thing has proven to be very, very handy.

I've never had any issue with opening links from vim: I have `<leader>y` set up
in Visual mode to yank stuff into the system-wide clipboard which I can then
paste into the browser. However, ever since I mapped `<leader>gh` to trigger
[`:GBrowse`][1] that opens a browser tab instantly, the old "select > copy >
switch to browser > Ctrl+T > Ctrl+V" flow started to feel... prehistoric. Mr.
Bright's comment gave me the final nudge to actually go ahead and set it up.

The good folks from the [developer encyclopedia][3] suggested `gx` but for some
reason, setting `g:netrw_browsex_viewer` [didn't seem to do anything][4] so the
command would always `wget` the link then tell the browser to open that
downloaded file. Therefore, I cobbled together this snippet which was adapted
from those stackoverflow & github threads:

```vimscript
function! OpenURL()
  let l:url = matchstr(expand("<cWORD>"), 'https\=:\/\/[^ >,;()]*')
  if l:url != ""
    let l:url = shellescape(l:url, 1)
    let l:command = "!xdg-open ".l:url
    echo l:command
    silent exec l:command
  else
    echo "No URL found under cursor."
  endif
endfunction

nnoremap gl :call OpenURL()<cr>
```

_(if you're on a Mac, replacing `xdg-open` with `open` will probably
do the same thing)_

Now whenever I have my cursor on an http(s) url, I can type `gl` from normal
mode and xdg-open will use my default browser to open it up. This could be
extended to any other scheme like `mailto` or `ftp` but I don't have any
practical use for them right now so that will do.

One drawback is if there's a whitespace in the URL (which is bad practice
anyway), my regex won't match the whole thing. In such cases I'd rather resort
to good old manual visual mode than try to be clever and make my URL detecting
logic exponentially more complex. I'd take simple software with obvious, easily
understood behavior over overcomplicated, (possibly) subtly broken balls of mud
any day.

By the way, if you looked at my script and got spooked by the idea of executing
a shell command composed from arbitrary, potentially unsafe input (i.e. text
file content), don't worry: that's what [`shellescape()`][2] is for.

[1]: https://github.com/tpope/vim-fugitive/blob/2dc08dfe354ed5400f5cdb3d5009dcd4024aac8a/doc/fugitive.txt#L213
[2]: https://learnvimscriptthehardway.stevelosh.com/chapters/32.html#escaping-shell-command-arguments
[3]: https://stackoverflow.com/questions/9458294/open-url-under-cursor-in-vim-with-browser
[4]: https://github.com/vim/vim/issues/4738
