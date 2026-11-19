# SEAMLESS SCRAPBOOK CAROUSEL GENERATOR (from the awa-posts format carousel-seamless-scrapbook, TOF).
# One wide canvas (N x 1080 px) with torn paper, a polaroid and a note that CROSS the slide edges, so each slide feels cut off
# and pulls the swipe. This script writes one HTML per slide (slides/01.html ...), each showing its 1080 px window of the
# same panorama, so the stills join perfectly.
# Edit: PANO (the shared canvas markup, global x positions) and N. Slide edges sit at x = 1080, 2160, 3240, 4320.
# Run from a working folder: python3 gen_scrapbook.py  -> slides/01.html ... then: python3 scripts/make_carousel.py slides/ out/name.pdf
# Rules: slide 1 = hook, last slide = CTA. Text never crosses a slide edge (only objects do). Logo on slide 1 and the last slide.
# AWA kit: paper #F6F1EA (allowed here: scrapbook posts), red, black, white; Anton hook, Caveat for the sticker, caption and note.
# No sticky-note yellow (not an AWA colour): the note is white paper.
import pathlib
W, H, N = 1080, 1350, 5

PANO = '''
<div style="position:absolute;left:0;top:0;width:1080px;height:1350px;background:#FFFFFF"></div>
<div style="position:absolute;left:1080px;top:0;width:2160px;height:1350px;background:#F6F1EA"></div>
<div class="redpanel" style="position:absolute;left:3240px;top:0;width:1080px;height:1350px"></div>
<div style="position:absolute;left:4320px;top:0;width:1080px;height:1350px;background:#000000"></div>

<img src="{{LOGO_DARK}}" alt="Agency Workplaces" style="position:absolute;left:96px;top:96px;height:48px">
<div class="display" style="position:absolute;left:96px;top:300px;width:760px;font-size:116px;color:#000">Why do good<br>people leave<br><span style="color:#CF0101">great agencies?</span></div>
<div class="hand" style="position:absolute;left:96px;top:1080px;background:#CF0101;color:#fff;padding:2px 34px 8px;border-radius:14px;transform:rotate(-4deg);font-size:76px">spoiler: not the money</div>

<!-- torn note crossing 1 -> 2 -->
<div style="position:absolute;left:860px;top:260px;width:820px;height:760px;background:#000;color:#fff;padding:120px 90px;box-sizing:border-box;transform:rotate(2deg);z-index:2;
  clip-path:polygon(0 3%,8% 0,20% 4%,35% 1%,50% 4%,66% 0,80% 3%,100% 1%,100% 97%,88% 100%,72% 96%,56% 100%,40% 97%,24% 100%,10% 96%,0 99%);filter:drop-shadow(0 30px 40px rgba(0,0,0,.3))">
  <div style="position:absolute;left:330px;top:110px;font-size:46px;font-weight:300;opacity:.75">The real reason?</div>
  <div class="h" style="position:absolute;left:330px;right:70px;top:190px;font-size:100px">They stopped feeling <span style="color:#FF3B3B">seen.</span></div>
</div>

<!-- polaroid crossing 2 -> 3 -->
<div style="position:absolute;left:1620px;top:170px;width:640px;height:960px;background:#fff;padding:30px 30px 120px;box-sizing:border-box;transform:rotate(-5deg);z-index:3;
  box-shadow:0 8px 16px rgba(0,0,0,.15),0 30px 60px rgba(0,0,0,.22)">
  <div class="photo-placeholder" data-edge style="position:relative;width:100%;height:100%">PHOTO: empty desk, last day</div>
  <div style="position:absolute;left:0;right:0;bottom:34px;text-align:center"><span class="hand" style="font-size:66px;color:#000">last day :(</span></div>
</div>
<div style="position:absolute;left:1820px;top:140px;width:230px;height:70px;background:rgba(207,1,1,.35);transform:rotate(-8deg);z-index:4"></div>

<div style="position:absolute;left:2560px;top:300px;width:600px;font-size:44px;line-height:1.55;color:#000;white-space:nowrap">
  <div class="h" style="font-size:64px;margin-bottom:30px">The quiet signs:</div>
  <div>They stop pitching ideas</div><div>They skip the extras</div><div>“I’m fine” sounds rehearsed</div>
</div>

<div class="h" style="position:absolute;left:3336px;top:250px;width:880px;font-size:110px;color:#fff">Notice early.<br>Recognize often.</div>
<!-- note crossing 3 -> 4 -->
<!-- the note crosses the edge, its text starts after it (x >= 3330) -->
<div style="position:absolute;left:3000px;top:780px;width:800px;padding:48px 48px 48px 330px;box-sizing:border-box;background:#fff;color:#000;transform:rotate(3deg);z-index:3;
  box-shadow:0 8px 16px rgba(0,0,0,.18),0 30px 60px rgba(0,0,0,.3)"><div class="hand" style="font-size:80px;line-height:1">recognition &gt; ping pong tables</div></div>

<img src="{{LOGO}}" alt="Agency Workplaces" style="position:absolute;left:4416px;top:96px;height:48px">
<div class="h-light" style="position:absolute;left:4416px;top:420px;width:880px;color:#fff;font-size:96px;line-height:1.05">Want to know<br>how your culture<br><b style="font-weight:800">really scores?</b></div>
<span class="pill pill-white" style="position:absolute;left:4416px;bottom:120px">Follow for part 2</span>
'''

def page(i):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>AWA scrapbook slide {i+1}</title>{{{{BASE_CSS}}}}</head><body>
<div class="aw paper" data-panorama style="width:{W}px;height:{H}px">
<div style="position:absolute;left:{-i*W}px;top:0;width:{N*W}px;height:{H}px">{PANO}</div>
<div class="count" data-edge style="position:absolute;right:96px;bottom:64px;z-index:9;color:{'#000' if i < 3 else '#fff'}">{i+1} / {N}</div>
</div></body></html>'''

pathlib.Path("slides").mkdir(exist_ok=True)
for i in range(N):
    pathlib.Path(f"slides/{i+1:02d}.html").write_text(page(i))
print(f"wrote slides/01.html ... slides/{N:02d}.html")
