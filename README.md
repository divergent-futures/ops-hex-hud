# ops-hex-hud

Hexagonal HUD for the Divergent Futures streams — 192 cards in the bank, a wall of
them on screen per show, lit individually while talking, with a private prompter
screen. Four channels: **DF** Divergent Futures · **HIS** Humans in Space ·
**LOTS** Living on the Spectrum · **BOOK** book writing.

`ops-` per the org convention: studio machinery, not something a stranger installs.

## Status

Software complete and content frozen. **This commit seeds the repo with the two
things that were outstanding: the first batch of hand-drawn art, and the grid rework.**
The server / HUD / control / prompter code still needs to land here — it lives in
`hex-hud-v1.1.zip` and has not been committed yet.

## What's here

```
public/art/          16 drawings, alpha-masked, drop-in ready
tools/art/           white-background scan -> alpha mask pipeline
tools/grid/          layout model + wall renderer
preview/             rendered checks (1920x1080 wall, per-card lit/unlit sheets)
```

## The art pipeline, in one paragraph

Scans render as a CSS **mask**: the PNG's alpha gives the shape and the colour comes
from the hex, so a drawing dims and lights exactly like the built-in vector glyphs.
Consequences: **ink colour in the scan is irrelevant** (black pen, blue pen, pencil —
identical once masked), and **a non-transparent white background renders as a solid
filled hex**, because the whole rectangle becomes "ink". `tools/art/convert.py`
turns white-background line art into a correct mask; see `public/art/README-CONVERSION.md`.

## Adding a drawing

1. Put the PNG in `public/art/`.
2. Add `"img": "<filename>.png"` to the matching item in `public/bank.json`.
3. Reload the OBS browser source.

No code change, no rebuild.

## The grid

`tools/grid/layout.py` is the source of truth for geometry and the occlusion table;
`build_wall.py` renders a 1920×1080 wall from it, so the render can never disagree
with the model. Current: **8-7-8-7-8 = 38 positions, 5 measured dead cells, 33 live.**
Full reasoning in `tools/grid/GRID-NOTES.md`.

## Licence

Open source, like everything Divergent Futures makes.

| What | Licence |
|---|---|
| Code, tools, docs | MIT — `LICENSE` |
| Drawings in `public/art/` | CC BY 4.0 — `LICENSE-ART` |

Both allow commercial use. Both require credit to Divergent Futures. The split
exists because software licences handle artwork badly — MIT says nothing useful
about a drawing, and CC licences say nothing useful about source code.

## Known gaps

- App code not yet committed (see Status).
- `tj_cutout.png` (webcam cutout used to measure occlusion) is not in the repo and
  the original was lost; the wall preview ships a stand-in placeholder.
- 33 live slots vs content frozen at 21 per channel — unresolved by design.
