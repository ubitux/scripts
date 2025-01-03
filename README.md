# ubitux scripts

This repository contains a bunch of more or less useful helper scripts that I
either use regularly, or used punctually in the past. I actually have many
other but they unfortunately contain personal settings I'm not willing to
share.

I may accept PR for fixes, but can't promise review for large or intrusive PR,
these scripts remain pretty personalized.

The overall quality of the scripts is not always great, use them at your own
risk.


## Daily scripts (utils directory)

These scripts are deployed using [install-utils](install-utils), which relies
on `stow`.

- [acc_add_mail_alias](utils/acc_add_mail_alias): create a mail alias; this is
  generally called after `acc_new`
    + depends on the [config](#Config), an OpenSMTPD setup, and a local
      repository with a copy of the SMTPD aliases
- [acc_new](utils/acc_new): provide two commands (`acc_add_mail_alias` and
  `acc_register`) to help creating a new account on a random
  website/service/whatever (sometimes only the mail is necessary, sometimes
  only login/password pair, hence the split). The space printed before the
  command are actually useful not to have them registered in the shell history
- [acc_register](utils/acc_register): register an account and its password in
  a `pass` keychain
    + depends on the [config](#Config), the `kp` setup
- [android_files](utils/android_files): mount the Android device and open file
  browser on its mount point
    + depends on the [config](#Config) and `mtp_mount`
- [android_send_pic](utils/android_send_pic): upload a picture to the Android
  device
- [android_send_vid](utils/android_send_vid): upload a video to the Android
  device
- [android_sync_dcim](utils/android_sync_dcim): mount the Android device, copy
  its `DCIM` directory locally, and remove them from the device
    + depends on the [config](#Config) and `mtp_mount`
- [android_sync_quicknotes](utils/android_sync_quicknotes): mount the Android
  device, and append the "quick notes" into the local notes scratchpad, then
  delete the file from the device
    + depends on the [config](#Config) and `mtp_mount`
- [arec](utils/arec): record an opus file from the mic input (made for Anki
  because the flatpak recording doesn't work for some reason)
- [backup](utils/backup): interrogate one backup (wrapper on top of `restic`)
    + depends on the [config](#Config), the `kp` setup, a restic server, and
      probably more stuff I'm forgetting
- [backups](utils/backups): interrogate all backups (basically call `backup`
  for all the hosts identified in the `kp` database)
    + depends on the [config](#Config), `backup`, etc
    + typical command: `backups snapshots --latest 5 --compact`
- [bh](utils/bh): "bh" is a shorthand for "blackhole", basically a place to
  upload files and share them through http
    + depends on the [config](#Config)
- [bpaste](utils/bpaste): similar to `bh` but oriented for sharing text files /
  command outputs
    + depends on the [config](#Config)
    + used exclusively as a pipe (`ls -l | bpaste` or `bpaste my-great-file <
      my.file`: the optional argument is only here to tweak the URL a bit
- [c](utils/c): calendar integration with `remind` and my notes (`rem` specs is
  extracted from a markdown quote); it watches for changes on the file and
  reload the calendar view when it happens
- [conv-to-mp3](utils/conv-to-mp3): find all music files and convert them to
  mp3 (if needed, with FFmpeg), preserving the file tree.
- [gifenc](utils/gifenc): encode a video to a GIF file using FFmpeg and the
  palette mechanism, supports fps, scale and a few other flags
- [hex](utils/hex): convert hex strings to their ASCII/binary representation
  (works with spaces)
- [i3mvws](utils/i3mvws): move all the windows from one workspace to another
    + `i3mvws 7 2` will move all windows in workspace 7 to workspace 2
- [kcheck](utils/kcheck): check if the current running kernel is matching the
  installed package (Archlinux only) in order to see if I need a reboot
- [kp](utils/kp): key pass wrapper
    + depends on the [config](#Config)
    + requires a specific git repository with both `pass` db and `GnuPG` home
      directory
- [kpf](utils/kpf): on top of `kp` but with `fzf` for fuzzy finding an account
    + depends on the [config](#Config)
- [mtp_mount](utils/mtp_mount): auto mount all MTP devices using GIO command
  line tool (depends on `gvfs-mtp`)
- [mtp_umount](utils/mtp_umount): auto umount all MTP devices using GIO command
  line tool (depends on `gvfs-mtp`)
- [music_clean_dir](utils/music_clean_dir): music from the Internet is usually
  polluted with various form of garbage, this script gets rid of it
- [newday](utils/newday): first thing I execute when I wake up; it creates a
  new entry in my `vimwiki` notes and prepare the daily commit in the git,
  which I update through the day until its last review before bed time.
    + depends on the [config](#Config)
- [notes_stats](utils/notes_stats): a bunch of stats of my notes
    + depends on the [config](#Config)
- [pytunes](utils/pytunes): connect to MPD, scp all files from the playlist
  locally, and eventually convert them to the specified audio format
- [record](utils/record): capture a selection (window or free-form) or the full
  screen and reencode it into a web-shareable file, using FFmpeg; X11 only
- [rgb2float](utils/rgb2float): convert `#RRGGBB` to `r,g,b` format where `r`,
  `g` and `b` are floats
- [rssfind](utils/rssfind): find RSS links given an URL, depends on `curl` and
  `htmlq`
- [shot](utils/shot): takes a screenshot using `shot` and uploads it
    + depends on the [config](#Config)
- [shotl](utils/shotl): takes a screenshot using `shotgun`. Supports delaying
  the screenshot `-d DELAY`, editing after the screenshot is taken (`-e`),
  picking a specific zone (`-s`) and an output file argument
    + depends on the [config](#Config), `shotgun`, `slop` (for selection) and
      `pwgen`
- [smux](utils/smux): connect to an host, start tmux if the target session is
  not up, and attach to it. I do have aliases such as `alias music='smux
  myserver music'` and `alias rss='smux myserver rss'` (same user/server,
  different sessions)
- [temp](utils/temp): convert temperatures (args or stdin) between °C and °F
- [term_switch_iosevka](utils/term_switch_iosevka): stupid script to switch
  alacritty to Iosevka font
- [term_switch_profont](utils/term_switch_profont): stupid script to switch
  alacritty to ProFont
- [urlencode](utils/urlencode): URL encode a string, used by some of the other
  scripts, and sometimes I also use it manually
- [weight_stats](utils/weight_stats): extract the weight stats from my notes
  and graph them with `gnuplot`

### Config

Some scripts depend on a config file. For those, the file [template config
file](utils/config.in) needs to be copied to a `config` file and adjusted
appropriately.


## Punctual scripts (oneshot directory)

- [axgen.py](oneshot/axgen.py): this is more a template than anything, it helps
  making an automatic grid of diagrams with matplotlib
- [best-pi.py](oneshot/best-pi.py): brute-force script to find the most
  retarded π approximation (spoiler: 22/7)
- [bezier-anim.py](oneshot/bezier-anim.py): script used to generate the
  deconstructed animated Bézier video in one of my [blog post][bezier]
- [simd-aarch64.py](oneshot/simd-aarch64.py): generates an SVG cheatsheet for a
  bunch of AArch64 SIMD instructions, can be [seen on Twitter][simd-aarch64]

[bezier]: http://blog.pkh.me/p/33-deconstructing-be%CC%81zier-curves.html
[simd-aarch64]: https://twitter.com/insouris/status/1580670107067432960


## Config
