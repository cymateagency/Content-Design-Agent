import pathlib
W,H=1080,1350
L,T,R,B,RAD=110,400,970,1100,90     # conveyor loop (centre line)
D=(f"M{L+RAD} {T} H{R-RAD} A{RAD} {RAD} 0 0 1 {R} {T+RAD} V{B-RAD} A{RAD} {RAD} 0 0 1 {R-RAD} {B} "
   f"H{L+RAD} A{RAD} {RAD} 0 0 1 {L} {B-RAD} V{T+RAD} A{RAD} {RAD} 0 0 1 {L+RAD} {T} Z")
LOOP=3.0; N=9
INK='#1A1715'; PAPER='#FBF6EF'; CREAM='#F3EADF'; OR='#FF5A00'
env=''.join(f'''<div class="env" style="animation:mv{k} {LOOP}s linear infinite"><svg width="56" height="40" viewBox="0 0 56 40"><rect x="2" y="2" width="52" height="36" rx="5" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/><path d="M4 5 L28 22 L52 5" fill="none" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/><circle cx="28" cy="22" r="6" fill="{OR}" stroke="{INK}" stroke-width="2"/></svg></div>''' for k in range(N))
kf=''.join(f"@keyframes mv{k}{{from{{offset-distance:{k*100/N:.4f}%}}to{{offset-distance:{(k+1)*100/N:.4f}%}}}}" for k in range(N))
def icon(kind):
    I={'inbox':'<path d="M3 13l3-8h12l3 8v6H3z"/><path d="M3 13h5l1.5 2.5h5L16 13h5"/>',
       'list':'<path d="M9 6h12M9 12h12M9 18h12"/><path d="M3.5 6l1.2 1.2L7 5M3.5 12l1.2 1.2L7 11M3.5 18l1.2 1.2L7 17"/>',
       'pen':'<path d="M4 20l1-4L16 5l3 3L8 19z"/><path d="M14 7l3 3"/>',
       'send':'<path d="M21 3L10 14"/><path d="M21 3l-7 18-4-7-7-4z"/>',
       'reply':'<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/>',
       'cal':'<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4M9 15l2 2 4-4"/>'}[kind]
    return f'<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{I}</svg>'
def station(n,title,desc,kind,cx,cy,blink):
    return f'''<div class="st" style="left:{cx-118}px;top:{cy-78}px">
  <div class="num">{n}</div><div class="ic">{icon(kind)}</div>
  <div class="tt">{title}</div><div class="ds">{desc}</div>
  <span class="lamp" style="animation-delay:{blink}s"></span></div>'''
st=''.join([
 station(1,'Inboxes','warmed up first','inbox',290,T,0),
 station(2,'List Lab','verified, on-ICP','list',540,T,.5),
 station(3,'Copy Desk','one idea, one ask','pen',790,T,1.0),
 station(4,'Send Queue','spread across inboxes','send',894,750,.25),
 station(5,'Reply Desk','every reply handled','reply',740,B,.75),
 station(6,'Booked','calls on your calendar','cal',340,B,1.25),
])
html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Cymate GIF: Outbound Factory</title>
<meta name="gif-loop" content="{LOOP}"><meta name="still-time" content="0">
{{{{BASE_CSS}}}}
<style>
/* LOOPING GIF TEMPLATE: everything repeats every {LOOP}s (envelopes move one slot, belt slides one dash, lamps blink twice).
   Flat colours only (GIF palette), no film grain. Render with scripts/make_gif.py. */
.stage{{position:absolute;inset:0;background:{CREAM}}}
.floor{{position:absolute;left:40px;right:40px;top:300px;bottom:150px;border-radius:44px;background:{PAPER};border:3px solid {INK};box-shadow:0 10px 0 #E2D3C2}}
.env{{position:absolute;left:0;top:0;width:56px;height:40px;offset-path:path('{D}');offset-rotate:0deg;z-index:3}}
.st{{position:absolute;width:236px;height:156px;box-sizing:border-box;padding:20px 20px 16px 20px;border-radius:24px;background:#FFFFFF;border:3px solid {INK};box-shadow:0 8px 0 {INK};z-index:5;font-family:Inter,Arial,sans-serif;color:{INK}}}
.st .num{{position:absolute;left:-16px;top:-16px;width:42px;height:42px;border-radius:50%;background:{OR};border:3px solid {INK};color:{INK};font-family:Poppins,sans-serif;font-weight:800;font-size:21px;display:flex;align-items:center;justify-content:center}}
.st .ic{{position:absolute;right:18px;top:16px}}
.st .tt{{font-family:Poppins,sans-serif;font-weight:800;font-size:27px;letter-spacing:-.5px;margin-top:2px}}
.st .ds{{font-size:19px;line-height:1.25;color:#55524E;margin-top:6px;width:200px}}
.st .lamp{{position:absolute;right:18px;bottom:16px;width:14px;height:14px;border-radius:50%;background:#2BC46A;border:2px solid {INK};animation:lamp {LOOP/2}s steps(1) infinite}}
@keyframes lamp{{0%{{background:#2BC46A}}50%{{background:#D9F5E4}}}}
.belt{{animation:belt {LOOP/2}s linear infinite}}
@keyframes belt{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-44}}}}
.bob{{animation:bob {LOOP}s ease-in-out infinite}}
@keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-10px)}}}}
.ping{{animation:ping {LOOP}s ease-out infinite}}
@keyframes ping{{0%{{transform:scale(.6);opacity:0}}12%{{opacity:1}}40%{{transform:scale(1);opacity:1}}85%,100%{{transform:scale(1);opacity:0}}}}
{kf}
</style></head><body>
<div class="cm paper" style="width:{W}px;height:{H}px">
<div class="stage"></div>
<img src="{{{{LOGO_DARK}}}}" alt="Cymate" style="position:absolute;left:84px;top:84px;height:30px;z-index:6">
<div style="position:absolute;right:84px;top:80px;z-index:6;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:19px;letter-spacing:4px;color:#55524E">HOW WE RUN OUTBOUND</div>
<div class="content" style="left:84px;right:84px;top:138px;z-index:6;font-family:Poppins,sans-serif;font-weight:300;font-size:62px;letter-spacing:-2px;line-height:1;white-space:nowrap;color:{INK}">Inside the <b style="font-weight:800;color:#D94600">Outbound Factory</b></div>
<div class="content" style="left:86px;top:224px;z-index:6;font-family:Inter,sans-serif;font-size:24px;color:#55524E">Six stations. One loop. Every week.</div>
<div class="floor"></div>
<svg style="position:absolute;inset:0;z-index:2" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <path d="{D}" fill="none" stroke="{INK}" stroke-width="66" stroke-linejoin="round"/>
  <path d="{D}" fill="none" stroke="#3B3430" stroke-width="54" stroke-linejoin="round"/>
  <path class="belt" d="{D}" fill="none" stroke="#5A4F48" stroke-width="54" stroke-dasharray="6 16" stroke-linejoin="round"/>
</svg>
{env}
{st}
<!-- centre: the team -->
<div style="position:absolute;left:330px;top:600px;width:420px;height:300px;border-radius:30px;background:#FFFFFF;border:3px solid {INK};box-shadow:0 8px 0 {INK};z-index:4"></div>
<img class="bob" src="{{{{MASCOT}}}}" alt="" style="position:absolute;left:452px;top:612px;width:176px;z-index:5">
<div style="position:absolute;left:330px;width:420px;top:800px;text-align:center;z-index:5;font-family:Poppins,sans-serif;font-weight:800;font-size:26px;color:{INK}">Your Cymate team</div>
<div style="position:absolute;left:330px;width:420px;top:840px;text-align:center;z-index:5;font-family:Inter,sans-serif;font-size:19px;color:#55524E">runs every station for you</div>
<div class="ping" style="position:absolute;left:470px;top:1035px;z-index:6;transform-origin:center"><span style="display:inline-block;padding:6px 14px;border-radius:999px;background:{OR};border:3px solid {INK};color:{INK};font-family:Poppins,sans-serif;font-weight:800;font-size:20px">+1 booked</span></div>
<div style="position:absolute;left:0;right:0;top:1222px;text-align:center;z-index:6"><span style="display:inline-flex;align-items:center;gap:12px;padding:16px 30px;border-radius:999px;background:{INK};color:#fff;font-family:Poppins,sans-serif;font-weight:600;font-size:24px">Want the factory running for you? <span style="color:{OR}">Link in comments</span></span></div>
</div></body></html>'''
pathlib.Path('g01.html').write_text(html)
