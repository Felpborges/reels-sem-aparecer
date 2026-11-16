// ESTILO C · tira quadros do index.html SEM renderizar o vídeo (rápido, para conferir layout e tempos).
// uso: node medir/quadros.mjs saida_prefixo t1 t2 ...   -> saida_prefixo-<t>.png (1080x1920)
import { createRequire } from "module"; import { fileURLToPath } from "url"; import http from "http"; import fs from "fs"; import path from "path";
const require = createRequire(process.env.RSA_NODE_MODULES || (process.env.HOME + "/.claude/skills/reels-sem-aparecer/ferramentas/node_modules/"));
const puppeteer = require("puppeteer-core");
const DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const [pre, ...ts] = process.argv.slice(2); const PORTA = 8740 + Math.floor(Math.random() * 200);
const TIPOS = { ".html": "text/html", ".js": "text/javascript", ".woff2": "font/woff2", ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml", ".mp4": "video/mp4", ".m4a": "audio/mp4", ".wav": "audio/wav" };
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
for (const t of ts) {
  await page.evaluate((t) => { const tl = window.__timelines.main; tl.seek(+t, false);
    for (const c of document.querySelectorAll("#stage > .clip")) { const a = +c.dataset.start, d = +c.dataset.duration; c.style.display = (t >= a && t < a + d) ? "" : "none"; }
    for (const v of document.querySelectorAll("#stage > video[data-start]")) { const a = +v.dataset.start, d = +v.dataset.duration;
      const on = t >= a && t < a + d; v.style.display = on ? "" : "none"; if (on) v.currentTime = (t - a) + (+v.dataset.mediaStart || 0); } }, t);
  await page.evaluate(() => Promise.all([...document.querySelectorAll("#stage > video")].filter((v) => v.style.display !== "none")
    .map((v) => new Promise((r) => { if (!v.seeking && v.readyState >= 2) return r(); v.addEventListener("seeked", r, { once: true }); setTimeout(r, 1500); }))));
  await page.screenshot({ path: `${pre}-${(+t).toFixed(2)}.png` });
}
await browser.close(); srv.close();
