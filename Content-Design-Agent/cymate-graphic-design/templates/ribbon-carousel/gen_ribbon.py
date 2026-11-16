# SEAMLESS RIBBON CAROUSEL GENERATOR (format from CR04 "REPLIEEEES", inspired by the stretched-word vehicle carousels on Pinterest).
# One long stretched word runs across every slide on a single path; the mascot rides the front of it and reveals the letters.
# Edit: C (path control points, global x across N slides), the word parts (REPLI + E... + S), END_X, the drive windows, and the slide bodies near the bottom.
# Run from a working folder: python3 gen_ribbon.py  -> writes slides/01.html ... then: python3 scripts/make_carousel.py slides/ out/name.pdf --video
# Rules: keep the path monotonic in x (no loops), gentle waves (amplitude ~100-130px) so letters do not crowd in the troughs, start the word >= 96px inside slide 1,
# and slide 1 must show the headline, the first letters and the mascot at frame 0. Long renders: run slides one by one with make_reel.py if a batch times out.
import math, pathlib, json
W,H,N=1080,1350,5
# --- control points across the panorama (global x, y) ---
C=[(-140,780),(300,700),(720,790),(1120,650),(1500,560),(1880,720),(2240,820),(2620,690),(3000,560),(3360,640),(3720,790),(4080,730),(4420,600),(4700,530),(5000,540)]
def catmull(P,steps=40):
    out=[]
    P=[P[0]]+P+[P[-1]]
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=P[i-1],P[i],P[i+1],P[i+2]
        for s in range(steps):
            t=s/steps;t2=t*t;t3=t2*t
            x=0.5*((2*p1[0])+(-p0[0]+p2[0])*t+(2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2+(-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3)
            y=0.5*((2*p1[1])+(-p0[1]+p2[1])*t+(2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2+(-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3)
            out.append((x,y))
    out.append(P[-2]); return out
pts=catmull(C)
cum=[0]
for a,b in zip(pts,pts[1:]): cum.append(cum[-1]+math.hypot(b[0]-a[0],b[1]-a[1]))
TOTAL=cum[-1]
def dist_at_x(x):
    for i in range(len(pts)-1):
        if pts[i][0]<=x<=pts[i+1][0]:
            f=(x-pts[i][0])/max(1e-6,pts[i+1][0]-pts[i][0]); return cum[i]+f*(cum[i+1]-cum[i])
    return 0 if x<pts[0][0] else TOTAL
def y_at_x(x):
    for i in range(len(pts)-1):
        if pts[i][0]<=x<=pts[i+1][0]:
            f=(x-pts[i][0])/max(1e-6,pts[i+1][0]-pts[i][0]); return pts[i][1]+f*(pts[i+1][1]-pts[i][1])
D="M"+" L".join(f"{x:.1f} {y:.1f}" for x,y in pts)
END_X=4320+600            # where the ribbon text ends (global)
TEXT_START=dist_at_x(96)  # text starts just inside slide 1
TEXT_LEN=dist_at_x(END_X)-TEXT_START
FS=138
n_chars=int(TEXT_LEN/(FS*0.64))
word="REPLI"+"E"*(n_chars-6)+"S"

def drive_keyframes(name,x0,x1,ease_out=False,k=24):
    """vehicle offset-distance and clip width keyframes, x linear in time (or ease-out)"""
    off=[];clip=[]
    for j in range(k+1):
        u=j/k                                  # fraction of x travelled
        t=(1-math.sqrt(1-u)) if ease_out else u  # time at which x reaches u (ease-out quad inverse)
        x=x0+(x1-x0)*u
        off.append(f"{t*100:.2f}%{{offset-distance:{dist_at_x(x)/TOTAL*100:.3f}%}}")
        clip.append((t*100,x))
    return f"@keyframes {name}{{{''.join(off)}}}", clip

slides=[]
for i in range(N):
    gx=i*W
    # drive window for this slide (global x)
    if i==0: x0,x1,t0,dur,eo=gx+600,gx+W+140,0.15,2.4,False
    elif i<N-1: x0,x1,t0,dur,eo=gx+60,gx+W+140,0.1,2.6,False
    else: x0,x1,t0,dur,eo=gx+60,END_X+70,0.1,2.0,True
    kf,clip=drive_keyframes(f"drv{i}",x0,x1,eo)
    clipkf="@keyframes clp%d{%s}"%(i,"".join(f"{t:.2f}%{{width:{max(0,x-gx-24):.1f}px}}" for t,x in clip))
    slides.append(dict(i=i,gx=gx,x0=x0,x1=x1,t0=t0,dur=dur,kf=kf,clipkf=clipkf))

def t_at(s,xg):  # when the vehicle passes global x on slide s (linear slides only)
    return s['t0']+(xg-s['x0'])/(s['x1']-s['x0'])*s['dur']

tick='<svg width="26" height="26" viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="#1DB954"/><path d="M7 12.5l3.2 3L17 8.5" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def tag(s,xl,text,above=True,rot=-3):
    xg=s['gx']+xl; y=y_at_x(xg); t=t_at(s,xg)+0.15
    top=(y-330) if above else (y+70)
    line_y1,line_y2=((top+92),(y-118)) if above else ((y+12),(top))
    return (f'''<svg class="a-fade" style="--d:{t:.2f}s;position:absolute;left:0;top:0;z-index:2" width="1080" height="1350"><path d="M{xl} {line_y1:.0f} L{xl} {line_y2:.0f}" stroke="#14161C" stroke-opacity=".35" stroke-width="2" stroke-dasharray="3 7" stroke-linecap="round"/><circle cx="{xl}" cy="{line_y2:.0f}" r="5" fill="#14161C" fill-opacity=".45"/></svg>
<div class="tag a-pop" style="--d:{t:.2f}s;left:{xl-190}px;top:{top:.0f}px;transform:rotate({rot}deg)">{tick}{text}</div>''', t)

def page(s, body, sfx, extra=""):
    i=s['i']
    ribbon=f'''
<div class="pano" style="transform:translateX({-s['gx']}px)">
  <svg width="{N*W}" height="{H}" viewBox="0 0 {N*W} {H}" style="position:absolute;left:0;top:0;overflow:visible">
    <defs>
      <linearGradient id="rg" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{N*W}" y2="0"><stop offset="0" stop-color="#E23A00"/><stop offset=".5" stop-color="#FF5A00"/><stop offset="1" stop-color="#FF7A2E"/></linearGradient>
      <filter id="ls" x="-5%" y="-30%" width="110%" height="160%"><feDropShadow dx="0" dy="10" stdDeviation="9" flood-color="#7A2A00" flood-opacity=".22"/><feDropShadow dx="0" dy="2" stdDeviation="1.5" flood-color="#5A1E00" flood-opacity=".25"/></filter>
      <path id="rp" d="{D}"/>
    </defs>
  </svg>
</div>
<div class="clip" style="animation:clp{i} {s['dur']}s linear {s['t0']}s both">
  <div class="pano" style="transform:translateX({-s['gx']}px)">
    <svg width="{N*W}" height="{H}" viewBox="0 0 {N*W} {H}" style="position:absolute;left:0;top:0;overflow:visible">
      <text font-family="Poppins" font-weight="800" font-size="{FS}" fill="url(#rg)" filter="url(#ls)" letter-spacing="0"><textPath href="#rp" startOffset="{TEXT_START:.1f}" textLength="{TEXT_LEN:.1f}" lengthAdjust="spacing">{word}</textPath></text>
    </svg>
  </div>
</div>
<div class="pano" style="transform:translateX({-s['gx']}px);z-index:4">
  <img class="veh" src="{{{{MASCOT}}}}" alt="" style="animation:drv{i} {s['dur']}s linear {s['t0']}s both">
</div>'''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>CR04 slide {i+1}</title>
<meta name="reel-duration" content="4.6"><meta name="reel-cover" content="0.6"><meta name="still-time" content="4.4">
<meta name="reel-sfx" content="{sfx}">
{{{{BASE_CSS}}}}
<style>
.pano{{position:absolute;left:0;top:0;width:{N*W}px;height:{H}px;pointer-events:none}}
.clip{{position:absolute;left:0;top:0;height:{H}px;overflow:hidden;z-index:3}}
.veh{{position:absolute;left:0;top:0;width:200px;offset-path:path('{D}');offset-rotate:auto;offset-anchor:50% 74%;filter:drop-shadow(0 18px 18px rgba(90,30,0,.28)) drop-shadow(0 3px 3px rgba(60,20,0,.25))}}
.tag{{position:absolute;z-index:5;width:380px;box-sizing:border-box;display:flex;align-items:center;gap:14px;padding:22px 26px;border-radius:22px;background:#FFFFFF;font-family:Poppins,sans-serif;font-weight:600;font-size:28px;color:#14161C;
  box-shadow:0 24px 50px rgba(60,30,10,.16),0 4px 10px rgba(60,30,10,.10),inset 0 1px 0 #fff;border:1px solid rgba(20,22,28,.06)}}
.kk{{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:21px;letter-spacing:5px;color:#5E5A55}}
.H{{font-family:Poppins,sans-serif;font-weight:300;font-size:74px;letter-spacing:-2.5px;line-height:1.02;color:#0A0C14}}
.H b{{font-weight:800}}
{s['kf']}
{s['clipkf']}
{extra}
</style></head><body>
<div class="cm paper" style="width:{W}px;height:{H}px">
<div style="position:absolute;left:-200px;top:-200px;width:900px;height:800px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,150,90,.14),rgba(255,150,90,0))"></div>
<img src="{{{{LOGO_DARK}}}}" alt="Cymate" style="position:absolute;left:112px;top:134px;height:32px;z-index:6">
<div style="position:absolute;right:112px;top:136px;z-index:6;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:20px;letter-spacing:3px;color:#55524E">{i+1:02d} / {N:02d}</div>
{ribbon}
{body}
</div></body></html>'''

out={}
s=slides[0]
out[0]=page(s,'''
<div class="content" style="left:96px;right:96px;top:250px;z-index:5">
  <div class="kk">WHEN OUTBOUND IS DONE RIGHT</div>
  <div class="H" style="margin-top:26px">Your inbox<br>starts filling with</div>
</div>
<div class="content" style="right:112px;top:1150px;z-index:6;display:flex;align-items:center;gap:14px;font-family:Inter,sans-serif;font-weight:700;font-size:20px;letter-spacing:3px;color:#5E5A55">SWIPE <svg class="a-nudge" width="44" height="16" viewBox="0 0 44 16"><path d="M0 8h40M33 1l8 7-8 7" fill="none" stroke="#FF5A00" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></div>''',
 "0.15:whoosh")
labels=[(1,520,"Warmed-up inboxes",True,-3),(2,560,"A list someone checked",False,3),(3,520,"Copy that sounds human",True,-2)]
for idx,xl,txt,ab,rot in labels:
    s=slides[idx]; html,t=tag(s,xl,txt,ab,rot)
    out[idx]=page(s,html,f"0.1:whoosh, {t:.2f}:pop")
s=slides[4]
cal_rows=[("Tue 10:00","Intro call · Northwind"),("Wed 2:30","Discovery · Brightlane"),("Thu 11:00","Demo · Fieldworks")]
rows="".join(f'''<div class="a-left" style="--d:{2.2+k*0.3:.2f}s;display:flex;align-items:center;gap:18px;padding:16px 18px;border-radius:16px;background:{['#FFF1E8','#FFF5EE','#EAF8EF'][k]};margin-top:12px">
<div style="width:6px;align-self:stretch;border-radius:3px;background:{['#FF5A00','#FF9A5C','#14894A'][k]}"></div>
<div style="font-family:'IBM Plex Mono',monospace;font-size:19px;font-weight:600;color:#5E5A55;width:130px">{a}</div><div style="font-family:Inter,sans-serif;font-weight:700;font-size:23px;color:#14161C">{b}</div></div>''' for k,(a,b) in enumerate(cal_rows))
out[4]=page(s,f'''
<div class="content" style="left:96px;right:96px;top:250px;z-index:5">
  <div class="H">Then your calendar<br>does <b class="grad-text" style="padding-right:6px">this.</b></div>
</div>
<div class="a-rise" style="--d:1.9s;position:absolute;left:96px;right:96px;top:700px;z-index:5;background:#FFFFFF;border-radius:32px;padding:26px 28px 28px;box-sizing:border-box;box-shadow:0 40px 80px rgba(60,30,10,.16),0 6px 14px rgba(60,30,10,.10);font-family:Inter,sans-serif">
  <div style="display:flex;justify-content:space-between;align-items:center"><div style="font-weight:800;font-size:28px;color:#14161C">This week</div><span class="a-pop" style="--d:3.2s;display:inline-flex;align-items:center;gap:8px;padding:8px 16px;border-radius:999px;background:linear-gradient(90deg,#C21A00,#FF5A00 60%,#FF9A5C);color:#fff;font-weight:700;font-size:19px">3 booked</span></div>
  {rows}
</div>
<div class="a-pop" style="--d:3.5s;position:absolute;left:0;right:0;top:1185px;z-index:6;text-align:center"><span class="gpill" style="font-size:26px">Cymate runs all of it · link in bio</span></div>''',
 "0.1:whoosh, 2.1:thud, 2.2:pop, 2.5:pop, 2.8:pop, 3.2:ding")
for k,h in out.items(): pathlib.Path(f"slides/{k+1:02d}.html").write_text(h)
print("chars",len(word),"textlen",round(TEXT_LEN),"total",round(TOTAL))
