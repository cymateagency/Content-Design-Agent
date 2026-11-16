import math, random, pathlib
W,H=1080,1350
def page(name,loop,body,css,bg):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{name}</title><meta name="gif-loop" content="{loop}"><meta name="still-time" content="0">{{{{BASE_CSS}}}}
<style>{css}</style></head><body><div class="cm" style="width:{W}px;height:{H}px;background:{bg}">{body}</div></body></html>'''

# ---------- L01: Replies on repeat (dark UI feed, 6 s) ----------
rows=[('JL','Jordan Lee','Northwind','Sounds interesting. Free Thursday?'),('PS','Priya Shah','Brightlane','Yes, send over a few times.'),
      ('MC','Marcus Cole','Fieldworks','Loop in my VP of Sales here.'),('ER','Elena Ruiz','Kestrel','Perfect timing, actually.'),
      ('SO','Sam Ortiz','Harbor & Co','What does onboarding look like?'),('DK','Dana Kim','Summit Ops','Let’s talk next week.'),
      ('LB','Leo Brandt','Lumen','Can you share how it works?'),('AV','Ava Voss','Granite','Booked. See you Tuesday.')]
RH=132
def row(r,k):
    ini,nm,co,msg=r
    shade=['#FF5A00','#E0A15E','#C7C1B8','#FF8A3D'][k%4]
    return f'''<div style="height:{RH-14}px;margin-bottom:14px;border-radius:20px;background:#1B1917;border:1px solid #2C2825;display:flex;align-items:center;gap:18px;padding:0 22px;box-sizing:border-box">
<div style="flex:none;width:58px;height:58px;border-radius:50%;background:{shade};color:#140700;font-weight:800;font-size:21px;display:flex;align-items:center;justify-content:center;font-family:Poppins,sans-serif">{ini}</div>
<div style="flex:1;min-width:0;font-family:Inter,sans-serif"><div style="display:flex;justify-content:space-between;align-items:center"><span style="font-weight:700;font-size:22px;color:#fff">{nm} <span style="font-weight:500;color:#9C958D">· {co}</span></span><span style="font-size:17px;color:#9C958D" data-small>now</span></div>
<div style="font-size:21px;color:#D9D3CB;margin-top:6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{msg}</div></div></div>'''
L1=6.0; n=len(rows)
lst=''.join(row(r,k) for k,r in enumerate(rows+rows))
steps=[]
for k in range(n+1):
    t0=k/n*100
    steps.append(f"{t0:.3f}%{{transform:translateY({-n*RH+k*RH}px)}}")
    if k<n: steps.append(f"{t0+ (100/n)*0.62:.3f}%{{transform:translateY({-n*RH+k*RH}px)}}")
# move happens in the last 38% of each slot (hold, then slide down one row)
kf="@keyframes feed{"+"".join(steps)+"}"
css1=f'''{kf}.feed{{animation:feed {L1}s cubic-bezier(.3,.8,.3,1) infinite}}
.pulse{{animation:pl {L1/4}s ease-in-out infinite}}@keyframes pl{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}'''
body1=f'''<div style="position:absolute;right:-240px;top:420px;width:900px;height:900px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,90,0,.20),rgba(255,90,0,0))"></div>
<img src="{{{{LOGO}}}}" alt="Cymate" style="position:absolute;left:84px;top:84px;height:30px">
<div class="content" style="left:84px;top:140px;font-family:Poppins,sans-serif;font-weight:300;font-size:72px;letter-spacing:-2.5px;line-height:1;color:#fff">Replies, <b style="font-weight:800;color:#FF6A1A">on repeat.</b></div>
<div class="content" style="left:86px;top:232px;font-family:Inter,sans-serif;font-size:25px;color:#B5AEA6">Your inbox when the outbound is done right.</div>
<div style="position:absolute;left:230px;top:320px;width:620px;height:930px;border-radius:64px;background:#0F0E0D;border:10px solid #22201E;box-shadow:0 0 0 2px #34302C,0 40px 80px rgba(0,0,0,.6);overflow:hidden">
  <div style="position:absolute;left:50%;top:14px;width:120px;height:32px;margin-left:-60px;border-radius:18px;background:#000"></div>
  <div style="position:absolute;left:30px;right:30px;top:66px;display:flex;justify-content:space-between;align-items:center;font-family:Poppins,sans-serif"><span style="font-weight:800;font-size:34px;color:#fff">Inbox</span>
    <span style="display:flex;align-items:center;gap:10px;font-family:Inter,sans-serif;font-weight:600;font-size:19px;color:#FF8A3D"><span class="pulse" style="width:12px;height:12px;border-radius:50%;background:#FF5A00;display:inline-block"></span>Live</span></div>
  <div style="position:absolute;left:24px;right:24px;top:130px;height:{RH*5}px;overflow:hidden">
    <div class="feed">{lst}</div>
    <div style="position:absolute;inset:0 0 auto 0;height:{RH-14}px;border-radius:20px;box-shadow:inset 0 0 0 3px #FF5A00;pointer-events:none"></div>
  </div>
  <div style="position:absolute;left:0;right:0;bottom:0;height:150px;background:linear-gradient(180deg,rgba(15,14,13,0),#0F0E0D 70%)"></div>
</div>'''
pathlib.Path('L01-replies-on-repeat.html').write_text(page('L01',L1,body1,css1,'#0B0A09'))

# ---------- L02: kinetic marquee on burnt orange (4 s) ----------
L2=4.0
def marquee(y,text,fs,direction,style,U):
    fill={'solid':'fill="#140700"','cream':'fill="#FFF1E6"','outline':'fill="none" stroke="#FFF1E6" stroke-width="3"','outline_dark':'fill="none" stroke="#140700" stroke-width="3"'}[style]
    txt=''.join(f'<text x="{i*U}" y="{y}" font-family="Bebas Neue" font-size="{fs}" {fill} textLength="{U-20}" lengthAdjust="spacingAndGlyphs">{text}</text>' for i in range(-1,4))
    anim='mqL' if direction<0 else 'mqR'
    return f'<g style="animation:{anim}{U} {L2}s linear infinite">{txt}</g>', U
rowsdef=[(420,'WARMED INBOXES • VERIFIED LISTS • HUMAN COPY •',220,-1,'cream',1880),(1250,'BOOKED CALLS • BOOKED CALLS •',220,1,'solid',1300)]
g='';kfs=set()
for y,t,fs,d,st,U in rowsdef:
    gg,_=marquee(y,t,fs,d,st,U); g+=gg; kfs.add((U,d))
kf2=''.join(f"@keyframes mqL{U}{{from{{transform:translateX(0)}}to{{transform:translateX(-{U}px)}}}}" if d<0 else f"@keyframes mqR{U}{{from{{transform:translateX(-{U}px)}}to{{transform:translateX(0)}}}}" for U,d in kfs)
body2=f'''<svg style="position:absolute;inset:0" width="{W}" height="{H}">{g}</svg>
<img src="{{{{LOGO}}}}" alt="Cymate" style="position:absolute;left:84px;top:84px;height:30px"><div style="position:absolute;left:90px;right:90px;top:520px;height:470px;border-radius:40px;background:#140700;box-shadow:0 14px 0 #7A2A00;padding:56px 60px;box-sizing:border-box;color:#fff">
  <div style="font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:21px;letter-spacing:5px;color:#C9B7A8">WHAT WE HANDLE</div>
  <div style="margin-top:30px;font-family:Poppins,sans-serif;font-weight:300;font-size:66px;letter-spacing:-2.5px;line-height:1.02">We do the boring parts.<br><b style="font-weight:800;color:#FF7A2E">You take the calls.</b></div>
  <img src="{{{{ICON}}}}" alt="" style="position:absolute;right:52px;top:44px;height:76px">
</div>'''
pathlib.Path('L02-kinetic-marquee.html').write_text(page('L02',L2,body2,kf2,'#C9480C'))

# ---------- L03: reply radar (near-black, 4 s) ----------
L3=4.0; cx,cy,R=540,800,380
blips=[(50,0.78,'Reply · VP Sales'),(128,0.6,'Meeting booked'),(196,0.82,'Reply · Founder'),(255,0.58,'Referral · CFO'),(318,0.8,'Reply · Head of Growth')]
bl=''
for i,(a,rr,lab) in enumerate(blips):
    x=cx+R*rr*math.sin(math.radians(a)); y=cy-R*rr*math.cos(math.radians(a))
    d=a/360*L3; delay=d-L3
    right_side = x > cx
    pos = f'left:{x+26:.0f}px' if right_side else f'right:{W-(x-26):.0f}px'
    bl+=f'''<div class="blip" style="animation-delay:{delay:.3f}s;position:absolute;left:{x-11:.0f}px;top:{y-11:.0f}px;width:22px;height:22px;border-radius:50%;background:#FF6A1A;box-shadow:0 0 0 6px rgba(255,106,26,.25)"></div>
<div class="blip" style="animation-delay:{delay:.3f}s;position:absolute;{pos};top:{y-22:.0f}px;padding:8px 16px;border-radius:999px;background:#FFF1E6;color:#140700;font-family:Inter,sans-serif;font-weight:700;font-size:20px;white-space:nowrap">{lab}</div>'''
wedges=''.join(f'<path d="M{R} {R} L{R} 0 A{R} {R} 0 0 1 {R+R*math.sin(math.radians(sp)):.1f} {R-R*math.cos(math.radians(sp)):.1f} Z" fill="#FF5A00" fill-opacity="{op}" transform="rotate({-sp} {R} {R})"/>' for sp,op in [(10,.35),(22,.18),(40,.09)])
rings=''.join(f'<circle cx="{R}" cy="{R}" r="{R*f:.0f}" fill="none" stroke="#2C2723" stroke-width="2"/>' for f in (.25,.5,.75,1))
css3=f'''.sweep{{position:absolute;left:{cx-R}px;top:{cy-R}px;width:{2*R}px;height:{2*R}px;animation:sw {L3}s linear infinite;transform-origin:50% 50%}}
@keyframes sw{{from{{transform:rotate(0deg)}}to{{transform:rotate(360deg)}}}}
.blip{{animation:bp {L3}s linear infinite;opacity:0}}@keyframes bp{{0%{{opacity:1;transform:scale(1.25)}}8%{{opacity:1;transform:scale(1)}}55%{{opacity:.85}}80%,100%{{opacity:0}}}}'''
body3=f'''<img src="{{{{LOGO}}}}" alt="Cymate" style="position:absolute;left:84px;top:84px;height:30px">
<div class="content" style="left:84px;top:140px;font-family:Poppins,sans-serif;font-weight:300;font-size:66px;letter-spacing:-2.5px;line-height:1.02;color:#fff">Always scanning for<br>people <b style="font-weight:800;color:#FF6A1A">ready to talk.</b></div>
<svg style="position:absolute;left:{cx-R}px;top:{cy-R}px" width="{2*R}" height="{2*R}"><circle cx="{R}" cy="{R}" r="{R}" fill="#121010"/>{rings}<path d="M{R} 0 V{2*R} M0 {R} H{2*R}" stroke="#2C2723" stroke-width="2"/></svg>
<div class="sweep"><svg width="{2*R}" height="{2*R}">{wedges}<line x1="{R}" y1="{R}" x2="{R}" y2="0" stroke="#FF8A3D" stroke-width="4"/></svg></div>
<div style="position:absolute;left:{cx-62}px;top:{cy-62}px;width:124px;height:124px;border-radius:50%;background:#1C1917;border:3px solid #FF5A00;display:flex;align-items:center;justify-content:center;z-index:3"><img src="{{{{ICON}}}}" alt="" style="height:80px"></div>
{bl}
<div class="content" style="left:0;right:0;top:1222px;text-align:center;font-family:Inter,sans-serif;font-size:25px;color:#B5AEA6">Signals, replies and booked calls. Found and handled.</div>'''
pathlib.Path('L03-reply-radar.html').write_text(page('L03',L3,body3,css3,'#0A0909'))

# ---------- L04: hand-drawn boil on paper (3 s, 12 fps) ----------
L4=3.0; random.seed(5)
def wob(pts,j=3,close=False):
    P=pts+([pts[0]] if close else []); out=[]
    for (x1,y1),(x2,y2) in zip(P,P[1:]):
        nn=max(2,int(math.hypot(x2-x1,y2-y1)/18))
        for k in range(nn): t=k/nn; out.append((x1+(x2-x1)*t+random.uniform(-j,j),y1+(y2-y1)*t+random.uniform(-j,j)))
    out.append(P[-1]); return "M"+" L".join(f"{x:.1f} {y:.1f}" for x,y in out)
ECX,ECY,ERX,ERY=540,760,400,300
def ell(j):
    pts=[(ECX+ERX*math.cos(a),ECY+ERY*math.sin(a)) for a in [i*2*math.pi/48 for i in range(48)]]
    return wob(pts,j,True)
PATH=f"M{ECX+ERX} {ECY} A{ERX} {ERY} 0 1 1 {ECX-ERX} {ECY} A{ERX} {ERY} 0 1 1 {ECX+ERX} {ECY} Z"
S='fill="none" stroke="#1A1715" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"'
O='fill="none" stroke="#FF5A00" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"'
def frame_art():
    a=f'<path d="{wob([(60,60),(1020,60),(1020,1290),(60,1290)],4,True)}" {S}/>'
    a+=f'<path d="{ell(4)}" fill="none" stroke="#1A1715" stroke-width="3" stroke-dasharray="14 14" stroke-linecap="round"/>'
    a+=f'<path d="{wob([(150,560),(260,552),(380,566)],3)}" {O}/>'        # under "write it"
    a+=f'<path d="{wob([(700,440),(830,432),(930,446)],3)}" {O}/>'        # under "send it"
    a+=f'<path d="{wob([(620,1176),(800,1168),(980,1180)],3)}" {O}/>'     # under "get the reply"
    return a
boil=''.join(f'<g class="boil" style="animation-delay:{-i*L4/24:.4f}s">{frame_art()}</g>' for i in range(3))
plane=f'''<svg width="120" height="90" viewBox="0 0 120 90"><path d="{wob([(6,46),(112,8),(70,84),(52,56)],2,True)}" fill="#FFFFFF" stroke="#1A1715" stroke-width="4" stroke-linejoin="round"/><path d="{wob([(112,8),(52,56),(46,80)],1.5)}" {S}/></svg>'''
css4=f'''.boil{{opacity:0;animation:bl {L4/8}s steps(1) infinite}}@keyframes bl{{0%{{opacity:1}}33.33%,100%{{opacity:0}}}}
.plane{{position:absolute;left:0;top:0;width:120px;height:90px;offset-path:path('{PATH}');offset-rotate:auto 0deg;animation:fly {L4}s steps(36) infinite;z-index:4}}
@keyframes fly{{from{{offset-distance:0%}}to{{offset-distance:100%}}}}
.hw{{position:absolute;font-family:Caveat,'Permanent Marker',cursive;font-weight:700;color:#1A1715;z-index:5}}'''
body4=f'''<svg style="position:absolute;inset:0;z-index:2" width="{W}" height="{H}">{boil}</svg>
<img src="{{{{LOGO_DARK}}}}" alt="Cymate" style="position:absolute;left:110px;top:120px;height:30px;z-index:5">
<div class="hw" style="left:110px;top:170px;font-size:92px;line-height:.95;width:860px">Cold email isn’t magic.<br>It’s a <span style="color:#D94600">loop.</span></div>
<div class="hw" style="left:150px;top:480px;font-size:70px;transform:rotate(-4deg)">write it</div>
<div class="hw" style="left:700px;top:362px;font-size:70px;transform:rotate(3deg)">send it</div>
<div class="hw" style="left:620px;top:1096px;font-size:70px;transform:rotate(-2deg)">get the reply</div>
<img src="{{{{MASCOT}}}}" alt="" style="position:absolute;left:{ECX-130}px;top:{ECY-112}px;width:260px;z-index:3">
<div class="plane">{plane}</div>'''
pathlib.Path('L04-handdrawn-loop.html').write_text(page('L04',L4,body4,css4,'#F6EFE4'))
print('ok')
