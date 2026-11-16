import random, math, pathlib
random.seed(21)
W,H=2560,1440
ang=math.radians(-58)  # streak direction: up and to the right
dx,dy=math.cos(ang),math.sin(ang)
def streak(x,y,length,width,color,op,blur):
    x2,y2=x+dx*length,y+dy*length
    return f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{color}" stroke-opacity="{op:.2f}" stroke-width="{width:.0f}" stroke-linecap="round" filter="url(#mb{blur})"/>'
grey=[]
for _ in range(130):
    x=random.uniform(-600,W+300); y=random.uniform(200,H+700)
    c=random.choice(['#3B3B3D','#2B2B2C','#4B4B4C','#1C1C1D','#5C5C5D'])
    grey.append(streak(x,y,random.uniform(500,1700),random.uniform(2,26),c,random.uniform(.12,.45),random.choice([1,2,3])))
orange=[]
for _ in range(16):
    x=random.uniform(-200,700); y=random.uniform(900,H+500)
    c=random.choice(['#FF5A00','#FF7A1A','#E03A00','#FFB070'])
    orange.append(streak(x,y,random.uniform(500,1300),random.uniform(14,60),c,random.uniform(.45,.95),random.choice([2,3])))
for _ in range(10):
    x=random.uniform(150,900); y=random.uniform(700,1300)
    orange.append(streak(x,y,random.uniform(300,800),random.uniform(4,10),'#FFC09A',random.uniform(.35,.7),1))
html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Cymate YouTube banner, Champions</title>{{{{BASE_CSS}}}}
<style>
/* "OUTBOUND FOR CHAMPIONS" look, matched to the official LinkedIn banner: brushed dark metal with diagonal speed streaks,
   orange streaks bottom-left, condensed Bebas Neue tagline fading white to orange, orange monogram tile, a huge ghosted mascot
   cropped off the right edge. Safe area (all devices) = centre 1546x423: x 507-2053, y 508-931. */
.tag{{font-family:'Bebas Neue','Archivo Black',sans-serif;font-size:150px;line-height:1;letter-spacing:1px;white-space:nowrap;
  background:linear-gradient(90deg,#FFFFFF 0%,#FFE9DC 18%,#FFC79F 42%,#FF9A52 70%,#FF6A10 100%);-webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 10px 24px rgba(0,0,0,.55))}}
</style></head><body>
<div class="cm haze-none" style="width:{W}px;height:{H}px;background:linear-gradient(115deg,#0C0C0C 0%,#181818 45%,#1F1F20 70%,#151515 100%)">
<svg style="position:absolute;inset:0" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
 <defs><filter id="mb1" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2"/></filter>
 <filter id="mb2" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="7"/></filter>
 <filter id="mb3" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="16"/></filter></defs>
 {''.join(grey)}
 {''.join(orange)}
</svg>
<div style="position:absolute;left:-300px;top:800px;width:1300px;height:900px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,90,0,.28),rgba(255,90,0,0))"></div>
<!-- ghosted mascot, cropped off the right edge (watermark, not a logo) -->
<img src="{{{{MASCOT}}}}" alt="" style="position:absolute;left:1870px;top:-70px;height:1320px;transform:rotate(-6deg);opacity:1;z-index:1">

<!-- SAFE AREA: tagline + monogram tile -->
<div class="content" style="left:0;right:0;top:640px;z-index:4;display:flex;align-items:center;justify-content:center;gap:28px">
  <div class="tag">OUTBOUND FOR CHAMPIONS</div>
  <img src="{{{{MONOGRAM}}}}" alt="Cymate" style="height:128px;flex:none;filter:drop-shadow(0 14px 26px rgba(0,0,0,.55))">
</div>
</div></body></html>'''
pathlib.Path('b07.html').write_text(html)
