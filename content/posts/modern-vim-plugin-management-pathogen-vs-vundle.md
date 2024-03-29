date: 2013-05-13 12:00
title: Modern vim plugin management: Pathogen vs Vundle
slug: modern-vim-plugin-management-pathogen-vs-vundle
lang: en
category: tutorials
tags: vim
summary: Pimp your vim with little effort.


For the impatient ones: Vundle is better than pathogen, use it.

This post will explain how vim plugins work and how to easily manage your plugins with
third-party tools: Pathogen or Vundle. I assume you are using a Linux distro and have git
already installed. If not, consult Dr. Google for more details.

## Vim plugins anatomy

A vim plugin is simply a set of files that alter vim's behavior or add new functionalities to it.
To make this possible, by default vim looks for files in your home folder (which is 
`/home/username` or `~`):

## ~/.vimrc (file)

This is where you put your personalizations to vim: indentations, keybindings, etc. This post
will not discuss in detail how you do your customizations. For now just know that it's there.

You will probably want to move this file into your ~/.vim folder to be able to manage everything
inside 1 folder. I will create `~/.vim/vimrc` then create a symlink pointing to it. Open a
terminal and type:

    :::bash
    ln -s ~/.vim/vimrc ~/.vimrc

## ~/.vim (directory)

This should contain a bunch of subdirectories. Some examples:

- autoload
- ftplugin
- colors
- syntax
- doc

Each of these directories serves a particular purpose: `colors` contains colorschemes, `syntax`
lets you add new rules for syntax highlighting, `doc` contains documentation...  
A plugin will typically put its files into more than one directory here. For example, here is
a plugin called [tagbar](https://github.com/majutsushi/tagbar), and I've installed it by
copying its content into my `~/.vim` folder:

    :::bash
    ~/.vim
    ├── autoload
    │   └── tagbar.vim
    ├── doc
    │   ├── tagbar.txt
    │   └── tags
    ├── plugin
    │   └── tagbar.vim
    ├── README
    └── syntax
        └── tagbar.vim

Everything looks good. Just copy and paste the whole thing, nice and simple. How about adding a
decent colorscheme? Let's install [solarized](https://github.com/altercation/vim-colors-solarized):

    :::bash
    ├── autoload
    │   └── togglebg.vim
    ├── bitmaps
    │   └── togglebg.png
    ├── colors
    │   └── solarized.vim
    ├── doc
    │   ├── solarized.txt
    │   └── tags
    └── README.mkd

Wait, `doc/tags` is already there. Ok, no problem! Let's just copy the content of solarized's
tags file and paste it into the existing one. Now we have:

    :::bash
    ~/.vim
    ├── autoload
    │   ├── tagbar.vim
    │   └── togglebg.vim
    ├── bitmaps
    │   └── togglebg.png
    ├── colors
    │   └── solarized.vim
    ├── doc
    │   ├── solarized.txt
    │   ├── tagbar.txt
    │   └── tags
    ├── plugin
    │   └── tagbar.vim
    ├── README
    ├── README.mkd
    └── syntax
        └── tagbar.vim

Now what if you you decide that solarized sucks and want to get rid of it? Good luck finding
which file belongs to which plugin. Oh, don't forget the merged `doc/tags` file!
Now imagine you have 20-30 plugins installed (which is normal, by the way). It's not a
pretty sight now, is it?

## Pathogen to the rescue!

The legendary Tim Pope came up with a genius solution:
[pathogen](https://github.com/tpope/vim-pathogen).
Now let's install it like any regular plugin (I've omitted the README):

    :::bash
    ~/.vim
    └── autoload
        └── pathogen.vim

Put this at the beginning of your `~/.vimrc`:

    :::vim
    execute pathogen#infect()

Create this directory: `~/.vim/bundle`. To install tagbar and solarized, just create their own
directories here:

    :::bash
    path
    ├── autoload
    │   └── pathogen.vim
    └── bundle
        ├── tagbar
        │   ├── autoload
        │   │   └── tagbar.vim
        │   ├── doc
        │   │   ├── tagbar.txt
        │   │   └── tags
        │   ├── plugin
        │   │   └── tagbar.vim
        │   ├── README
        │   └── syntax
        │       └── tagbar.vim
        └── vim-colors-solarized
            ├── autoload
            │   └── togglebg.vim
            ├── bitmaps
            │   └── togglebg.png
            ├── colors
            │   └── solarized.vim
            ├── doc
            │   ├── solarized.txt
            │   └── tags
            └── README.mkd

What Pathogen does is that it adds every directory inside `bundle` into vim's "runtimepath".
It means that each folder here can be considered a new `.vim` folder where vim looks for
appropriate configuration files. The plugins are now isolated so removing or updating them
becomes trivial: just remove or update its own directory.

## Pathogen + Git

Everything goes to the cloud these days, and certainly your vim setup should as well. If you
haven't created a [Github](https://github.com) account, do it now. Create an empty repository
with any name you want (mine is `.vim`). Don't commit yet. Create a file: `~/.vim/.gitignore`,
add these lines to its content:

    :::bash
    bundle/
    .netrwhist

.netrwhist is a local file generated by vim that is better off ignored. We also ignore bundle
directory because the plugins will be included as git submodules (google *git submodule*
for details). Remember to delete everything inside `bundle/`, because we will install the
plugins again with git.

Git init, commit and push to your github repo: (on the *git remote add...* line, replace `nhanb`
with your github username, `.vim` with your repo name)

    :::bash
    cd ~/.vim
    git init
    git add .
    git commit -m 'init'

    git remote add origin https://github.com/nhanb/.vim.git
    git push -u origin master

Everytime you edit anything in your .vim directory, remember to commit the changes and push to
github:

    :::bash
    git add . 
    git commit -m 'some message here'
    git push

If you want to install a plugin, see if it has a git repo (9 out of 10 times it has a
github repo). Find its git url and add to your .vim as a submodule:

    :::bash
    cd ~/.vim
    git add submodule https://github.com/majutsushi/tagbar.git bundle/tagbar
    git add submodule https://github.com/altercation/vim-colors-solarized.git bundle/solarized
    git submodule update --init
    git submodule foreach git pull origin master

When you need to update your plugins, just run the last line to make git pull updates for all
plugins. 

Here's the awesome part: when you're using a whole new computer and want to get all your vim settings
from the cloud, simply clone your github repo, make a symlink for .vimrc and pull all plugins:

    :::bash
    cd ~
    git clone https://github.com/nhanb/.vim.git .vim
    ln -s ~/.vim/vimrc ~/.vimrc
    cd .vim
    git submodule update --init && git submodule foreach git pull origin master

Now you must be really excited, no? Git does everything for you: upload/download, add plugins,
update plugins *and* remove plugins... There must be some simple git command to remove a
submodule, right?

**NO**. Sadly, no. To remove a git submodule, you'll need to manually edit 2 git files and
remove the folder by hand. See
[this Stackoverflow question](http://stackoverflow.com/questions/1260748/how-do-i-remove-a-git-submodule)
for detailed instructions.

## Vundle, the new cool kid

This time let's start fresh: remove all submodules and pathogen. Your bundle folder should be
now empty. Clone [Vundle](https://github.com/gmarik/vundle):

    :::bash
    git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle

Put this in your .vimrc (preferably at the beginning):

    :::vim
    set nocompatible               " be iMproved
    filetype off                   " required!

    set rtp+=~/.vim/bundle/vundle/
    call vundle#rc()

    " let Vundle manage Vundle
    " required! 
    Bundle 'gmarik/vundle'

    " My Bundles here:
    "
    " original repos on github
    Bundle 'majutsushi/tagbar'
    Bundle 'altercation/vim-colors-solarized'

    " Github repos of the user 'vim-scripts'
    " => can omit the username part
    Bundle 'L9'
    Bundle 'FuzzyFinder'

    " non github repos
    Bundle 'git://git.wincent.com/command-t.git'
    " ...

    filetype plugin indent on     " required!

Relaunch vim, run `:BundleInstall` to install the "bundles" you listed in .vimrc. When you want
to update them, `:BundleUpdate`. To remove a plugin, just delete its line in your .vimrc file
then relaunch vim and run `:BundleClean` to remove its folder inside ~/.vim/bundle/

Vundle follows Pathogen's approach: putting plugins in their separate directories. However,
it also takes care of the git stuff for us too! Note that by default it uses `git clone`, not
`git add submodule` to add plugins. If you're using Windows, there's Vundle for Windows too,
though I've never tried it.

That's it, happy coding! Feel free to leave your comments if there's anything wrong/unclear here.
