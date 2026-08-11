"""Caption removal: explicit rect erase where lettering overlaps the drawing's
bounding box, connected-component filter where it sits clear of it."""
import numpy as np, os
from PIL import Image, ImageFilter
from scipy import ndimage

RECTS = {   # normalised x0,y0,x1,y1 regions to erase — measured off a grid overlay
 'moore':            [(0.50,0.40,0.99,0.66)],                  # "Moore's Law"
 'spiky':            [(0.51,0.04,0.87,0.28)],                  # "spiky"
 'toomuchload':      [(0.74,0.00,1.00,0.09),(0.00,0.90,0.14,1.00)],  # "too much" / "load"
 'idonotunderstand': [(0.00,0.83,1.00,1.00)],                  # "I do not understand"
}
COMPS = {'spectrum':0.02,'toomuch8':0.18,'buttinchair':0.03,
         'killdarlings':0.02,'firstdraft':0.01}
THICK = {'wavelet':13,'toomuchload':9,'kardashev':7,'toomuch8':7}
KEEP  = ['glass','kardashev','massratio','emc2','wavelet','squiggle','iceberg']
ALL = ['glass','kardashev','massratio','emc2','moore','spiky','wavelet','spectrum',
       'iceberg','toomuch8','toomuchload','buttinchair','killdarlings','firstdraft',
       'idonotunderstand','squiggle']

def resquare(a,size=1024):
    ys,xs=np.nonzero(a>12); a=a[ys.min():ys.max()+1,xs.min():xs.max()+1]
    h,w=a.shape; s=max(h,w); p=np.zeros((s,s),np.uint8)
    p[(s-h)//2:(s-h)//2+h,(s-w)//2:(s-w)//2+w]=a
    return np.asarray(Image.fromarray(p,'L').resize((size,size),Image.LANCZOS))

os.makedirs('final/art',exist_ok=True); rows=[]
for s in ALL:
    a = np.asarray(Image.open(f'art/{s}.png').split()[-1]).copy(); note=[]
    if s in RECTS:
        h,w = a.shape
        for x0,y0,x1,y1 in RECTS[s]:
            a[int(y0*h):int(y1*h), int(x0*w):int(x1*w)] = 0
        a = resquare(a); note.append('caption erased')
    elif s in COMPS:
        b=a>24; lab,n=ndimage.label(b,structure=np.ones((3,3)))
        sz=ndimage.sum(b,lab,range(1,n+1)); keep=[i+1 for i,v in enumerate(sz) if v>=sz.max()*COMPS[s]]
        a = resquare(np.where(np.isin(lab,keep),a,0).astype(np.uint8)); note.append('caption removed')
    if s in THICK:
        a = resquare(np.asarray(Image.fromarray(a,'L').filter(ImageFilter.MaxFilter(THICK[s]))))
        note.append(f'stroke +{THICK[s]}px')
    if not note: note=['as converted']
    Image.merge('RGBA',[Image.new('L',(1024,1024),0)]*3+[Image.fromarray(a,'L')]).save(f'final/art/{s}.png')
    rows.append(f'{s:20s} {", ".join(note):34s} ink {round(100*float((a>24).mean()),1)}%')
print('\n'.join(rows))
