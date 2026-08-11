import json, base64, os
L = json.load(open('layout.json'))
ART = {f[:-4]:'data:image/png;base64,'+base64.b64encode(open(f'final/art/{f}','rb').read()).decode()
       for f in os.listdir('final/art') if f.endswith('.png')}
CARDS=[("glass","half full","orange","the same volume, twice"),
("kardashev","kardashev","blue","energy, not territory"),
("emc2","E = mc²","blue","mass is stored energy"),
("massratio","mass ratio","blue","the rocket is mostly fuel"),
("moore","Moore's Law","blue","an S-curve, not a ramp"),
("wavelet","signal","blue","the spike and the rebound"),
("spiky","spiky","blue","the average hides the peak"),
("spectrum","spectrum","red","not a line — a radius"),
("iceberg","what they see","orange","the visible tenth"),
("toomuch8","too much","orange","load without margin"),
("toomuchload","too much load","orange","the budget nobody sees"),
("buttinchair","butt in chair","green","the only reliable method"),
("killdarlings","kill your darlings","green","cut what you love most"),
("firstdraft","first draft","green","it is supposed to be bad"),
("idonotunderstand","i do not understand","green","the honest starting point"),
("squiggle","one line","green","never lift the pen")]
assign = dict(zip(L['fill'], CARDS))
P='50,0 100,28.87 100,86.6 50,115.47 0,86.6 0,28.87'
w,h = L['w'], L['h']

tiles=[]
for r,c in enumerate(L['rows']):
    for i in range(c):
        k=f'{r}:{i}'
        if k in L['dead']: continue
        x = L['row_x0'][r] + i*(w+L['gx']); y = L['row_top'][r]
        card = assign.get(k)
        # top row is cropped: push its content down so nothing important is lost
        nudge = ' style="transform:translateY(16px)"' if r==0 else ''
        frame = (f'<svg class=frame viewBox="0 0 100 115.47" preserveAspectRatio=none>'
                 f'<polygon class=face points="{P}"/><polygon class=edge points="{P}"/></svg>')
        if card:
            s,lbl,col,sub = card
            lit = ' lit' if s=='glass' else ' dim'
            inner = (f'<div class=art style="--s:url({ART[s]})"></div>'
                     f'<div class=lbl>{lbl}</div><div class=sub>{sub}</div>')
        else:
            col, lit = 'blue', ' dim type'
            inner = '<div class="lbl tonly">type<br>only</div>'
        tiles.append(f'<div class="hex {col}{lit}" style="left:{x:.1f}px;top:{y:.1f}px">'
                     f'{frame}<div class=inner{nudge}>{inner}</div></div>')

html = f'''<!doctype html><meta charset=utf-8><title>Hex HUD — 5-row wall</title>
<style>
:root{{--blue:#5fb8ff;--green:#5fe0a8;--orange:#ffa64d;--red:#ff5f6d}}
*{{box-sizing:border-box}}
html,body{{margin:0;width:{L['W']}px;height:{L['H']}px;overflow:hidden;background:#05070a;
 font:14px/1.3 -apple-system,"Segoe UI",Roboto,sans-serif;color:#e6edf5}}
#stage{{position:relative;width:{L['W']}px;height:{L['H']}px;overflow:hidden}}
#stage::before{{content:"";position:absolute;inset:0;
 background:radial-gradient(120% 90% at 50% 94%,rgba(90,140,200,.06),transparent 62%)}}
.hex{{position:absolute;width:{w}px;height:{h}px;display:grid;place-items:center}}
.frame{{position:absolute;inset:0;width:100%;height:100%}}
.face{{fill:currentColor;opacity:.05}}
.edge{{fill:none;stroke:currentColor;stroke-width:.75px;
 vector-effect:non-scaling-stroke;opacity:.8}}
.blue{{color:var(--blue)}}.green{{color:var(--green)}}
.orange{{color:var(--orange)}}.red{{color:var(--red)}}
.inner{{position:relative;display:flex;flex-direction:column;align-items:center;gap:9px}}
.art{{width:138px;height:138px;background-color:currentColor;
 -webkit-mask-image:var(--s);mask-image:var(--s);
 -webkit-mask-size:contain;mask-size:contain;-webkit-mask-position:center;mask-position:center;
 -webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;filter:drop-shadow(0 0 8px currentColor)}}
.lbl{{font:700 12px/1.2 sans-serif;letter-spacing:.13em;text-transform:uppercase;
 max-width:172px;text-align:center}}
.tonly{{font-size:10px;opacity:.8}}
.sub{{font:400 10px/1.3 sans-serif;letter-spacing:.03em;color:#8fa2b5;max-width:176px;
 text-align:center;opacity:0}}
.dim .face{{opacity:.016}}.dim .edge{{opacity:.19}}
.dim .inner{{opacity:.30}}.dim .art{{filter:none}}
.lit .sub{{opacity:.9}}
.type .inner{{opacity:.22}}
/* ---------- seated stand-in, scaled to the measured coverage ---------- */
#tj{{position:absolute;left:50%;bottom:0;transform:translateX(-50%);
 width:1000px;height:470px;z-index:5;pointer-events:none}}
#tj div{{position:absolute;background:#05070a;border-color:#40596b;border-style:dashed}}
#tj .head{{left:50%;top:0;transform:translateX(-50%);width:196px;height:222px;
 border-radius:50%;border-width:2px}}
#tj .neck{{left:50%;top:196px;transform:translateX(-50%);width:124px;height:56px;
 border-width:0 2px}}
#tj .torso{{left:50%;bottom:0;transform:translateX(-50%);width:980px;height:250px;
 border-width:2px 2px 0;border-radius:300px 300px 0 0}}
#tj .cap{{left:0;right:0;bottom:70px;background:none;border:none;text-align:center;
 font:600 13px/1.8 sans-serif;letter-spacing:.22em;text-transform:uppercase;color:#55738a}}
/* ---- SWAP IN THE REAL CUTOUT: uncomment, drop tj_cutout.png beside this file ----
#tj > div{{display:none}}
#tj{{width:1040px;height:640px;background:url(tj_cutout.png) bottom center/contain no-repeat}}
*/
</style>
<body><div id=stage>
{chr(10).join(tiles)}
<div id=tj><div class=torso></div><div class=neck></div><div class=head></div>
 <div class=cap>your cutout<br>goes here</div></div>
</div>'''
open('wall5_standalone.html','w').write(html)
print(f'{len(tiles)} live hexes  ·  {len(assign)} with art  ·  {len(tiles)-len(assign)} type-only'
      f'  ·  {round(len(html)/1024)} KB')
