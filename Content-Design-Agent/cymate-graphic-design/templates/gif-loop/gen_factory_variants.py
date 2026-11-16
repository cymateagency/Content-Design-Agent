import math, pathlib
W,H=1080,1350; LOOP=3.0
THEMES={
 'dark':  dict(bg='#0E0D0C', floor='#161412', floorline='#2E2A26', fshadow='#000000', card='#1E1B19', cardline='#3A342F', cshadow='#000000', text='#FFFFFF', sub='#B5AEA6',
               belt_out='#000000', belt='#262220', belt_dash='#4A3F38', env='#FFFFFF', envline='#0E0D0C', title='#FFFFFF', accent='#FF6A1A', kicker='#B5AEA6', lamp_on='#FF6A1A', lamp_off='#3A2A20', cta_bg='#FF5A00', cta_fg='#140700', cta_acc='#140700', logo='LOGO', centre='#1E1B19', badge_fg='#140700'),
 'orange':dict(bg='#C9480C', floor='#D9561A', floorline='#140700', fshadow='#8E3006', card='#FFF6EC', cardline='#140700', cshadow='#140700', text='#140700', sub='#5E4A3C',
               belt_out='#140700', belt='#2B1A10', belt_dash='#5B3A26', env='#FFFFFF', envline='#140700', title='#FFFFFF', accent='#140700', kicker='#FFFFFF', lamp_on='#2BC46A', lamp_off='#D9F5E4', cta_bg='#140700', cta_fg='#FFFFFF', cta_acc='#FFB27A', logo='LOGO', centre='#FFF6EC', badge_fg='#140700'),
 'champ': dict(bg='#111111', floor='#181818', floorline='#2C2C2C', fshadow='#000000', card='#1C1C1C', cardline='#FF5A00', cshadow='#000000', text='#FFFFFF', sub='#ADA79F',
               belt_out='#000000', belt='#232323', belt_dash='#FF5A00', env='#FFFFFF', envline='#111111', title='#FFFFFF', accent='#FF6A1A', kicker='#ADA79F', lamp_on='#FF6A1A', lamp_off='#3A2A20', cta_bg='#FFFFFF', cta_fg='#111111', cta_acc='#B83A00', logo='LOGO', centre='#1C1C1C', badge_fg='#140700'),
 'paper': dict(bg='#F3EADF', floor='#FBF6EF', floorline='#1A1715', fshadow='#E2D3C2', card='#FFFFFF', cardline='#1A1715', cshadow='#1A1715', text='#1A1715', sub='#55524E',
               belt_out='#1A1715', belt='#3B3430', belt_dash='#5A4F48', env='#FFFFFF', envline='#1A1715', title='#1A1715', accent='#D94600', kicker='#55524E', lamp_on='#2BC46A', lamp_off='#D9F5E4', cta_bg='#1A1715', cta_fg='#FFFFFF', cta_acc='#FF7A33', logo='LOGO_DARK', centre='#FFFFFF', badge_fg='#1A1715'),
}
STATIONS=[('Inboxes','warmed up first','inbox'),('List Lab','verified, on-ICP','list'),('Copy Desk','one idea, one ask','pen'),
          ('Send Queue','spread across inboxes','send'),('Reply Desk','every reply handled','reply'),('Booked','calls on your calendar','cal')]
def icon(kind,col):
    I={'inbox':'<path d="M3 13l3-8h12l3 8v6H3z"/><path d="M3 13h5l1.5 2.5h5L16 13h5"/>','list':'<path d="M9 6h12M9 12h12M9 18h12"/><path d="M3.5 6l1.2 1.2L7 5M3.5 12l1.2 1.2L7 11M3.5 18l1.2 1.2L7 17"/>',
       'pen':'<path d="M4 20l1-4L16 5l3 3L8 19z"/><path d="M14 7l3 3"/>','send':'<path d="M21 3L10 14"/><path d="M21 3l-7 18-4-7-7-4z"/>',
       'reply':'<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/>','cal':'<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4M9 15l2 2 4-4"/>'}[kind]
    return f'<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{I}</svg>'
def rect_path(L,T,R,B,RAD): return (f"M{L+RAD} {T} H{R-RAD} A{RAD} {RAD} 0 0 1 {R} {T+RAD} V{B-RAD} A{RAD} {RAD} 0 0 1 {R-RAD} {B} H{L+RAD} A{RAD} {RAD} 0 0 1 {L} {B-RAD} V{T+RAD} A{RAD} {RAD} 0 0 1 {L+RAD} {T} Z")
def ring_path(cx,cy,r): return f"M{cx} {cy-r} A{r} {r} 0 1 1 {cx} {cy+r} A{r} {r} 0 1 1 {cx} {cy-r} Z"

def scene(name, th, D, N, positions, centre, title_html, sub, kicker, floor_box, extra_bg='', size=(W,H), cta_top=1222, card_w=236, sub_top=226, cta_fs=24):
    t=THEMES[th]; w,h=size
    env=''.join(f'<div class="env" style="animation:mv{k} {LOOP}s linear infinite"><svg width="54" height="38" viewBox="0 0 56 40"><rect x="2" y="2" width="52" height="36" rx="5" fill="{t["env"]}" stroke="{t["envline"]}" stroke-width="3"/><path d="M4 5 L28 22 L52 5" fill="none" stroke="{t["envline"]}" stroke-width="3" stroke-linejoin="round"/><circle cx="28" cy="22" r="6" fill="#FF5A00" stroke="{t["envline"]}" stroke-width="2"/></svg></div>' for k in range(N))
    kf=''.join(f"@keyframes mv{k}{{from{{offset-distance:{k*100/N:.4f}%}}to{{offset-distance:{(k+1)*100/N:.4f}%}}}}" for k in range(N))
    st=''
    for i,((tt,ds,ic),(cx,cy)) in enumerate(zip(STATIONS,positions)):
        st+=f'''<div class="st" style="left:{cx-card_w/2:.0f}px;top:{cy-78:.0f}px"><div class="num">{i+1}</div><div class="ic">{icon(ic,t["text"])}</div><div class="tt">{tt}</div><div class="ds">{ds}</div><span class="lamp" style="animation-delay:{(i*0.25)%1.5:.2f}s"></span></div>'''
    fl,ft,fr,fb,frad=floor_box
    html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{name}</title><meta name="gif-loop" content="{LOOP}"><meta name="still-time" content="0">{{{{BASE_CSS}}}}
<style>
.env{{position:absolute;left:0;top:0;width:54px;height:38px;offset-path:path('{D}');offset-rotate:0deg;z-index:3}}
.st{{position:absolute;width:{card_w}px;height:156px;box-sizing:border-box;padding:20px;border-radius:24px;background:{t["card"]};border:3px solid {t["cardline"]};box-shadow:0 8px 0 {t["cshadow"]};z-index:5;font-family:Inter,Arial,sans-serif;color:{t["text"]}}}
.st .num{{position:absolute;left:-16px;top:-16px;width:42px;height:42px;border-radius:50%;background:#FF5A00;border:3px solid {t["cardline"] if th!='champ' else '#000'};color:{t["badge_fg"]};font-family:Poppins,sans-serif;font-weight:800;font-size:21px;display:flex;align-items:center;justify-content:center}}
.st .ic{{position:absolute;right:18px;top:16px}}
.st .tt{{font-family:Poppins,sans-serif;font-weight:800;font-size:27px;letter-spacing:-.5px;margin-top:2px}}
.st .ds{{font-size:19px;line-height:1.25;color:{t["sub"]};margin-top:6px;width:{card_w-36}px}}
.st .lamp{{position:absolute;right:18px;bottom:16px;width:14px;height:14px;border-radius:50%;border:2px solid {t["cardline"] if th!='champ' else '#000'};animation:lamp {LOOP/2}s steps(1) infinite}}
@keyframes lamp{{0%{{background:{t["lamp_on"]}}}50%{{background:{t["lamp_off"]}}}}}
.belt{{animation:belt {LOOP/2}s linear infinite}}@keyframes belt{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-44}}}}
.bob{{animation:bob {LOOP}s ease-in-out infinite}}@keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-10px)}}}}
.ping{{animation:ping {LOOP}s ease-out infinite}}@keyframes ping{{0%{{transform:scale(.6);opacity:0}}12%{{opacity:1}}40%{{transform:scale(1);opacity:1}}85%,100%{{transform:scale(1);opacity:0}}}}
{kf}
</style></head><body>
<div class="cm" style="width:{w}px;height:{h}px;background:{t["bg"]};color:{t["text"]}">
{extra_bg}
<img src="{{{{{t["logo"]}}}}}" alt="Cymate" style="position:absolute;left:84px;top:84px;height:30px;z-index:6">
<div style="position:absolute;right:84px;top:80px;z-index:6;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:19px;letter-spacing:4px;color:{t["kicker"]}">{kicker}</div>
<div class="content" style="left:84px;right:84px;top:138px;z-index:6;white-space:nowrap;color:{t["title"]}">{title_html}</div>
<div class="content" style="left:86px;top:{sub_top}px;z-index:6;font-family:Inter,sans-serif;font-size:24px;color:{t["kicker"]}">{sub}</div>
<div style="position:absolute;left:{fl}px;top:{ft}px;width:{fr-fl}px;height:{fb-ft}px;border-radius:{frad}px;background:{t["floor"]};border:3px solid {t["floorline"]};box-shadow:0 10px 0 {t["fshadow"]}"></div>
<svg style="position:absolute;inset:0;z-index:2" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <path d="{D}" fill="none" stroke="{t["belt_out"]}" stroke-width="66" stroke-linejoin="round"/>
  <path d="{D}" fill="none" stroke="{t["belt"]}" stroke-width="54" stroke-linejoin="round"/>
  <path class="belt" d="{D}" fill="none" stroke="{t["belt_dash"]}" stroke-width="54" stroke-dasharray="6 16" stroke-linejoin="round" {'stroke-opacity=".55"' if th=='champ' else ''}/>
</svg>
{env}{st}{centre.format(**t)}
<div style="position:absolute;left:0;right:0;top:{cta_top}px;text-align:center;z-index:6"><span style="display:inline-flex;align-items:center;gap:12px;padding:16px 30px;border-radius:999px;background:{t["cta_bg"]};color:{t["cta_fg"]};font-family:Poppins,sans-serif;font-weight:600;font-size:{cta_fs}px">Want the factory running for you? <span style="color:{t["cta_acc"]}">Link in comments</span></span></div>
</div></body></html>'''
    pathlib.Path(name+'.html').write_text(html)

TITLE=lambda t: f'<span style="font-family:Poppins,sans-serif;font-weight:300;font-size:62px;letter-spacing:-2px">Inside the <b style="font-weight:800;color:{THEMES[t]["accent"]}">Outbound Factory</b></span>'
CENTRE_BOX='''<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:30px;background:{{centre}};border:3px solid {{cardline}};box-shadow:0 8px 0 {{cshadow}};z-index:4"></div>
<img class="bob" src="{{{{{{{{MASCOT}}}}}}}}" alt="" style="position:absolute;left:{mx}px;top:{my}px;width:{mw}px;z-index:5">
<div style="position:absolute;left:{x}px;width:{w}px;top:{ty}px;text-align:center;z-index:5;font-family:Poppins,sans-serif;font-weight:800;font-size:26px;color:{{text}}">Your Cymate team</div>
<div style="position:absolute;left:{x}px;width:{w}px;top:{sy}px;text-align:center;z-index:5;font-family:Inter,sans-serif;font-size:19px;color:{{sub}}">runs every station for you</div>'''
def centre(x,y,w,h,mw,ping):
    mx=x+(w-mw)//2; my=y+14; ty=my+int(mw*0.86)+14; sy=ty+40
    c=CENTRE_BOX.format(x=x,y=y,w=w,h=h,mx=mx,my=my,mw=mw,ty=ty,sy=sy)
    px,py=ping
    return c+f'<div class="ping" style="position:absolute;left:{px}px;top:{py}px;z-index:6"><span style="display:inline-block;padding:6px 14px;border-radius:999px;background:#FF5A00;border:3px solid #140700;color:#140700;font-family:Poppins,sans-serif;font-weight:800;font-size:20px">+1 booked</span></div>'

# G02 dark night shift: same rounded-rect factory, dark
L,T,R,B=110,400,970,1100
scene('G02-factory-dark','dark',rect_path(L,T,R,B,90),9,[(290,T),(540,T),(790,T),(894,750),(740,B),(340,B)],
      centre(330,600,420,300,176,(470,1035)),TITLE('dark'),'Six stations. One loop. Every week.','HOW WE RUN OUTBOUND',(40,300,1040,1200,44))
# G03 orange ring: stations around a circle
cx,cy,r=540,770,330
pos=[(cx+r*math.cos(math.radians(a)),cy+r*math.sin(math.radians(a))*1.0) for a in (-90,-30,30,90,150,210)]
pos=[(round(x),round(y)) for x,y in pos]
scene('G03-factory-ring-orange','orange',ring_path(cx,cy,r),7,pos,
      centre(395,655,290,230,140,(470,912)),TITLE('orange').replace('color:#140700">Outbound','color:#140700">Outbound'),'One loop, running every week.','HOW WE RUN OUTBOUND',(40,300,1040,1200,44))
# G04 champions dark: horizontal stadium track, Bebas title, static speed streaks
import random; random.seed(7)
streaks=''.join(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+math.cos(math.radians(-58))*Lg:.0f}" y2="{y+math.sin(math.radians(-58))*Lg:.0f}" stroke="{c}" stroke-opacity="{o:.2f}" stroke-width="{wd:.0f}" stroke-linecap="round"/>'
  for x,y,Lg,c,o,wd in [(random.uniform(-300,1100),random.uniform(200,1700),random.uniform(300,900),random.choice(['#2A2A2A','#333333','#FF5A00']),random.uniform(.25,.6),random.uniform(2,14)) for _ in range(40)])
bg=f'<svg style="position:absolute;inset:0;z-index:0" width="{W}" height="{H}">{streaks}</svg>'
PL,PT,PR,PB=150,560,930,980
pr=(PB-PT)//2
D=f"M{PL+pr} {PT} H{PR-pr} A{pr} {pr} 0 0 1 {PR-pr} {PB} H{PL+pr} A{pr} {pr} 0 0 1 {PL+pr} {PT} Z"
champ_title='<span style="font-family:\'Bebas Neue\',sans-serif;font-size:96px;letter-spacing:1px;line-height:1;background:linear-gradient(90deg,#FFFFFF 0%,#FFD2B0 45%,#FF6A10 100%);-webkit-background-clip:text;background-clip:text;color:transparent">THE OUTBOUND FACTORY</span>'
scene('G04-factory-champions','champ',D,7,[(300,PT),(540,PT),(780,PT),(780,PB),(540,PB),(300,PB)],
      centre(395,650,290,240,150,(476,1110)),champ_title,'Six stations. One loop. Built for champions.','HOW WE RUN OUTBOUND',(40,330,1040,1190,44),extra_bg=bg,sub_top=246)
# G05 light, square 1080x1080, ring with grid
grid='<svg style="position:absolute;inset:0;z-index:0" width="1080" height="1080"><defs><pattern id="g" width="60" height="60" patternUnits="userSpaceOnUse"><path d="M60 0H0V60" fill="none" stroke="#E4D9CB" stroke-width="1.5"/></pattern></defs><rect width="1080" height="1080" fill="url(#g)"/></svg>'
SL,ST,SR,SB=150,430,930,820
sr=(SB-ST)//2
D5=f"M{SL+sr} {ST} H{SR-sr} A{sr} {sr} 0 0 1 {SR-sr} {SB} H{SL+sr} A{sr} {sr} 0 0 1 {SL+sr} {ST} Z"
scene('G05-factory-square-light','paper',D5,6,[(300,ST),(540,ST),(780,ST),(780,SB),(540,SB),(300,SB)],
      '<img class="bob" src="{{{{MASCOT}}}}" alt="" style="position:absolute;left:470px;top:548px;width:140px;z-index:5"><div class="ping" style="position:absolute;left:610px;top:560px;z-index:6"><span style="display:inline-block;padding:6px 14px;border-radius:999px;background:#FF5A00;border:3px solid #140700;color:#140700;font-family:Poppins,sans-serif;font-weight:800;font-size:20px">+1 booked</span></div>',TITLE('paper').replace('font-size:62px','font-size:56px'),'Six stations. One loop.','HOW WE RUN OUTBOUND',(40,300,1040,935,40),extra_bg=grid,size=(1080,1080),cta_top=958,card_w=220,cta_fs=22)
print('ok')
