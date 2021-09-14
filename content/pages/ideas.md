Title: Potential project ideas
Slug: ideas
Hidden: True

## Self hosted RSS reader in D

- Single executable, web based
- SQLite3
- Either use adamdruppe's rss.d or wrap libmrss
- Bonus: e-ink friendly display
- Bonus: netsurf friendly

## Desktop GUI blogging CMS using tkinter

- Native win/mac look-and-feel, acceptable on linux (`clam` looks alright)
- Split screen: one with markdown/bbcode source and one with rendered preview
- Sane embedded image/video/etc. file management via GUI
  + Bonus: 1-click preprocessing: strip EXIF, losslessly optimize image
- **No embedded browser**
- Is static site generator, but supports 1-click deployment to neocities,
  github/gitlab/sourcehut pages etc.
- Human-friend distribution e.g. nuitka, pyoxidizer (pyinstaller is pretty meh)
- Bonus: pluggable templates

## Manhoa

Still fuzzy. May want to ditch the familiar Django stack and try using vibe.d.
Who knows?
