# Promo assets — epsteinexposed

Silent, captioned promo video for **epsteinexposed**, part of the shared
[Epstein Files toolchain](../README.md#the-toolchain) asset set.

| File | Dimensions | Use |
|---|---|---|
| `exposed-16x9.mp4` | 1920×1080 | YouTube, docs sites, embeds, Hacker News |
| `exposed-1x1.mp4` | 1080×1080 | Twitter and Reddit — the default for social |
| `exposed-poster.png` | 1920×1080 | README embeds, link previews, PyPI |

Both clips run 19.6s, H.264 / yuv420p, silent with burned-in text, so they
autoplay correctly in muted timelines.

## Regenerating

These are rendered from animated HTML captured frame-by-frame through
Chromium and encoded with ffmpeg, so output is deterministic. The renderer
lives in the Explorer repo, which holds the master asset set:

```bash
git clone https://github.com/guilyx/epsteinexplorer
cd epsteinexplorer/promo
npm install
npm run render          # all four tools, both crops
```

Copy `out/exposed-*` back here afterwards.

Visual language and palette: [`brand/DESIGN.md`](../brand/DESIGN.md).
Channel-by-channel launch plan: [`LAUNCH.md`](https://github.com/guilyx/epsteinexplorer/blob/main/LAUNCH.md).

## A note on content

No promo asset names any individual, and no redaction effect is applied over
real records. Inclusion in these files is not an accusation — see
`brand/DESIGN.md` § Ethical constraints.
