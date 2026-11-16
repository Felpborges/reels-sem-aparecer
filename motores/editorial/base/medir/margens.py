"""Confere se toda palavra/pílula/cartão cabe no quadro com margem (regra: nenhuma palavra cortada).
Build parado (MEDIR=1, sem câmera) -> Chrome headless -> retângulo de cada elemento em px do espaço 720x1280."""
import subprocess, json, os, re, sys, pathlib
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); MARGEM = 36
subprocess.run([sys.executable, "build.py"], cwd=AQUI, env={**os.environ, "MEDIR": "1", "SO_VOZ": "1"}, capture_output=True)
html = open(os.path.join(AQUI, "index.html")).read()
js = """<script>window.addEventListener('load',()=>{setTimeout(()=>{const o=[];document.querySelectorAll('.wd,.pill,.ln,.im,.badge').forEach(e=>{const r=e.getBoundingClientRect();if(r.width>0)o.push([e.id||e.parentElement.id,e.className,e.textContent.trim().slice(0,24),Math.round(r.left/1.5),Math.round(r.right/1.5),Math.round(r.top/1.5),Math.round(r.bottom/1.5)])});const d=document.createElement('pre');d.id='__rects';d.textContent=JSON.stringify(o);document.body.appendChild(d)},1200)})</script></body>"""
open(os.path.join(AQUI, "medir", "_margens.html"), "w").write(html.replace('src="assets/', 'src="../assets/').replace("url('assets/", "url('../assets/").replace("</body>", js))
dom = subprocess.run([os.environ.get("RSA_CHROME") or "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1080,1920", "--allow-file-access-from-files",
                      "--virtual-time-budget=6000", "--dump-dom", pathlib.Path(AQUI, "medir", "_margens.html").as_uri()], capture_output=True, text=True).stdout
m = re.search(r'<pre id="__rects">(.*?)</pre>', dom, re.S); R = json.loads(m.group(1).replace("&quot;", '"').replace("&amp;", "&"))
ruins = [r for r in R if ("wd" in r[1] or "pill" in r[1] or "badge" in r[1]) and (r[3] < MARGEM or r[4] > 720 - MARGEM or r[5] < 60 or r[6] > 1230)]
print(len(R), "elementos medidos;", len(ruins), "fora da margem de", MARGEM, "px")
for r in ruins: print("  ", r)
os.remove(os.path.join(AQUI, "medir", "_margens.html"))
subprocess.run([sys.executable, "build.py"], cwd=AQUI, capture_output=True)   # devolve o index.html normal (câmera + mixagem)
sys.exit(1 if ruins else 0)
