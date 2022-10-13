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

- [conv-to-mp3](utils/conv-to-mp3): find all music files and convert them to
  mp3 (if needed, with FFmpeg), preserving the file tree.
- [gifenc](utils/gifenc): encode a video to a GIF file using FFmpeg and the
  palette mechanism, supports fps, scale and a few other flags
- [kcheck](utils/kcheck): check if the current running kernel is matching the
  installed package (Archlinux only) in order to see if I need a reboot
- [mtp_mount](utils/mtp_mount): auto mount all MTP devices using GIO command
  line tool
- [mtp_umount](utils/mtp_umount): auto umount all MTP devices using GIO command
  line tool
- [pytunes](utils/pytunes): connect to MPD, scp all files from the playlist
  locally, and eventually convert them to the specified audio format
- [record](utils/record): capture a selection (window or free-form) or the full
  screen and reencode it into a web-shareable file, using FFmpeg; X11 only
- [temp](utils/temp): convert temperatures (args or stdin) between °C and °F
- [hex](utils/hex): convert hex strings to their ASCII/binary representation
  (works with spaces)


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
