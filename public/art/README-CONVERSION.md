# hex HUD art — conversion notes (2026-08-10)

These 16 PNGs are drop-in ready for `hexhud/public/art/`.

## What was done to the source JPEGs

The source files were **opaque white-background JPEGs**. Dropped into `public/art/`
as-is they would each have rendered as a **solid filled hexagon** — the whole
rectangle becomes "ink" under the mask pipeline. That's the failure mode already
documented in `public/art/README.md`.

`convert.py` fixes it:

1. Estimate the paper level per-image with a large-radius max-filter + blur
   (handles uneven lighting / off-white paper — several sources measured 213–247
   grey in the corners, not 255).
2. `alpha = 1 - (luminance / paper)`, so ink → opaque, paper → transparent.
3. Levels clamp at 0.10 / 0.55 to kill JPEG noise and paper texture without
   eating real line edges.
4. Trim to content bbox, pad to square, resample to 1024×1024.
5. Write RGBA with **black RGB and the computed alpha**. RGB is irrelevant under
   a mask; only alpha matters.

Six pieces were stroke-thickened (morphological dilate) because their linework
was too fine to survive rendering at 60% of hex width:
`wavelet +13px, toomuchload +9px, kardashev +7px, toomuch8 +7px, moore +7px, spiky +5px`.

## Verified

Rendered through a replica of the HUD's mask path (`background-color: currentColor`
+ `mask-image`), dark background, dormant and lit side by side. All 16 dim and
light with the hex exactly like the built-in vector glyphs. No `rawimg` needed
on any of them.

## Alternates

`_alternates/` holds versions with the artist's handwritten caption cropped out
(`massratio`, `killdarlings`, `toomuchload`). At hex scale the handwriting inside
a drawing is illegible **and** it duplicates the hex's own printed label.
`massratio_nolabel.png` is the clearest demonstration. Swap in if wanted.

## Integration

```
public/art/glass.png                     <- copy the file
public/bank.json  ->  "img": "glass.png" <- one line on the matching item
```
Reload the browser source. No code change.

**Slugs here are inferred from the drawings, not read from `bank.json`** — the
zip wasn't in this session. Confirm each filename against the real item key
before wiring, or just rename the PNG to match.
