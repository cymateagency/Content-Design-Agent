import pathlib
def frame(title, cls, body, bg=""):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title>{{{{BASE_CSS}}}}
<style>
.note{{position:absolute;box-sizing:border-box;border-radius:28px;padding:22px 26px;font-family:Inter,Arial,sans-serif;color:#fff;background:linear-gradient(135deg,rgba(255,255,255,.13),rgba(255,255,255,.05));border:1px solid rgba(255,255,255,.18);backdrop-filter:blur(18px);box-shadow:0 40px 80px rgba(0,0,0,.55),0 8px 18px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.22)}}
.mono{{font-family:'IBM Plex Mono',monospace;font-weight:600;letter-spacing:5px}}
.key{{position:relative;width:330px;height:300px;border-radius:44px;background:linear-gradient(160deg,#FF9A3D 0%,#FF6A00 45%,#E04E00 100%);box-shadow:0 46px 70px rgba(120,40,0,.32),0 16px 26px rgba(120,40,0,.28),inset 0 -14px 0 rgba(150,45,0,.45),inset 0 4px 2px rgba(255,220,180,.6)}}
.key .top{{position:absolute;left:34px;right:34px;top:22px;bottom:52px;border-radius:30px;background:linear-gradient(170deg,#FFB061 0%,#FF7A1A 55%,#FF6A00 100%);box-shadow:inset 0 2px 1px rgba(255,235,210,.8),inset 0 -6px 14px rgba(190,60,0,.35),0 8px 14px rgba(160,50,0,.25)}}
.key .lbl{{position:absolute;left:30px;top:24px;font-family:Inter,Arial,sans-serif;font-size:44px;font-weight:500;color:#2A1505}}
</style></head><body>
<div class="cm {cls}" style="width:2560px;height:1440px;{bg}">
{body}
</div></body></html>'''

V={}
# B02 — object pun on paper
V['B02-paper-reply-key']=frame('B02','paper',r'''
<svg class="tx" width="2560" height="1440" style="opacity:.55"><defs><pattern id="g" width="96" height="96" patternUnits="userSpaceOnUse"><path d="M96 0H0V96" fill="none" stroke="#DCD8D0" stroke-width="1.2"/></pattern></defs><rect width="2560" height="1440" fill="url(#g)"/></svg>
<div style="position:absolute;left:1500px;top:300px;width:1100px;height:900px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,140,60,.16),rgba(255,140,60,0))"></div>
<img src="{{MASCOT}}" alt="" style="position:absolute;left:560px;top:560px;height:150px;z-index:3;filter:drop-shadow(0 18px 22px rgba(10,12,20,.25))">
<img src="{{LOGO_DARK}}" alt="Cymate" style="position:absolute;left:560px;top:760px;height:52px;z-index:3">
<div class="content" style="left:560px;top:836px;z-index:3;font-family:Inter,sans-serif;font-size:26px;font-weight:500;color:#55524E;width:420px;line-height:1.35">Cold outbound, done for you.</div>
<div style="position:absolute;left:1020px;top:520px;width:2px;height:400px;background:#D8D3CA;z-index:2"></div>
<div class="content" style="left:1090px;top:556px;z-index:3;font-family:'Archivo Black',Poppins,sans-serif;font-size:96px;line-height:.92;letter-spacing:-2.5px;color:#0A0C14;text-transform:uppercase">Outbound<br>that gets a</div>
<div class="key" style="position:absolute;left:1790px;top:560px;transform:rotate(-5deg);z-index:4;width:236px;height:214px;border-radius:34px"><div class="top" style="left:26px;right:26px;top:16px;bottom:40px;border-radius:24px"><div class="lbl" style="font-size:36px;left:22px;top:18px">Reply</div></div></div>
<div class="content mono" style="left:1092px;top:800px;z-index:3;font-size:22px;color:#55524E">INFRASTRUCTURE · LISTS · COPY</div>
''')
# B03 — seamless REPLIEEEES ribbon on paper
import math, random
pts=[]; 
for k in range(0,2761,20):
    x=k-100; y=800+45*math.sin(k/260)
    pts.append((x,y))
D="M"+" L".join(f"{x:.0f} {y:.1f}" for x,y in pts)
V['B03-ribbon-repliees']=frame('B03','paper',f'''
<div style="position:absolute;left:-300px;top:200px;width:1400px;height:1000px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,150,90,.18),rgba(255,150,90,0))"></div>
<img src="{{{{LOGO_DARK}}}}" alt="Cymate" style="position:absolute;left:560px;top:536px;height:46px;z-index:5">
<div class="content mono" style="left:562px;top:604px;z-index:5;font-size:22px;color:#55524E">WE FILL INBOXES WITH</div>
<svg style="position:absolute;left:0;top:0;z-index:3" width="2560" height="1440" viewBox="0 0 2560 1440">
 <defs><linearGradient id="rg" x1="0" x2="1"><stop offset="0" stop-color="#E23A00"/><stop offset=".5" stop-color="#FF5A00"/><stop offset="1" stop-color="#FF7A2E"/></linearGradient>
 <filter id="ls" x="-5%" y="-30%" width="110%" height="160%"><feDropShadow dx="0" dy="10" stdDeviation="9" flood-color="#7A2A00" flood-opacity=".22"/></filter><path id="rp" d="{D}"/></defs>
 <text font-family="Poppins" font-weight="800" font-size="140" fill="url(#rg)" filter="url(#ls)"><textPath href="#rp" startOffset="660" textLength="1180" lengthAdjust="spacing">REPLIEEEEEEES</textPath></text>
 <text font-family="Poppins" font-weight="800" font-size="150" fill="url(#rg)" filter="url(#ls)" opacity=".18"><textPath href="#rp" startOffset="1900" textLength="900" lengthAdjust="spacing">EEEEEEEE</textPath><textPath href="#rp" startOffset="0" textLength="560" lengthAdjust="spacing">EEEEE</textPath></text>
</svg>
<img src="{{{{MASCOT}}}}" alt="" style="position:absolute;left:1820px;top:{800+45*math.sin((1860+100)/260)-150:.0f}px;height:190px;z-index:4;transform:rotate({math.degrees(math.atan(45/260*math.cos((1860+100)/260))):.0f}deg);filter:drop-shadow(0 18px 18px rgba(90,30,0,.28))">
<div class="content" style="left:562px;top:878px;z-index:5;font-family:Inter,sans-serif;font-size:27px;font-weight:600;color:#0A0C14">Cold outbound, done for you. <span style="color:#55524E;font-weight:500">Infrastructure, lists, copy and replies.</span></div>
''')
# B04 — spec sheet
V['B04-spec-system']=frame('B04','haze-none',r'''
<div class="tx tx-grid" style="opacity:.5"></div>
<div style="position:absolute;left:300px;top:700px;width:900px;height:110px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,110,40,.7),rgba(255,90,0,0));filter:blur(8px)"></div>
<div style="position:absolute;left:1300px;top:860px;width:1300px;height:90px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,170,120,.6),rgba(255,90,0,0));filter:blur(6px)"></div>
<div style="position:absolute;left:1500px;top:400px;width:900px;height:700px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,90,0,.22),rgba(255,90,0,0))"></div>
<div style="position:absolute;left:1210px;top:568px;width:500px;padding:24px 28px;box-sizing:border-box;border-radius:26px;background:linear-gradient(180deg,#FFFFFF,#F2EFEC);color:#15171C;font-family:Inter,sans-serif;transform:perspective(1400px) rotateY(-14deg) rotateZ(-4deg);box-shadow:0 50px 90px rgba(0,0,0,.6),0 12px 20px rgba(0,0,0,.35);z-index:3">
  <div style="font-weight:700;font-size:26px">quick question, Alex</div>
  <div style="margin-top:10px;font-size:21px;line-height:1.45;color:#3E3B37">Saw you opened two new regions. Worth a look at how others fill that pipeline fast?</div></div>
<div style="position:absolute;left:1180px;top:536px;width:580px;height:290px;border:2px solid rgba(255,255,255,.85);z-index:4"></div>
<svg style="position:absolute;inset:0;z-index:5" width="2560" height="1440"><g fill="#fff"><rect x="1173" y="529" width="14" height="14"/><rect x="1753" y="529" width="14" height="14"/><rect x="1173" y="819" width="14" height="14"/><rect x="1753" y="819" width="14" height="14"/><rect x="1463" y="529" width="14" height="14"/><rect x="1463" y="819" width="14" height="14"/></g>
<g fill="none" stroke="#fff" stroke-width="2"><path d="M1700 640 L1790 600 H1810"/><circle cx="1700" cy="640" r="5" fill="#fff"/></g></svg>
<div class="content" style="left:1818px;top:578px;z-index:5;color:#fff;font-family:Inter,sans-serif;width:200px"><div style="font-weight:600;font-size:24px">HUMAN COPY</div><div data-small style="font-size:16px;letter-spacing:.6px;color:rgba(255,255,255,.7);margin-top:4px">ONE IDEA, ONE ASK</div></div>
<div class="content" style="left:560px;top:540px;z-index:5;color:#fff;font-family:Inter,sans-serif">
  <img src="{{LOGO}}" alt="Cymate" style="height:34px;display:block;margin-bottom:8px">
  <div style="font-family:Poppins,sans-serif;font-size:104px;font-weight:300;line-height:.95;letter-spacing:-2px">OUTBOUND</div>
  <div style="margin-top:6px;display:flex;align-items:baseline;gap:22px"><span style="font-size:30px;font-weight:300;letter-spacing:2px">SYSTEM</span><span class="grad-text" style="font-family:Poppins,sans-serif;font-size:104px;font-weight:700;line-height:.95">0001</span></div>
  <div style="margin-top:22px;border-top:2px solid rgba(255,255,255,.5);padding-top:14px;font-size:19px;letter-spacing:1.2px;color:rgba(255,255,255,.8);white-space:nowrap"><b>BUILT ON :</b>&nbsp; WARMED INBOXES · VERIFIED LISTS</div>
</div>
<img src="{{ICON}}" alt="" style="position:absolute;left:2140px;top:760px;height:90px;z-index:5;opacity:.9">
''', 'background:radial-gradient(80% 60% at 55% 50%,#1C1C1E 0%,#0F0F10 55%,#070707 100%)')
# B05 — burnt orange, stacked logo, bold type
V['B05-orange-stacked']=frame('B05','orange',r'''
<div class="tx tx-dots" style="opacity:.25"></div>
<div style="position:absolute;left:1600px;top:-200px;width:1400px;height:1100px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,200,150,.30),rgba(255,200,150,0))"></div>
<div style="position:absolute;left:-300px;top:700px;width:1200px;height:900px;border-radius:50%;background:radial-gradient(closest-side,rgba(60,10,0,.35),rgba(60,10,0,0))"></div>
<img src="{{LOCKUP}}" alt="Cymate" style="position:absolute;left:580px;top:560px;height:330px;z-index:4;filter:drop-shadow(0 26px 36px rgba(60,15,0,.45))">
<div class="content" style="left:1060px;top:560px;z-index:4;color:#fff">
  <div style="font-family:Poppins,sans-serif;font-weight:300;font-size:104px;letter-spacing:-3.5px;line-height:1">Cold email that</div>
  <div style="font-family:Poppins,sans-serif;font-weight:800;font-size:104px;letter-spacing:-3.5px;line-height:1;color:#140700">books meetings.</div>
  <div class="mono" style="margin-top:30px;font-size:24px;color:#1A0900">INFRASTRUCTURE · LISTS · COPY · REPLIES</div>
</div>
<img src="{{MONOGRAM}}" alt="" style="position:absolute;left:2190px;top:600px;height:240px;transform:rotate(6deg);opacity:.9;z-index:3;filter:drop-shadow(0 20px 30px rgba(60,15,0,.4))">
''')
# B06 — photo + sketch, educational channel
V['B06-photo-learn']=frame('B06','haze-none',r'''
<div style="position:absolute;left:300px;top:250px;width:1100px;height:950px;overflow:hidden;z-index:1;-webkit-mask-image:radial-gradient(48% 50% at 50% 52%,#000 50%,transparent 100%);mask-image:radial-gradient(48% 50% at 50% 52%,#000 50%,transparent 100%)">
  <img src="{{PHOTO}}" alt="" style="position:absolute;left:-90px;top:170px;height:1000px;filter:brightness(.62) saturate(.8) contrast(1.05)"></div>
<div style="position:absolute;left:1500px;top:300px;width:1200px;height:900px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,90,0,.30),rgba(255,90,0,0))"></div>
<div class="tx tx-dots" style="opacity:.3"></div>
<svg style="position:absolute;inset:0;z-index:3" width="2560" height="1440"><path d="M1030 760 C 1080 700, 1140 690, 1200 700" fill="none" stroke="#FF7A33" stroke-width="5" stroke-linecap="round"/><path d="M1182 684 L1204 701 L1180 716" fill="none" stroke="#FF7A33" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>
<div class="content" style="left:1210px;top:548px;z-index:4">
  <img src="{{LOGO}}" alt="Cymate" style="height:48px;display:block">
  <div style="margin-top:20px;font-family:Caveat,'Permanent Marker',cursive;font-weight:700;font-size:100px;line-height:.95;color:#fff">Learn outbound that</div>
  <div style="font-family:Poppins,sans-serif;font-weight:800;font-size:92px;letter-spacing:-3px;line-height:1"><span class="grad-text" style="padding-right:8px">books meetings.</span></div>
  <div class="mono" style="margin-top:22px;font-size:20px;letter-spacing:4px;color:rgba(255,255,255,.78)">COLD EMAIL · LISTS · DELIVERABILITY</div>
</div>
''', 'background:#070707')
for k,h in V.items(): pathlib.Path(k+'.html').write_text(h)
print(list(V))
