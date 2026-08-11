"""5-row grid. Top row's peak cropped; grid sat flush to the bottom edge (no gap);
the three 6-wide rows widened to 8 by adding one hex at each end, which crops
only 15px at the frame sides."""
import json
W,H = 1920,1080
w = 235.0; h = round(w*1.1547,1)      # 271.4
gx, gy = 10.0, 6.0
pitch = 0.75*h + gy                   # 209.6
BOTTOM = 0.0                          # was 40 — the gap TJ spotted
ROWS = [8,7,8,7,8]                    # was 6-7-6-7-6; +1 each end of every 8-row
n = len(ROWS)
row_top = [round((H-BOTTOM-h) - (n-1-r)*pitch, 1) for r in range(n)]
row_x0  = [round((W - (c*w + (c-1)*gx))/2, 1) for c in ROWS]

# Measured 08-05 occlusion. Rows 1 and 3 (7-wide) are untouched, so their indices
# are unchanged. Rows 0/2/4 gained a cell at index 0, so old i -> new i+1.
DEAD = {'3:3':0.697,                                       # old row2 centre
        '4:2':0.98,'4:3':0.966,'4:4':1.00,'4:5':0.98}      # old row3 inner four
KEPT = {'4:1':0.08,'4:6':0.07}                             # "those were fine"

live=[]
for r,c in enumerate(ROWS):
    for i in range(c):
        k=f'{r}:{i}'
        if k in DEAD: continue
        live.append((DEAD.get(k, KEPT.get(k,0.0)), r, abs(i-(c-1)/2), k))
live.sort()
FILL=[k for *_,k in live]

crop_top  = -row_top[0]
crop_side = -row_x0[0]
print(f'hex {w:.0f} x {h:.0f}   pitch {pitch:.1f}   rows {ROWS} = {sum(ROWS)} positions')
print(f'row tops  {row_top}')
print(f'row x0    {row_x0}')
print(f'top crop  {crop_top:.1f}px = {100*crop_top/h:.1f}% of hex height')
print(f'side crop {crop_side:.1f}px = {100*crop_side/w:.1f}% of hex width (8-wide rows only)')
print(f'bottom    row 4 ends at y={row_top[-1]+h:.0f} — flush, no gap')
print(f'dead {len(DEAD)}   LIVE {len(FILL)}')
json.dump({'W':W,'H':H,'w':w,'h':h,'gx':gx,'gy':gy,'rows':ROWS,'row_top':row_top,
           'row_x0':row_x0,'dead':list(DEAD),'fill':FILL}, open('layout.json','w'), indent=1)
