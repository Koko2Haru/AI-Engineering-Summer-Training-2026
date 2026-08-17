# Rafid — brand assets

| File | Use |
|---|---|
| `icon.svg` | source mark, square |
| `icon.png` | 512×512 — **Discord bot avatar** |
| `icon-1024.png` | 1024×1024 — anywhere needing a bigger icon |
| `banner.svg` | 680×240 — **Discord application banner** |
| `logo.svg` | horizontal lockup, transparent, navy text — for **light** backgrounds |
| `logo-white.svg` | same lockup, white text — for **dark** backgrounds |

## The mark

رافد is one who supports, and shows the way. The mark is a hand pointing
converge and leave as one gold channel that rises.

## Colours

| | Hex | Where |
|---|---|---|
| Navy | `#1F3864` | background, wordmark. Same navy the generated PDFs use |
| Mid blue | `#5B79AB` | the tributaries |
| Light blue | `#7E9AC8` | outer tributaries |
| Gold | `#F0B429` | the channel, the rise, Arabic wordmark |
| Muted | `#9DB3D4` | secondary text |

The navy matches `md2pdf.py`'s heading colour, so the brand and the documents
Rafid produces are the same palette.

## Exporting the banner to PNG

`banner.svg` contains Arabic text, which most command-line SVG converters render
unjoined or reversed because they have no text-shaping engine. Browsers get it
right.

To export: open `banner.svg` in Chrome or Edge, zoom to 100%, and screenshot the
680×240 area. Or use an online SVG→PNG converter, then check the Arabic renders
as **رافد** and not as disconnected letters.

`icon.png` has no text, so it converts cleanly anywhere.
