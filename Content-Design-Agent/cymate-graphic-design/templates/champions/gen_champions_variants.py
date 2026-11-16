import random, math, pathlib
W,H=2560,1440
def streaks(seed, angle_deg, n_grey, n_or, or_box, grey_op=(.12,.42), cx=None, cy=None, radial=False):
    random.seed(seed); out=[]
    def line(x,y,ang,L,w,c,op,b):
        dx,dy=math.cos(ang),math.sin(ang)
        return f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+dx*L:.0f}" y2="{y+dy*L:.0f}" stroke="{c}" stroke-opacity="{op:.2f}" stroke-width="{w:.0f}" stroke-linecap="round" filter="url(#mb{b})"/>'
    for _ in range(n_grey):
        if radial:
            a=random.uniform(0,2*math.pi); r0=random.uniform(380,700); L=random.uniform(400,1200)
            x,y=cx+math.cos(a)*r0, cy+math.sin(a)*r0*0.6; ang=math.atan2(y-cy,x-cx)
        else:
            x=random.uniform(-600,W+300); y=random.uniform(150,H+700); ang=math.radians(angle_deg); L=random.uniform(500,1700)
        out.append(line(x,y,ang,L,random.uniform(2,24),random.choice(['#3B3B3D','#2B2B2C','#4B4B4C','#5C5C5D']),random.uniform(*grey_op),random.choice([1,2,3])))
    for _ in range(n_or):
        x0,x1,y0,y1=or_box
        if radial:
            a=random.uniform(0,2*math.pi); r0=random.uniform(420,760); L=random.uniform(300,900)
            x,y=cx+math.cos(a)*r0, cy+math.sin(a)*r0*0.6; ang=math.atan2(y-cy,x-cx)
        else:
            x=random.uniform(x0,x1); y=random.uniform(y0,y1); ang=math.radians(angle_deg); L=random.uniform(400,1300)
        out.append(line(x,y,ang,L,random.uniform(8,56),random.choice(['#FF5A00','#FF7A1A','#E03A00','#FFB070']),random.uniform(.45,.92),random.choice([2,3])))
    return "".join(out)
DEFS='<defs><filter id="mb1" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2"/></filter><filter id="mb2" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="7"/></filter><filter id="mb3" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="16"/></filter></defs>'
CSS='''.tag{font-family:'Bebas Neue','Archivo Black',sans-serif;line-height:.9;letter-spacing:1px;white-space:nowrap;background:linear-gradient(90deg,#FFFFFF 0%,#FFE9DC 18%,#FFC79F 42%,#FF9A52 70%,#FF6A10 100%);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 10px 24px rgba(0,0,0,.55))}
.bb{font-family:'Bebas Neue','Archivo Black',sans-serif;line-height:.9;white-space:nowrap}
.mono{font-family:'IBM Plex Mono',monospace;font-weight:600;letter-spacing:6px}'''
def page(title,bg,body):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title>{{{{BASE_CSS}}}}<style>{CSS}</style></head><body>
<div class="cm haze-none" style="width:{W}px;height:{H}px;background:{bg}">{body}</div></body></html>'''
METAL='linear-gradient(115deg,#0C0C0C 0%,#181818 45%,#1F1F20 70%,#151515 100%)'
V={}
# C1 stacked, left-aligned, streaks from the right (mirrored)
V['B08-champions-stacked']=page('B08',METAL,f'''
<svg style="position:absolute;inset:0" width="{W}" height="{H}">{DEFS}{streaks(3,-122,120,16,(1900,2700,900,1900))}</svg>
<div style="position:absolute;right:-300px;top:800px;width:1300px;height:900px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,90,0,.28),rgba(255,90,0,0))"></div>
<img src="{{{{MASCOT}}}}" alt="" style="position:absolute;left:-250px;top:-60px;height:1320px;transform:scaleX(-1) rotate(-6deg);z-index:1">
<div class="content" style="left:640px;top:540px;z-index:4">
  <div class="tag" style="font-size:200px">OUTBOUND</div>
  <div style="display:flex;align-items:center;gap:30px"><div class="tag" style="font-size:200px;background-position:40% 0">FOR CHAMPIONS</div><img src="{{{{MONOGRAM}}}}" alt="Cymate" style="height:150px;filter:drop-shadow(0 14px 26px rgba(0,0,0,.55))"></div>
</div>''')
# C2 burnt orange
V['B09-champions-orange']=page('B09','linear-gradient(115deg,#7A2200 0%,#C24000 40%,#E55300 70%,#B83A00 100%)',f'''
<svg style="position:absolute;inset:0" width="{W}" height="{H}">{DEFS}{streaks(5,-58,110,0,(0,1,0,1),grey_op=(.10,.30)).replace('#3B3B3D','#2A0C00').replace('#2B2B2C','#3A1200').replace('#4B4B4C','#FFB27A').replace('#5C5C5D','#FFD2B0')}</svg>
<div style="position:absolute;left:600px;top:300px;width:1400px;height:800px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,190,140,.30),rgba(255,190,140,0))"></div>
<img src="{{{{MASCOT}}}}" alt="" style="position:absolute;left:1870px;top:-70px;height:1320px;transform:rotate(-6deg);opacity:.55;mix-blend-mode:multiply;z-index:1">
<div class="content" style="left:0;right:0;top:640px;z-index:4;display:flex;align-items:center;justify-content:center;gap:28px">
  <div class="bb" style="font-size:150px;color:#FFFFFF;filter:drop-shadow(0 10px 20px rgba(60,12,0,.45))">OUTBOUND FOR <span style="color:#160600">CHAMPIONS</span></div>
  <img src="{{{{LOCKUP_DARK}}}}" alt="" style="display:none"><img src="{{{{MONOGRAM}}}}" alt="Cymate" style="height:128px;filter:drop-shadow(0 12px 22px rgba(60,12,0,.45))"></div>''')
# C3 spotlight stage
V['B10-champions-spotlight']=page('B10','#08090B',f'''
<svg style="position:absolute;inset:0" width="{W}" height="{H}"><defs><linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE3CC" stop-opacity=".30"/><stop offset="1" stop-color="#FF8A3D" stop-opacity="0"/></linearGradient><filter id="sb" x="-20%" y="-10%" width="140%" height="120%"><feGaussianBlur stdDeviation="22"/></filter></defs>
<polygon points="1180,-40 1380,-40 1700,1100 860,1100" fill="url(#beam)" filter="url(#sb)"/>
<polygon points="380,-40 520,-40 1160,1000 820,1060" fill="url(#beam)" opacity=".55" filter="url(#sb)"/>
<polygon points="2040,-40 2180,-40 1740,1060 1400,1000" fill="url(#beam)" opacity=".55" filter="url(#sb)"/></svg>
<div style="position:absolute;left:480px;top:960px;width:1600px;height:320px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,110,30,.55),rgba(255,90,0,.15) 60%,rgba(255,90,0,0))"></div>
<img src="{{{{MASCOT}}}}" alt="" style="position:absolute;left:830px;top:180px;height:1000px;opacity:.9;z-index:1">
<div class="tx tx-dots" style="opacity:.25"></div>
<div class="content" style="left:0;right:0;top:600px;z-index:4;text-align:center">
  <div class="mono" style="font-size:26px;color:rgba(255,255,255,.7)">COLD OUTBOUND · DONE FOR YOU</div>
  <div style="display:flex;align-items:center;justify-content:center;gap:28px;margin-top:20px"><div class="tag" style="font-size:146px">OUTBOUND FOR CHAMPIONS</div><img src="{{{{MONOGRAM}}}}" alt="Cymate" style="height:124px;filter:drop-shadow(0 14px 26px rgba(0,0,0,.55))"></div>
</div>''')
# C4 radial speed burst
V['B11-champions-burst']=page('B11',METAL,f'''
<svg style="position:absolute;inset:0" width="{W}" height="{H}">{DEFS}{streaks(9,0,220,40,(0,0,0,0),cx=1280,cy=720,radial=True)}</svg>
<div style="position:absolute;left:780px;top:430px;width:1000px;height:580px;border-radius:50%;background:radial-gradient(closest-side,rgba(8,9,11,.95),rgba(8,9,11,.6) 55%,rgba(8,9,11,0))"></div>
<img src="{{{{MASCOT}}}}" alt="" style="position:absolute;left:-200px;top:-90px;height:1300px;transform:scaleX(-1) rotate(-8deg);opacity:.9;z-index:1">
<div class="content" style="left:0;right:0;top:612px;z-index:4;display:flex;align-items:center;justify-content:center;gap:28px">
  <div class="tag" style="font-size:150px">OUTBOUND FOR CHAMPIONS</div><img src="{{{{MONOGRAM}}}}" alt="Cymate" style="height:128px;filter:drop-shadow(0 14px 26px rgba(0,0,0,.55))"></div>
<div class="content mono" style="left:0;right:0;top:812px;z-index:4;text-align:center;font-size:24px;color:rgba(255,255,255,.72)">INFRASTRUCTURE · LISTS · COPY · REPLIES</div>''')
# C5 minimal outline + solid
V['B12-champions-minimal']=page('B12','#050506',f'''
<svg style="position:absolute;inset:0" width="{W}" height="{H}">{DEFS}
<line x1="300" y1="900" x2="2260" y2="900" stroke="#FF5A00" stroke-width="10" stroke-linecap="round" filter="url(#mb2)" opacity=".9"/>
<line x1="560" y1="900" x2="2000" y2="900" stroke="#FFC09A" stroke-width="3" stroke-linecap="round"/></svg>
<div style="position:absolute;left:280px;top:760px;width:2000px;height:300px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,90,0,.22),rgba(255,90,0,0))"></div>
<div class="content" style="left:0;right:0;top:600px;z-index:4;display:flex;align-items:center;justify-content:center;gap:34px">
  <img src="{{{{ICON}}}}" alt="" style="height:170px;filter:drop-shadow(0 16px 26px rgba(0,0,0,.6))">
  <div><div class="bb" style="font-size:150px;color:transparent;-webkit-text-stroke:3px rgba(255,255,255,.9)">OUTBOUND FOR</div>
  <div style="display:flex;align-items:center;gap:26px;margin-top:-6px"><div class="tag" style="font-size:150px">CHAMPIONS</div><img src="{{{{MONOGRAM}}}}" alt="Cymate" style="height:118px;filter:drop-shadow(0 14px 26px rgba(0,0,0,.55))"></div></div></div>''')
for k,h in V.items(): pathlib.Path(k+'.html').write_text(h)
print(list(V))
