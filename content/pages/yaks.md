Title: Yak shaving
Slug: yaks
Hidden: True


Basically my TODOs, in pursuit of the ever-pervasive _pleasant workflow_.

## Replacing tmux with kitty

All blockers seem to have been addressed now?

- [tmuxp replacement](https://sw.kovidgoyal.net/kitty/index.html#startup-sessions)
- [seamless navigation alongside vimsplit](https://github.com/knubie/vim-kitty-navigator)


## Interesting tools

- [pyinfra](https://pointlessramblings.com/posts/why-you-should-try-pyinfra/):
    + faster than ansible, from my anecdotal experience
    + python, not yaml
    + truly agentless (doesn't even require python)

- [doit](https://pydoit.org/): I just want a cross-platform `make`.


## Home server

Specs:

- Thinkpad T430 whose screen just broke
- Accessible via Tailscale
- Debian 10 installed on main SSD
- 2x1TB Seagate HDDs, LUKS encrypted, running a RAID1 btrfs pool.

Services:

- [x] Syncthing
- [] Some RSS reader
- [] Some bookmarking system that does full text search.
