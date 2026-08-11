# 5-row wall — flush bottom, widened rows (2026-08-11, rev 2)

`wall5_standalone.html` — open directly, no server. Art is embedded as data URIs
because CSS mask images silently fail to load over `file://`.

```
hex        235 × 271.4 px      (pointy-top, w × w·1.1547)
row pitch  209.6 px            (0.75·h + 6px gap)
rows       8-7-8-7-8 = 38 positions
row tops   −29.6 · 180.0 · 389.5 · 599.1 · 808.6
row x0     −15 · 107.5 · −15 · 107.5 · −15
top crop   29.6px = 10.9% of hex height
side crop  15.0px = 6.4% of hex width, 8-wide rows only
bottom     row 4 ends at y=1080 — flush
dead 5  ·  LIVE 33
```

## Changes from rev 1

**Bottom gap closed.** `BOTTOM` margin 40 → 0, so the bottom row's points land
exactly on y=1080. Because the grid is bottom-anchored this drops everything 40px,
which also lowers the top row — the two fixes are the same edit. Side effect: the
top row now crops only 10.9% rather than 25.6%, so its content offset drops from
50px to 16px (it is centred in the *visible* part of the hex, not the full one).

**Three more on either side.** The three 6-wide rows (top, middle, bottom) each
gained one hex at each end → 8 wide. That is +6 positions, three per side.
An 8-wide row measures 1950px against a 1920px frame, so the end hexes crop 15px
— 6.4% of width, and the art sits well inside that, so nothing is lost.
The 7-wide rows are untouched at 107.5px side margins; widening them to 9 would
need 2195px and crop 58% off each end, which is why they stay as they are.

## Occlusion

Rows 1 and 3 are unchanged, so `3:3` (69.7%) still holds. Rows 0/2/4 gained a
cell at index 0, so the bottom row's measured cells shift by one: the inner four
are now `4:2`–`4:5` (96.6–100%) and the two TJ called "fine" are `4:1` and `4:6`
(7–8%). The two brand-new bottom corners, `4:0` and `4:7`, sit at x≈102 and 1817
— nowhere near him, so live. **The bottom row now offers 4 usable slots, up from 2.**

## Slot count

**33 live, against content frozen at 21 per channel.** Rev 1 was 27. Each widening
makes the gap larger: 12 slots per channel now have no card assigned. Either the
rotations grow, or the surplus fills from the bank live. Unresolved by design —
worth settling against a real stream.

Note also that `FILL_ORDER` (least-occluded first, then centre-out) puts all 16
drawings in the top two rows, because everything above the shoulders measures 0%.
The wall therefore reads top-heavy until more art exists. That is the spec's own
ordering rule working correctly, not a layout fault.

## Swapping in the real cutout

The figure is a stand-in sized to the measured coverage, not a likeness. Drop
`tj_cutout.png` beside the HTML and uncomment the two rules at the end of `<style>`.

## Regenerating

`layout.py` → `layout.json` → `build_wall.py` → HTML, so the page can never
disagree with the model. Change `ROWS`, `w` or `BOTTOM` and re-run both.
