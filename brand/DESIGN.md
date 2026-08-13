# Epstein Files Toolchain — Design System

**Direction:** Declassified · **Version:** 1.1.0
**Canonical source:** [`releasetheepsteinfiles/branding`](https://github.com/releasetheepsteinfiles/branding)

This document lives in `releasetheepsteinfiles/branding` and is copied
byte-identically into every consumer repository by `sync.sh`. It is the
shared contract that keeps them looking like one family of tools:

| Repo | Surface | Role |
|---|---|---|
| [`epsteinexposed`](https://github.com/releasetheepsteinfiles/epsteinexposed) | Python client + docs site | The library |
| [`epsteinexposed-mcp`](https://github.com/releasetheepsteinfiles/epsteinexposed-mcp) | MCP server + docs site | Structured search for agents |
| [`epstein-files-rag-mcp`](https://github.com/releasetheepsteinfiles/epstein-files-rag-mcp) | RAG MCP server + docs site | Semantic search for agents |
| [`epsteinexplorer`](https://github.com/releasetheepsteinfiles/epsteinexplorer) | Chat app + docs site | The product |

---

## 1. Why this direction

These tools sit on top of court filings, flight logs and released
government records about a criminal case with real victims. The visual
language has to earn trust with journalists, researchers and skeptical
readers on Twitter and Reddit. That rules out two tempting registers:

- **Neon cyberpunk** (the previous `#22d3ee` cyan theme) reads as
  entertainment. It aestheticises the material and undercuts the claim
  that this is a research instrument.
- **True-crime lurid** — blood reds, distressed textures, conspiracy
  corkboards — is worse. It signals advocacy, not evidence.

**Declassified** is the register of the source material itself: a
document release. Dark archival navy, hairline rules, monospace labels,
one ember accent standing in for stamp ink, and redaction bars as the
signature motif. It is sober, it is distinctive in a timeline, and it
says *primary sources* rather than *hot take*.

### Ethical constraints on the aesthetic

These are binding, not stylistic preferences:

1. **Never animate a redaction bar "unblurring" to reveal a name.**
   The motif is decorative and must stay abstract. Revealing real names
   as a visual flourish turns victims and unindicted individuals into
   set dressing.
2. **Never use a person's photograph** in promo material, docs or
   chrome. Inclusion in this database is not an accusation, and the
   disclaimer every repo carries must not be contradicted by imagery.
3. **Redaction bars stand in for nothing real** — use them on the
   product's own name (`EPSTEIN ███ EXPLORER`) or on lorem-style filler,
   never over an actual record shown in a screenshot.
4. **Status colours mean status.** `--color-seal` is for errors, not for
   making a claim look alarming.

---

## 2. Palette

One accent. Four surface steps. Four text steps. Two status colours.
Contrast ratios are measured against `--color-ink`.

### Surfaces

| Token | Hex | Use |
|---|---|---|
| `--color-ink` | `#0b1017` | Page background. The darkest step. |
| `--color-deep` | `#10171f` | Code blocks, inset wells, input fields. |
| `--color-panel` | `#161f2b` | Cards, sidebars, raised surfaces. |
| `--color-line` | `#243040` | Hairline borders, dividers, rules. |

Do not invent a fifth grey. If an element needs to read as raised, give
it a `--color-line` border rather than a new background value.

### Text

| Token | Hex | Contrast | Use |
|---|---|---|---|
| `--color-muted` | `#5c6c82` | 3.4:1 | List markers, disabled state, decorative borders. **Never body text.** |
| `--color-subtle` | `#94a3b8` | 7.1:1 | Secondary text, captions, nav idle. |
| `--color-text` | `#e4e8ee` | 15.0:1 | Body copy. |
| `--color-bright` | `#f5f7fa` | 17.2:1 | Headings, emphasis, active nav. |

### Accent and status

| Token | Hex | Contrast | Use |
|---|---|---|---|
| `--color-ember` | `#e8913a` | 7.5:1 | The single accent: links, focus rings, active nav, the highlighted half of a logotype, stamp chips. |
| `--color-ember-dim` | `#8a5520` | — | Hover/pressed states, dim rules, chip borders. |
| `--color-seal` | `#c0524a` | 3.9:1 | Errors and destructive actions. Large text or icons only — pair with `--color-bright` when used as a fill. |
| `--color-verify` | `#5fa37e` | 6.4:1 | Success, "source verified" states. |

**The restraint is the brand.** The previous system had cyan, violet,
amber and rose all live at once, which is why nothing read as
intentional. If you find yourself wanting a second accent, you probably
want a different *weight* or *size* instead.

---

## 3. Typography

```
Display / headings / labels / nav / UI  →  JetBrains Mono
Running prose (paragraphs, docs body)   →  Inter
Code                                     →  JetBrains Mono
```

Monospace carries the archival register and sets everything structural.
Inter carries long-form prose only, because extended monospace reading is
genuinely punishing. This split is the core typographic decision — keep
it.

### Scale

| Role | Size | Weight | Tracking | Family |
|---|---|---|---|---|
| Hero | `clamp(1.9rem, 4vw, 2.75rem)` | 700 | `-0.02em` | Mono |
| H1 | `1.85rem` | 700 | `-0.02em` | Mono |
| H2 | `1.35rem` | 600 | `-0.01em` | Mono |
| H3 | `1.05rem` | 600 | `0` | Mono |
| Body | `0.9375rem` / 1.7 | 400 | `0` | Sans |
| Small | `0.8125rem` | 400 | `0` | Sans |
| Kicker / stamp | `0.6875rem` | 500 | `0.12em`, uppercase | Mono |
| Code | `0.8125rem` | 400 | `0` | Mono |

Both families load from Google Fonts with `display=swap`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link
  href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap"
  rel="stylesheet"
/>
```

---

## 4. Motifs

**Redaction bar** (`.redact`, `.redact-ember`) — a solid block standing in
for withheld text. The signature device. Use in logotypes and hero
headlines. Subject to the ethical constraints in §1.

**Stamp chip** (`.stamp`) — uppercase mono, letterspaced, ember, thin
`--color-ember-dim` border, 2px radius. Used for version badges, file
numbers, section kickers, `beta` tags.

**Hairline rule** — 1px `--color-line`. Separates everything. This system
uses rules where other systems would use shadows; there are no drop
shadows anywhere.

**File numbering** — docs sections and video cards carry a monospace
kicker (`FILE 01 — CLIENT`, `EXH. 04`). Cheap, and it does a lot of work
to sell the archival premise.

---

## 5. Geometry and motion

Radii stay tight: `2px` / `4px` / `6px`. Documents have corners.

Motion is mechanical — `cubic-bezier(0.2, 0, 0, 1)`, nothing overshoots,
nothing bounces. Durations: `120ms` fast, `180ms` base, `320ms` slow.
The aesthetic leans on typography rather than movement, so
`prefers-reduced-motion` costs nothing; `tokens.css` disables animation
globally under that query.

---

## 6. Integration per repo

Every repo carries `brand/tokens.css` (the `:root` source of truth) and
this document. How each surface consumes it:

| Surface | Stack | Integration |
|---|---|---|
| `epsteinexposed/docs` | Vite + React + Tailwind 4 | `src/brand.css` mirrors tokens in `@theme`; imported by `src/index.css` |
| `epsteinexposed-mcp/docs` | VitePress | `.vitepress/theme/custom.css` maps `--vp-*` onto the palette |
| `epstein-files-rag-mcp/docs` | Vite + React | `src/styles.css` imports `brand/tokens.css` |
| `epsteinexplorer/frontend` | Vite + React + Tailwind 4 | `src/brand.css` mirrors tokens in `@theme`; imported by `src/index.css` |
| `epsteinexplorer/docs` | Vite + React (plain CSS) | `src/styles.css` imports `brand/tokens.css` |

### Tailwind 4 token names

The `@theme` mirror uses the same names as `tokens.css`, so utility
classes read directly off the vocabulary above:

```
bg-ink  bg-deep  bg-panel     border-line   text-muted   text-subtle
text-text  text-bright  text-ember  bg-ember  border-ember
text-seal  text-verify
```

There is exactly one vocabulary. A component written for the Explorer
app drops into the docs site unchanged — which was the whole point of
the alignment.

---

## 7. Do / Don't

**Do**
- Reach for a hairline rule before a background change.
- Let ember be the only thing that glows.
- Set structure in mono, prose in Inter.
- Keep radii tight and shadows absent.

**Don't**
- Add a second accent hue.
- Use `--color-muted` for anything a reader must actually read.
- Animate redaction reveals over real records.
- Introduce drop shadows, glows, scanlines or CRT effects — those
  belonged to the retired cyberpunk theme.

---

## 8. Changing this system

Edit `DESIGN.md` and `tokens.css` **in `releasetheepsteinfiles/branding`**,
bump the version at the top of both files, add a `CHANGELOG.md` entry, then
propagate:

```bash
./sync.sh ~/src            # writes brand/ into every consumer repo found there
./sync.sh --check ~/src    # CI mode: exits non-zero if any repo has drifted
```

Never edit `brand/DESIGN.md` or `brand/tokens.css` inside a consumer repo — the
next sync overwrites it, and the change is lost without warning.

Drift between repos is the failure mode this system exists to prevent. The
pre-alignment state had three different palettes across four surfaces, all
nominally "the same theme"; v1.0.0 fixed the values but left propagation as a
manual "copy both files verbatim into the other three repositories", which is
the same failure mode wearing a process. `sync.sh` closes it.

Two independent checks guard the boundary:

| Check | Scope | Catches |
| :--- | :--- | :--- |
| `sync.sh --check` | across repos | a consumer repo whose `brand/` has drifted from canon |
| `verify-tokens.mjs` | within a repo | a Tailwind `@theme` mirror that disagrees with `brand/tokens.css` |

Run the first in this repo's CI, the second in each consumer's CI.
