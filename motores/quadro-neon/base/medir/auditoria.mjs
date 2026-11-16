// ESTILO C · AUDITORIA QUADRO A QUADRO do texto (regra do Felipe, 12/11/2026: nenhuma palavra cortada, coberta ou encostada).
// uso: node medir/auditoria.mjs [fps=30]   -> medir/auditoria.json
// Para cada quadro: avança a timeline, liga só a seção ativa e mede CADA PALAVRA visível (opacidade >= 0,35):
//   corte (parte fora do quadro) · rente (a menos de 22 px da borda, em 1080) · coberta (imagem/print por cima)
//   encosta (palavras de elementos diferentes sobrepostas) · zona-ig (coluna dos botões do Instagram ou rodapé)
import { createRequire } from "module"; import { fileURLToPath } from "url"; import http from "http"; import fs from "fs"; import path from "path";
const require = createRequire(process.env.RSA_NODE_MODULES || (process.env.HOME + "/.claude/skills/reels-sem-aparecer/ferramentas/node_modules/"));
const puppeteer = require("puppeteer-core");
const DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const FPS = Number(process.argv[2] || 30), PORTA = 8940 + Math.floor(Math.random() * 50);
const TIPOS = { ".html": "text/html", ".js": "text/javascript", ".woff2": "font/woff2", ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml", ".mp4": "video/mp4" };
const srv = http.createServer((q, r) => { const f = path.join(DIR, decodeURIComponent(q.url.split("?")[0]));
  fs.stat(f, (e, st) => { if (e) { r.writeHead(404); r.end(); return; }
    const tipo = TIPOS[path.extname(f)] || "application/octet-stream", rg = q.headers.range;
    if (rg) { const [a, b] = rg.replace("bytes=", "").split("-"); const ini = +a, fim = b ? +b : st.size - 1;      // range: o Chrome precisa para pular dentro do vídeo
      r.writeHead(206, { "Content-Type": tipo, "Accept-Ranges": "bytes", "Content-Range": `bytes ${ini}-${fim}/${st.size}`, "Content-Length": fim - ini + 1 });
      fs.createReadStream(f, { start: ini, end: fim }).pipe(r); }
    else { r.writeHead(200, { "Content-Type": tipo, "Accept-Ranges": "bytes", "Content-Length": st.size }); fs.createReadStream(f).pipe(r); } }); }).listen(PORTA);
const browser = await puppeteer.launch({ executablePath: process.env.RSA_CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless: "new", args: ["--hide-scrollbars"] });
const page = await browser.newPage(); await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
await page.goto(`http://localhost:${PORTA}/index.html`, { waitUntil: "load", timeout: 180000 });
await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map((i) => i.decode().catch(() => 0))); });
const dur = await page.evaluate(() => Number(document.getElementById("root").dataset.duration));
const res = [];
for (let q = 0; q < Math.round(dur * FPS); q++) {
  const t = (q + 0.5) / FPS;
  res.push(await page.evaluate((t) => {
    window.__timelines.main.seek(t, false);
    for (const c of document.querySelectorAll("#stage > .clip")) { const a = +c.dataset.start, d = +c.dataset.duration; c.style.display = (t >= a && t < a + d) ? "" : "none"; }
    for (const v of document.querySelectorAll("#stage > video[data-start]")) { const a = +v.dataset.start, d = +v.dataset.duration;
      const on = t >= a && t < a + d; v.style.display = on ? "" : "none"; if (on) v.currentTime = (t - a) + (+v.dataset.mediaStart || 0); }
    const opac = (el) => { let o = 1; for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.display === "none" || cs.visibility === "hidden") return 0; o *= +cs.opacity; } return o; };
    const dono = (el) => { for (let e = el; e; e = e.parentElement) if (e.id) return e.id; return "?"; };
    const W = 1080, H = 1920, palavras = [];
    const walker = document.createTreeWalker(document.getElementById("stage"), NodeFilter.SHOW_TEXT); let n;
    while ((n = walker.nextNode())) {
      const el = n.parentElement; if (!n.data.trim() || el.closest(".deco")) continue;
      const op = opac(el); if (op < 0.35) continue;
      const re = /\S+/g; let m;
      while ((m = re.exec(n.data))) {
        const rg = document.createRange(); rg.setStart(n, m.index); rg.setEnd(n, m.index + m[0].length);
        const r = rg.getBoundingClientRect(); if (r.width < 1 || r.height < 1) continue;
        palavras.push({ w: m[0], el, r, id: dono(el) });
      }
    }
    // palavras digitadas letra a letra: junta as letras visíveis do mesmo elemento numa "palavra"
    for (const p of palavras) {
      const { r } = p; const iss = [];
      const ix = Math.max(0, Math.min(r.right, W) - Math.max(r.left, 0)), iy = Math.max(0, Math.min(r.bottom, H) - Math.max(r.top, 0));
      const vis = (ix * iy) / (r.width * r.height);
      if (vis < 0.97) iss.push(vis < 0.03 ? "fora" : "corte");
      else if (r.left < 22 || r.right > W - 22 || r.top < 22 || r.bottom > H - 22) iss.push("rente");
      let cob = 0, quem = "";
      for (const [fx, fy] of [[.5, .5], [.2, .5], [.8, .5]]) {
        const x = r.left + r.width * fx, y = r.top + r.height * fy; if (x < 0 || y < 0 || x >= W || y >= H) continue;
        for (const h of document.elementsFromPoint(x, y)) {
          if (h === p.el || p.el.contains(h) || h.contains(p.el)) break;
          if (opac(h) < 0.3 || h.closest(".deco") || h.classList.contains("secao")) continue;
          if (h.tagName === "IMG") { cob++; quem = dono(h); break; }
        }
      }
      if (cob >= 2) iss.push("coberta:" + quem);
      if ((r.right > W * 0.9 && r.top > H * 0.52 && r.bottom < H * 0.84) || r.bottom > H * 0.88) iss.push("zona-ig");
      p.iss = iss;
    }
    for (let i = 0; i < palavras.length; i++) for (let j = i + 1; j < palavras.length; j++) {
      const a = palavras[i], b = palavras[j]; if (a.id === b.id) continue;
      const fa = (r) => ({ l: r.left + r.width * .04, r: r.right - r.width * .04, t: r.top + r.height * .25, b: r.bottom - r.height * .22 });
      const A_ = fa(a.r), B_ = fa(b.r);
      const ix = Math.max(0, Math.min(A_.r, B_.r) - Math.max(A_.l, B_.l)), iy = Math.max(0, Math.min(A_.b, B_.b) - Math.max(A_.t, B_.t));
      if (ix * iy > 0.06 * Math.min(a.r.width * a.r.height, b.r.width * b.r.height)) { a.iss.push("encosta:" + b.w); b.iss.push("encosta:" + a.w); }
    }
    return { t: +t.toFixed(3), palavras: palavras.map((p) => ({ w: p.w, id: p.id, x: Math.round(p.r.left), y: Math.round(p.r.top), iss: p.iss })) };
  }, t));
}
fs.writeFileSync(path.join(DIR, "medir", "auditoria.json"), JSON.stringify(res));
await browser.close(); srv.close(); console.log("ok", res.length, "quadros");
