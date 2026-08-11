#!/usr/bin/env python3
"""white-background line art -> transparent alpha mask for hex HUD."""
import sys, os, glob, json
import numpy as np
from PIL import Image, ImageFilter

def to_mask(path, out, size=1024, frame_crop=False, gamma=1.0):
    im = Image.open(path).convert('L')
    a = np.asarray(im).astype(np.float32)

    # --- background estimate: large-radius max-filter approximates the paper level
    bg = np.asarray(Image.fromarray(a.astype(np.uint8))
                    .filter(ImageFilter.MaxFilter(size=25))
                    .filter(ImageFilter.GaussianBlur(30))).astype(np.float32)
    bg = np.clip(bg, 40, 255)

    # --- normalised ink: 0 = paper, 1 = full ink
    ink = 1.0 - (a / bg)
    ink = np.clip(ink, 0, 1)

    # --- levels: kill paper texture / jpeg noise, keep real line edges
    black, white = 0.10, 0.55
    ink = np.clip((ink - black) / (white - black), 0, 1)
    if gamma != 1.0:
        ink = ink ** gamma

    alpha = (ink * 255).astype(np.uint8)

    # --- optional: crop just inside a hand-drawn outer frame
    if frame_crop:
        h, w = alpha.shape
        m = 0.10
        alpha = alpha[int(h*m):int(h*(1-m)), int(w*m):int(w*(1-m))]

    # --- trim to content, then pad square
    ys, xs = np.nonzero(alpha > 12)
    if len(ys):
        y0,y1,x0,x1 = ys.min(), ys.max()+1, xs.min(), xs.max()+1
        alpha = alpha[y0:y1, x0:x1]
    h, w = alpha.shape
    s = max(h, w)
    pad = np.zeros((s, s), np.uint8)
    pad[(s-h)//2:(s-h)//2+h, (s-w)//2:(s-w)//2+w] = alpha
    alpha = pad

    img = Image.fromarray(alpha, 'L').resize((size, size), Image.LANCZOS)
    rgba = Image.merge('RGBA', [Image.new('L',(size,size),0)]*3 + [img])
    rgba.save(out, optimize=True)

    cov = float((np.asarray(img) > 24).mean())
    mean_a = float(np.asarray(img).mean()/255)
    return {'file': os.path.basename(out), 'coverage_pct': round(cov*100,2),
            'mean_alpha': round(mean_a,3)}

if __name__ == '__main__':
    NAMES = json.load(open('/root/hexart/names.json'))
    rep = []
    for src, meta in NAMES.items():
        p = glob.glob(f'/root/hexart/raw/{src}*')[0]
        out = f"/root/hexart/art/{meta['slug']}.png"
        rep.append(to_mask(p, out, frame_crop=meta.get('frame', False),
                           gamma=meta.get('gamma',1.0)) | {'label': meta['label']})
    print(json.dumps(rep, indent=1))
